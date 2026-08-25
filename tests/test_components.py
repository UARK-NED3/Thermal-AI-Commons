import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_component_registry_has_immutable_references() -> None:
    registry = json.loads((ROOT / "components" / "registry-v0.1.json").read_text())

    assert registry["registry_version"] == "0.1.0"
    assert {component["id"] for component in registry["components"]} == {
        "seqreg",
        "bubbleid",
        "bubbleid-flow",
    }
    for component in registry["components"]:
        assert component["release_tag"]
        assert len(component["commit"]) == 40
