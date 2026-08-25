"""Versioned experiment-manifest validation utilities."""

from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


class ManifestValidationError(ValueError):
    """Raised when an experiment manifest violates its declared contract."""


def default_schema_path() -> Path:
    """Return the installed v0.1 experiment-manifest schema path."""
    return Path(files("thermal_ai_commons").joinpath("_schemas/experiment-manifest-v0.1.json"))


def load_schema(schema_path: Path | None = None) -> dict[str, Any]:
    """Load the default or user-supplied JSON Schema."""
    path = schema_path or default_schema_path()
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest: Mapping[str, Any], schema_path: Path | None = None) -> None:
    """Validate a manifest and raise one readable error containing all violations."""
    schema = load_schema(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda error: list(error.path))
    if errors:
        details = "\n".join(
            f"- {'/'.join(str(item) for item in error.path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ManifestValidationError(f"Experiment manifest is invalid:\n{details}")


def validate_manifest_file(path: Path, schema_path: Path | None = None) -> None:
    """Load and validate one JSON experiment manifest without changing it."""
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ManifestValidationError(f"Invalid JSON in {path}: {error}") from error
    validate_manifest(manifest, schema_path)
