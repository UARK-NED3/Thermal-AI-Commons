import json
from pathlib import Path

import pytest

from thermal_ai_commons import SCHEMA_VERSION
from thermal_ai_commons.contracts import ManifestValidationError, load_schema, validate_manifest


ROOT = Path(__file__).resolve().parents[1]


def test_schema_and_example_use_current_version() -> None:
    schema = json.loads((ROOT / "schemas" / "experiment-manifest-v0.1.json").read_text())
    example = json.loads((ROOT / "examples" / "synthetic-experiment-manifest.json").read_text())

    assert schema["properties"]["schema_version"]["const"] == SCHEMA_VERSION
    assert example["schema_version"] == SCHEMA_VERSION


def test_packaged_schema_matches_repository_schema() -> None:
    repository_schema = json.loads((ROOT / "schemas" / "experiment-manifest-v0.1.json").read_text())

    assert load_schema() == repository_schema


def test_example_has_required_top_level_fields() -> None:
    schema = json.loads((ROOT / "schemas" / "experiment-manifest-v0.1.json").read_text())
    example = json.loads((ROOT / "examples" / "synthetic-experiment-manifest.json").read_text())

    assert set(schema["required"]).issubset(example)


def test_validator_accepts_synthetic_example() -> None:
    example = json.loads((ROOT / "examples" / "synthetic-experiment-manifest.json").read_text())

    validate_manifest(example)


def test_validator_reports_missing_required_field() -> None:
    example = json.loads((ROOT / "examples" / "synthetic-experiment-manifest.json").read_text())
    del example["rights"]

    with pytest.raises(ManifestValidationError, match="rights"):
        validate_manifest(example)
