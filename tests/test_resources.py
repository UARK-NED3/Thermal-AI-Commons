import json
from pathlib import Path

import pytest

from thermal_ai_commons.resources import (
    ResourceCardValidationError,
    load_resource_registry,
    resource_cards_for_task,
    validate_resource_registry,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "components" / "resource-cards-v0.1.json"


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
