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
import shutil
import sys
from pathlib import Path

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
    repo_root = repo_root.resolve(strict=True)
    # Validate the entire plan before creating anything. Never replace a user's
    # directory, follow a source symlink, or allow a manifest to escape its roots.
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"output already exists: {output}; choose a new directory")
    output = output.resolve()
    if output == repo_root or output in repo_root.parents:
        raise ValueError("output must not contain the repository")

    def source_path(relative: str) -> Path:
        rel = Path(relative)
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError(f"source must be relative to the repository: {relative}")
        path = repo_root / rel
        for part in [path, *path.parents]:
            if part == repo_root:
                break
            if part.is_symlink():
                raise ValueError(f"symlink source: {part}")
        if not path.exists():
            raise FileNotFoundError(path)
        files = list(path.rglob("*")) if path.is_dir() else [path]
        if any(p.is_symlink() or not (p.is_file() or p.is_dir()) for p in files):
            raise ValueError(f"source contains a symlink or special file: {path}")
        if output == path or path in output.parents:
            raise ValueError("output must not be inside an exported source")
        return path

    baseline = manifest["baseline"]
    baseline_manifest = source_path(baseline["manifest_path"])
    image = None
    if include_baseline_image:
        image = source_path(baseline["image_path"])
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
    plan: list[tuple[Path, Path]] = []
    destinations = [Path("metadata"), Path("baseline")]
    for source in manifest["sources"]:
        selected = source.get("include_in_default_export", False)
        if not selected and not include_candidates:
            continue

        source_root = source_path(source["source_path"])
        if source.get("format") == "ascii-40x24":
            errors = validate_ascii_40x24(source_root)
            if errors:
                raise ValueError("\n".join(errors))

        relative = Path(source["staging_path"])
        if not relative.parts or relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"invalid staging path: {relative}")
        if any(relative == p or p in relative.parents or relative in p.parents for p in destinations):
            raise ValueError(f"overlapping staging path: {relative}")
        destinations.append(relative)
        plan.append((source_root, output / relative))

    output.mkdir(parents=True, exist_ok=False)
    metadata = output / "metadata"
    metadata.mkdir()
    shutil.copy2(baseline_manifest, metadata / "ORIGINAL-CF-MANIFEST.md")
    (metadata / "SOURCE-REGISTRY.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if image is not None:
        baseline_dir = output / "baseline"
        baseline_dir.mkdir()
        shutil.copy2(image, baseline_dir / image.name)
    for source_root, destination in plan:
        if source_root.is_dir():
            shutil.copytree(source_root, destination)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_root, destination)

    inventory = {
        p.relative_to(output).as_posix(): {"bytes": p.stat().st_size, "sha256": sha256_file(p)}
        for p in sorted(output.rglob("*")) if p.is_file()
    }
    (metadata / "FILES.json").write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")


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
