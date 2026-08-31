"""Query persistent META/1 records without invoking a language model."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from .meta_store import ResearchDatabase


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    claim = commands.add_parser("claim")
    claim.add_argument("claim_id")
    history = commands.add_parser("history")
    history.add_argument("claim_id")
    history.add_argument("--through-sequence", type=int)
    commands.add_parser("queue")
    tribunal = commands.add_parser("tribunal")
    tribunal.add_argument("claim_id")
    tribunal.add_argument("--minimum-causal-level", type=int, default=0)
    args = parser.parse_args(argv)
    database = ResearchDatabase(args.db)
    try:
        result: Any
        if args.command == "claim":
            result = database.claim(args.claim_id) or {"status": "INSUFFICIENT_EVIDENCE", "claim_id": args.claim_id}
        elif args.command == "history":
            result = database.claim_history(args.claim_id, through_sequence=args.through_sequence)
        elif args.command == "queue":
            result = database.research_queue()
        else:
            result = database.tribunal(args.claim_id, minimum_causal_level=args.minimum_causal_level)
        print(json.dumps(result, indent=2, sort_keys=True))
    finally:
        database.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
