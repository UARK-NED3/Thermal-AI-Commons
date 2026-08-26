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


def validate_quantitative_multimodal_profile(manifest: Mapping[str, Any]) -> None:
    """Require metadata needed before a quantitative multimodal claim.

    This profile validates declared metadata only. It does not validate sensor
    calibration, time alignment, or uncertainty against independent evidence.
    """
    validate_manifest(manifest)
    issues: list[str] = []
    modalities = manifest["modalities"]
    synchronization = manifest.get("synchronization")
    calibration = manifest.get("calibration")
    uncertainty = manifest.get("uncertainty")

    if not isinstance(synchronization, Mapping):
        issues.append("synchronization must be an object")
    else:
        reference_clock = synchronization.get("reference_clock")
        alignments = synchronization.get("alignments")
        if not isinstance(reference_clock, str) or not reference_clock.strip():
            issues.append("synchronization.reference_clock must be a non-empty string")
        if not isinstance(alignments, list):
            issues.append("synchronization.alignments must be a list")
        else:
            alignment_by_modality: dict[str, Mapping[str, Any]] = {}
            for index, alignment in enumerate(alignments):
                if not isinstance(alignment, Mapping):
                    issues.append(f"synchronization.alignments[{index}] must be an object")
                    continue
                modality = alignment.get("modality")
                if not isinstance(modality, str) or not modality:
                    issues.append(f"synchronization.alignments[{index}].modality is required")
                    continue
                alignment_by_modality[modality] = alignment
                for field_name in ("source_clock", "method", "status"):
                    if not isinstance(alignment.get(field_name), str) or not alignment[field_name].strip():
                        issues.append(
                            f"synchronization.alignments[{index}].{field_name} must be a non-empty string"
                        )
                residual = alignment.get("residual_std_s")
                if not isinstance(residual, (int, float)) or isinstance(residual, bool) or residual < 0:
                    issues.append(
                        f"synchronization.alignments[{index}].residual_std_s must be non-negative"
                    )
            for modality in modalities:
                name = modality["name"]
                if name not in alignment_by_modality:
                    issues.append(f"synchronization has no alignment record for modality {name!r}")

    for field_name, value in (("calibration", calibration), ("uncertainty", uncertainty)):
        if not isinstance(value, Mapping) or not isinstance(value.get("status"), str):
            issues.append(f"{field_name}.status must be declared for a quantitative multimodal profile")

    if issues:
        raise ManifestValidationError("Quantitative multimodal profile is incomplete:\n- " + "\n- ".join(issues))


def validate_manifest_file(
    path: Path, schema_path: Path | None = None, profile: str = "core"
) -> None:
    """Load and validate one JSON experiment manifest without changing it."""
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ManifestValidationError(f"Invalid JSON in {path}: {error}") from error
    validate_manifest(manifest, schema_path)
    if profile == "quantitative-multimodal":
        validate_quantitative_multimodal_profile(manifest)
    elif profile != "core":
        raise ManifestValidationError(f"Unknown validation profile: {profile}")
