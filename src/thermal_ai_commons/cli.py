"""Command-line entry points for Thermal AI Commons."""

from __future__ import annotations

import argparse
from pathlib import Path

from thermal_ai_commons.contracts import ManifestValidationError, validate_manifest_file


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
    args = parser.parse_args()

    if args.command == "validate":
        try:
            validate_manifest_file(args.manifest, args.schema, args.profile)
        except (ManifestValidationError, OSError) as error:
            parser.exit(2, f"validation failed: {error}\n")
        print(f"valid manifest: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
