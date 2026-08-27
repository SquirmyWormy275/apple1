"""Compile-only provenance preflight for a future Propeller toolchain."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Sequence


def preflight_toolchain(source_root: str | Path, tool_path: str | Path | None = None) -> dict[str, object]:
    """Describe what is known without invoking a compiler or programmer."""
    root = Path(source_root)
    readme = (root / "_README_.txt").read_text(encoding="utf-16")
    match = re.search(r"Tool\s*:\s*(.+)", readme)
    if match is None:
        raise ValueError("vendor archive does not identify its original tool")
    tool = Path(tool_path) if tool_path is not None else None
    return {
        "action": "compile-only-preflight",
        "device_access": False,
        "compiler_invoked": False,
        "archived_tool": match.group(1).strip(),
        "tool_present": tool is not None and tool.is_file(),
        "tool_path": str(tool) if tool is not None else None,
        "vendor_readme_sha256": hashlib.sha256((root / "_README_.txt").read_bytes()).hexdigest(),
        "required_before_compile": [
            "recorded tool executable version and SHA-256",
            "separate output directory",
            "candidate-source hash check",
            "no programmer or serial owner lease",
        ],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--tool", type=Path)
    args = parser.parse_args(argv)
    print(json.dumps(preflight_toolchain(args.source, args.tool), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
