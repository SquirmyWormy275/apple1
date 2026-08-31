"""Repository-wide schemas, structure, documentation, ASCII, and provenance validation."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Sequence
from pathlib import Path

from jsonschema import Draft202012Validator

from neural1.visualization import lint_provenance, validate_frame

REQUIRED_PATHS = (
    "README.md",
    "docs/PROJECT-MAP.md",
    "docs/repository/README.md",
    "docs/repository/architecture.md",
    "docs/repository/git-archaeology-2026-08-30.md",
    "docs/repository/provenance-audit-2026-08-30.md",
    "docs/neural1/research/pilot-001/README.md",
    "docs/field-library/README.md",
    "docs/peripherals/displays/README.md",
    "cf-card/README.md",
    "preservation/cf-card/2026-08-28/MANIFEST.md",
    "firmware/vendor/110REV03/provenance.json",
    "data/neural1/history/1976-research-index.json",
)

SKIPPED_MARKDOWN_PARTS = {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".neural1", "external", "out"}


def _first_party_markdown(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*.md"))
        if not any(part in SKIPPED_MARKDOWN_PARTS for part in path.relative_to(root).parts)
    ]


def _validate_markdown_links(root: Path, path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        link = link.strip().strip("<>")
        if not link or link.startswith("#") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", link):
            continue
        raw_target = link.split("#", 1)[0].split("?", 1)[0]
        if not raw_target:
            continue
        target = (root / raw_target.lstrip("/")) if raw_target.startswith("/") else (path.parent / raw_target)
        if not target.resolve().exists():
            errors.append(f"{path.relative_to(root)}: broken link {link}")
    return errors


def validate_repository(root: str | Path) -> list[str]:
    root_path = Path(root).resolve()
    errors: list[str] = []

    for relative_path in REQUIRED_PATHS:
        if not (root_path / relative_path).exists():
            errors.append(f"missing required repository anchor: {relative_path}")

    for schema_path in sorted((root_path / "schemas" / "neural1").glob("*.schema.json")):
        try:
            Draft202012Validator.check_schema(json.loads(schema_path.read_text(encoding="utf-8")))
        except Exception as error:
            errors.append(f"{schema_path.relative_to(root_path)}: invalid schema: {error}")

    instances = {
        "campaign.schema.json": root_path / "configs" / "neural1" / "pilot-001" / "campaign.json",
        "historical-research-index.schema.json": root_path / "data" / "neural1" / "history" / "1976-research-index.json",
        "model-registry.schema.json": root_path / "configs" / "neural1" / "pilot-001" / "model-registry.template.json",
    }
    for schema_name, instance_path in instances.items():
        try:
            schema = json.loads((root_path / "schemas" / "neural1" / schema_name).read_text(encoding="utf-8"))
            Draft202012Validator(schema).validate(json.loads(instance_path.read_text(encoding="utf-8")))
        except Exception as error:
            errors.append(f"{instance_path.relative_to(root_path)}: schema validation failed: {error}")

    research_index_path = root_path / "data" / "neural1" / "history" / "1976-research-index.json"
    try:
        research_index = json.loads(research_index_path.read_text(encoding="utf-8"))
        runtime_ids = research_index.get("runtime_authoritative_component_ids", [])
        if research_index.get("authoritative_runtime_records") != len(runtime_ids):
            errors.append(
                f"{research_index_path.relative_to(root_path)}: authoritative_runtime_records does not match runtime_authoritative_component_ids"
            )
        for research_input in research_index.get("research_inputs", []):
            source_path = root_path / research_input["path"]
            if not source_path.exists():
                errors.append(f"{research_index_path.relative_to(root_path)}: missing research input {research_input['path']}")
        if research_index.get("status") == "RESEARCH_STAGING" and runtime_ids:
            errors.append(f"{research_index_path.relative_to(root_path)}: staging corpus cannot contain authoritative runtime component IDs")
        policy = research_index.get("promotion_policy", {})
        required_policy = (
            "requires_sha256",
            "requires_claim_review",
            "requires_cutoff_validation",
            "missing_prices_remain_null",
            "no_llm_estimates",
        )
        if not all(policy.get(key) is True for key in required_policy):
            errors.append(f"{research_index_path.relative_to(root_path)}: historical promotion policy is incomplete or unsafe")
    except Exception as error:
        errors.append(f"{research_index_path.relative_to(root_path)}: research-index validation failed: {error}")

    for path in _first_party_markdown(root_path):
        errors.extend(_validate_markdown_links(root_path, path))

    for path in sorted((root_path / "art").rglob("*.txt")):
        errors.extend(f"{path.relative_to(root_path)}: {error}" for error in validate_frame(path.read_text(encoding="ascii")))
    errors.extend(lint_provenance(root_path / "art" / "provenance"))
    return errors


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path.cwd())
    args = parser.parse_args(argv)
    errors = validate_repository(args.root)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2, sort_keys=True))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
