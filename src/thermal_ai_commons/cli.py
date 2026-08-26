"""Command-line entry points for Thermal AI Commons."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from thermal_ai_commons.contracts import ManifestValidationError, validate_manifest_file
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
