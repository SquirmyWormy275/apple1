"""NEURAL1 command-line interface for validation, campaigns, and bundles."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from .bundle import export_bundle, verify_bundle
from .campaign import CampaignEngine, CampaignSpec
from .drivers import objective, parse_commands
from .evaluation import evaluate_campaign
from .pilot_report import generate_pilot_001
from .provider_factory import provider_for
from .qualification import qualify_registry
from .registry import ModelRegistry


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate-campaign")
    validate.add_argument("spec", type=Path)
    validate.add_argument("registry", type=Path)
    run = commands.add_parser("run-campaign")
    run.add_argument("spec", type=Path)
    run.add_argument("registry", type=Path)
    run.add_argument("--output", type=Path, required=True)
    cancel = commands.add_parser("cancel-campaign")
    cancel.add_argument("campaign_root", type=Path)
    bundle = commands.add_parser("export-bundle")
    bundle.add_argument("source", type=Path)
    bundle.add_argument("destination", type=Path)
    bundle.add_argument("--reproduce", required=True)
    verify = commands.add_parser("verify-bundle")
    verify.add_argument("bundle", type=Path)
    evaluate = commands.add_parser("evaluate-campaign")
    evaluate.add_argument("campaign_root", type=Path)
    report = commands.add_parser("pilot-report")
    report.add_argument("campaign_root", type=Path)
    report.add_argument("registry", type=Path)
    report.add_argument("destination", type=Path)
    report.add_argument("--runtime-metadata", type=Path)
    report.add_argument("--thermal-log", type=Path)
    report.add_argument("--meta-database", type=Path)
    qualify = commands.add_parser("qualify-models")
    qualify.add_argument("registry", type=Path)
    qualify.add_argument("destination", type=Path)
    args = parser.parse_args(argv)

    if args.command == "validate-campaign":
        spec = CampaignSpec.load(args.spec)
        registry = ModelRegistry.load(args.registry, allow_unqualified=True)
        missing = sorted(set(spec.model_ids) - registry.models.keys())
        result = {"valid": not missing, "campaign_id": spec.campaign_id, "cells": len(spec.cells), "missing_models": missing}
        print(json.dumps(result, indent=2, sort_keys=True))
        return int(bool(missing))
    if args.command == "run-campaign":
        spec = CampaignSpec.load(args.spec)
        registry = ModelRegistry.load(args.registry)
        providers = {model_id: provider_for(registry.require(model_id), record_path=args.output / "model-recordings" / f"{model_id}.jsonl") for model_id in spec.model_ids}
        summary = CampaignEngine(args.output, registry, providers).run(spec, objective_factory=objective, command_parser=parse_commands)
        print(json.dumps(asdict(summary), indent=2, sort_keys=True))
        return 0 if summary.status == "COMPLETED" else 2
    if args.command == "cancel-campaign":
        args.campaign_root.mkdir(parents=True, exist_ok=True)
        (args.campaign_root / "CANCEL").touch(exist_ok=True)
        return 0
    if args.command == "export-bundle":
        print(export_bundle(args.source, args.destination, reproduction_command=args.reproduce))
        return 0
    if args.command == "evaluate-campaign":
        print(json.dumps(evaluate_campaign(args.campaign_root), indent=2, sort_keys=True))
        return 0
    if args.command == "pilot-report":
        result = generate_pilot_001(args.campaign_root, args.registry, args.destination, runtime_metadata=args.runtime_metadata, thermal_log=args.thermal_log, meta_database=args.meta_database)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if args.command == "qualify-models":
        result = qualify_registry(args.registry, args.destination)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["qualified"] else 2
    verification = verify_bundle(args.bundle)
    print(json.dumps(asdict(verification), indent=2, sort_keys=True))
    return 0 if verification.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
