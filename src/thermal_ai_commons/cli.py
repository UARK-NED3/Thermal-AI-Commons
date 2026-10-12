"""Command-line entry points for Thermal AI Commons."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from thermal_ai_commons.contracts import ManifestValidationError, validate_manifest_file
from thermal_ai_commons.reports import create_evidence_report, write_evidence_report
from thermal_ai_commons.resources import (
    ResourceCardValidationError,
    ResourceManifestValidationError,
    load_resource_manifest,
    load_resource_registry,
)
from thermal_ai_commons.splits import make_group_split, write_group_split_manifest


def main() -> int:
    parser = argparse.ArgumentParser(prog="thermal-ai-commons")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate", help="validate an experiment manifest")
    validate_parser.add_argument("manifest", type=Path, help="JSON experiment-manifest file")
    validate_parser.add_argument("--schema", type=Path, help="optional replacement JSON Schema")
    validate_parser.add_argument(
        "--profile",
        choices=("core", "quantitative-multimodal"),
        default="core",
        help="metadata profile to validate; does not establish physical validation",
    )
    split_parser = subparsers.add_parser("split", help="create a deterministic group-level split manifest")
    split_parser.add_argument("groups", type=Path, help="JSON file with experiment_id, group_unit, and groups")
    split_parser.add_argument("--out", type=Path, required=True, help="output split-manifest JSON path")
    split_parser.add_argument("--seed", type=int, default=0, help="deterministic shuffle seed")
    report_parser = subparsers.add_parser("report", help="create a machine-readable evidence report")
    report_parser.add_argument("--input", type=Path, required=True, help="JSON result and claim declaration")
    report_parser.add_argument("--manifest", type=Path, required=True, help="experiment-manifest JSON path")
    report_parser.add_argument("--split", type=Path, required=True, help="group split-manifest JSON path")
    report_parser.add_argument(
        "--registry",
        type=Path,
        default=Path("components/registry-v0.1.json"),
        help="pinned component registry JSON path",
    )
    report_parser.add_argument("--out", type=Path, required=True, help="output evidence-report JSON path")
    resources_parser = subparsers.add_parser("resources", help="validate or list workflow-routing resource cards")
    resources_parser.add_argument("action", choices=("validate", "list"))
    resources_parser.add_argument(
        "registry", type=Path, nargs="?", default=Path("components/resource-cards-v0.1.json"),
        help="resource-card registry JSON path",
    )
    resource_manifest_parser = subparsers.add_parser(
        "resource-manifest", help="validate repository-owned resource metadata"
    )
    resource_manifest_parser.add_argument("action", choices=("validate",))
    resource_manifest_parser.add_argument("manifest", type=Path, help="resource-manifest JSON path")
    args = parser.parse_args()

    if args.command == "validate":
        try:
            validate_manifest_file(args.manifest, args.schema, args.profile)
        except (ManifestValidationError, OSError) as error:
            parser.exit(2, f"validation failed: {error}\n")
        print(f"valid manifest: {args.manifest}")
    if args.command == "split":
        try:
            groups_document = json.loads(args.groups.read_text(encoding="utf-8"))
            split_manifest = make_group_split(
                groups_document["groups"],
                experiment_id=groups_document["experiment_id"],
                group_unit=groups_document["group_unit"],
                seed=args.seed,
            )
            write_group_split_manifest(args.out, split_manifest)
        except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
            parser.exit(2, f"split creation failed: {error}\n")
        print(f"wrote split manifest: {args.out}")
    if args.command == "report":
        try:
            report = create_evidence_report(args.input, args.manifest, args.split, args.registry)
            write_evidence_report(args.out, report)
        except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
            parser.exit(2, f"evidence report creation failed: {error}\n")
        print(f"wrote evidence report: {args.out}")
    if args.command == "resources":
        try:
            registry = load_resource_registry(args.registry)
        except (ResourceCardValidationError, OSError, json.JSONDecodeError) as error:
            parser.exit(2, f"resource-card validation failed: {error}\n")
        if args.action == "validate":
            print(f"valid resource-card registry: {args.registry}")
        else:
            for card in registry["cards"]:
                print(f"{card['id']}: {card['product_kind']} ({card['evidence_ceiling']})")
    if args.command == "resource-manifest":
        try:
            load_resource_manifest(args.manifest)
        except (ResourceManifestValidationError, OSError, json.JSONDecodeError) as error:
            parser.exit(2, f"resource-manifest validation failed: {error}\n")
        print(f"valid resource manifest: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
