"""Build a host-side staging tree from the CF-card source manifest.

This tool never opens a block device, serial port, CFFA1, or mounted CF card. It
copies repository files into an ordinary output directory for review/build
preparation. The preserved baseline image is optional and is copied only after
size and SHA-256 verification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

DEFAULT_MANIFEST = Path("cf-card/manifests/current.json")
DEFAULT_OUTPUT = Path("out/cf-card-staging")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_ascii_40x24(root: Path) -> list[str]:
    """Return validation errors for a display-native ASCII source tree."""
    errors: list[str] = []
    pages = sorted(root.rglob("*.txt"))
    if not pages:
        return [f"{root}: no .txt card pages found"]

    for page in pages:
        try:
            text = page.read_bytes().decode("ascii")
        except UnicodeDecodeError as exc:
            errors.append(f"{page}: non-ASCII content: {exc}")
            continue

        lines = text.splitlines()
        if len(lines) > 24:
            errors.append(f"{page}: {len(lines)} lines exceeds 24")
        for number, line in enumerate(lines, 1):
            if len(line) > 40:
                errors.append(
                    f"{page}:{number}: {len(line)} columns exceeds 40"
                )
            if line != line.upper():
                errors.append(f"{page}:{number}: lowercase source text")
            if any(not (" " <= character <= "~") for character in line):
                errors.append(f"{page}:{number}: non-printable ASCII")
    return errors


def load_manifest(repo_root: Path, manifest_path: Path) -> dict:
    path = manifest_path if manifest_path.is_absolute() else repo_root / manifest_path
    return json.loads(path.read_text(encoding="utf-8"))


def export_sources(
    repo_root: Path,
    manifest: dict,
    output: Path,
    *,
    include_candidates: bool = False,
    include_baseline_image: bool = False,
) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    metadata = output / "metadata"
    metadata.mkdir()

    baseline = manifest["baseline"]
    baseline_manifest = repo_root / baseline["manifest_path"]
    if not baseline_manifest.is_file():
        raise FileNotFoundError(baseline_manifest)
    shutil.copy2(baseline_manifest, metadata / "ORIGINAL-CF-MANIFEST.md")

    (metadata / "SOURCE-REGISTRY.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    if include_baseline_image:
        image = repo_root / baseline["image_path"]
        if not image.is_file():
            raise FileNotFoundError(image)
        expected_size = int(baseline["size_bytes"])
        actual_size = image.stat().st_size
        if actual_size != expected_size:
            raise ValueError(
                f"baseline image size {actual_size} != expected {expected_size}; "
                "Git LFS may not be hydrated"
            )
        actual_hash = sha256_file(image)
        if actual_hash.lower() != baseline["sha256"].lower():
            raise ValueError("baseline image SHA-256 does not match manifest")
        baseline_dir = output / "baseline"
        baseline_dir.mkdir()
        shutil.copy2(image, baseline_dir / image.name)

    for source in manifest["sources"]:
        selected = source.get("include_in_default_export", False)
        if not selected and not include_candidates:
            continue

        source_root = repo_root / source["source_path"]
        if not source_root.exists():
            raise FileNotFoundError(source_root)

        if source.get("format") == "ascii-40x24":
            errors = validate_ascii_40x24(source_root)
            if errors:
                raise ValueError("\n".join(errors))

        destination = output / source["staging_path"]
        if source_root.is_dir():
            shutil.copytree(source_root, destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_root, destination)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export approved CF-card sources to a host-side staging tree."
    )
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--include-candidates",
        action="store_true",
        help="also stage sources whose default-export flag is false",
    )
    parser.add_argument(
        "--include-baseline-image",
        action="store_true",
        help="copy the hydrated original image after size/SHA-256 verification",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    output = args.output
    if not output.is_absolute():
        output = repo_root / output

    manifest = load_manifest(repo_root, args.manifest)
    export_sources(
        repo_root,
        manifest,
        output,
        include_candidates=args.include_candidates,
        include_baseline_image=args.include_baseline_image,
    )
    print(f"staged CF-card sources at {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
