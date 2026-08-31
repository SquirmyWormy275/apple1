"""Repository-wide NEURAL1 schemas, documentation, ASCII, and provenance validation."""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Sequence
from pathlib import Path

from jsonschema import Draft202012Validator

from neural1.visualization import lint_provenance, validate_frame


def validate_repository(root: str | Path) -> list[str]:
    root_path = Path(root)
    errors: list[str] = []
    for schema_path in sorted((root_path / "schemas" / "neural1").glob("*.schema.json")):
        try:
            Draft202012Validator.check_schema(json.loads(schema_path.read_text(encoding="utf-8")))
        except Exception as error:
            errors.append(f"{schema_path.relative_to(root_path)}: invalid schema: {error}")
    instances = {
        "campaign.schema.json": root_path / "configs" / "neural1" / "pilot-001" / "campaign.json",
        "model-registry.schema.json": root_path / "configs" / "neural1" / "pilot-001" / "model-registry.template.json",
    }
    for schema_name, instance_path in instances.items():
        try:
            schema = json.loads((root_path / "schemas" / "neural1" / schema_name).read_text(encoding="utf-8"))
            Draft202012Validator(schema).validate(json.loads(instance_path.read_text(encoding="utf-8")))
        except Exception as error:
            errors.append(f"{instance_path.relative_to(root_path)}: schema validation failed: {error}")
    markdown = [root_path / "README.md", *(root_path / "docs" / "neural1").rglob("*.md"), *(root_path / "docs" / "visual-system").rglob("*.md"), *(root_path / "art").rglob("*.md"), *(root_path / "wiki").rglob("*.md")]
    for path in markdown:
        for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in link or link.startswith("#"):
                continue
            target = (path.parent / link.split("#", 1)[0]).resolve()
            if not target.exists():
                errors.append(f"{path.relative_to(root_path)}: broken link {link}")
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
