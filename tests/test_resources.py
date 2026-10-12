import json
from pathlib import Path

import pytest

from thermal_ai_commons.resources import (
    ResourceCardValidationError,
    ResourceManifestValidationError,
    load_resource_manifest,
    load_resource_registry,
    resource_cards_for_task,
    validate_resource_registry,
    validate_resource_manifest,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "components" / "resource-cards-v0.1.json"
MANIFEST = ROOT / "examples" / "ned3-resource-manifest-v0.1.example.json"
COMMONS_MANIFEST = ROOT / ".ned3" / "resource-manifest-v0.1.json"


def test_resource_cards_validate_and_cover_the_initial_portfolio() -> None:
    registry = load_resource_registry(REGISTRY)

    assert [card["id"] for card in registry["cards"]] == [
        "thermal-ai-commons",
        "data-center-cooling-research-tools",
        "opendc-lca",
        "cfdtwin",
        "boilinglab",
        "flowlab",
    ]
    assert registry["cards"][2]["evidence_ceiling"] == "screening"
    assert "not a local run" in registry["cards"][1]["not_supported"]


def test_resource_cards_reject_duplicate_identifiers() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["cards"][1]["id"] = registry["cards"][0]["id"]

    with pytest.raises(ResourceCardValidationError, match="duplicate card id"):
        validate_resource_registry(registry)


def test_exact_task_lookup_preserves_evidence_boundaries() -> None:
    registry = load_resource_registry(REGISTRY)

    cards = resource_cards_for_task(registry, "screen cooling life-cycle scenarios")

    assert [card["id"] for card in cards] == ["opendc-lca"]
    assert "ISO-conformant" in cards[0]["not_supported"]


def test_resource_manifest_example_validates_with_explicit_boundaries() -> None:
    manifest = load_resource_manifest(MANIFEST)

    assert manifest["evidence"]["ceiling"] == "screening"
    assert manifest["lifecycle"]["maintainer_review"] == "pending"


def test_resource_manifest_default_schema_is_packaged() -> None:
    schema_path = ROOT / "src" / "thermal_ai_commons" / "_schemas" / "resource-manifest-v0.1.json"

    assert schema_path.is_file()
    assert json.loads(schema_path.read_text(encoding="utf-8")) == json.loads(
        (ROOT / "schemas" / "resource-manifest-v0.1.json").read_text(encoding="utf-8")
    )


def test_resource_manifest_requires_a_non_use_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    del manifest["intended_use"]["not_intended_for"]

    with pytest.raises(ResourceManifestValidationError, match="not_intended_for"):
        validate_resource_manifest(manifest)


def test_commons_uses_its_own_reviewed_manifest() -> None:
    manifest = load_resource_manifest(COMMONS_MANIFEST)

    assert manifest["resource"]["id"] == "thermal-ai-commons"
    assert manifest["lifecycle"]["maintainer_review"] == "reviewed"
    assert manifest["evidence"]["ceiling"] == "metadata_only"
