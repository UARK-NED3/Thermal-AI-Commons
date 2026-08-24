import json
from pathlib import Path

from thermal_ai_commons import SCHEMA_VERSION


ROOT = Path(__file__).resolve().parents[1]


def test_schema_and_example_use_current_version() -> None:
    schema = json.loads((ROOT / "schemas" / "experiment-manifest-v0.1.json").read_text())
    example = json.loads((ROOT / "examples" / "synthetic-experiment-manifest.json").read_text())

    assert schema["properties"]["schema_version"]["const"] == SCHEMA_VERSION
    assert example["schema_version"] == SCHEMA_VERSION


def test_example_has_required_top_level_fields() -> None:
    schema = json.loads((ROOT / "schemas" / "experiment-manifest-v0.1.json").read_text())
    example = json.loads((ROOT / "examples" / "synthetic-experiment-manifest.json").read_text())

    assert set(schema["required"]).issubset(example)
