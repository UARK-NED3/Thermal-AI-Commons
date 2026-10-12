"""Validation and lookup utilities for the Commons resource-card registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator


class ResourceCardValidationError(ValueError):
    """Raised when resource-card metadata is incomplete or internally inconsistent."""


class ResourceManifestValidationError(ValueError):
    """Raised when repository-owned resource metadata is incomplete or inconsistent."""


def default_resource_card_schema_path() -> Path:
    return Path(__file__).resolve().parents[2] / "schemas" / "resource-card-registry-v0.1.json"


def default_resource_manifest_schema_path() -> Path:
    return Path(__file__).resolve().parent / "_schemas" / "resource-manifest-v0.1.json"


def validate_resource_manifest(manifest: Mapping[str, Any], schema_path: Path | None = None) -> None:
    """Validate a repository-owned resource manifest; no scientific claim is certified."""
    schema = json.loads((schema_path or default_resource_manifest_schema_path()).read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda error: list(error.path))
    if errors:
        details = [
            f"{'/'.join(str(item) for item in error.path) or '<root>'}: {error.message}"
            for error in errors
        ]
        raise ResourceManifestValidationError("Resource manifest is invalid:\n- " + "\n- ".join(details))


def load_resource_manifest(path: str | Path) -> dict[str, Any]:
    """Load and structurally validate a repository-owned resource manifest."""
    manifest_path = Path(path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_resource_manifest(manifest)
    return manifest


def validate_resource_registry(registry: Mapping[str, Any], schema_path: Path | None = None) -> None:
    """Validate registry shape and enforce unique resource identifiers."""
    schema = json.loads((schema_path or default_resource_card_schema_path()).read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(registry), key=lambda error: list(error.path))
    details = [
        f"{'/'.join(str(item) for item in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]
    cards = registry.get("cards", [])
    if isinstance(cards, list):
        card_ids = [card.get("id") for card in cards if isinstance(card, Mapping)]
        duplicates = sorted({card_id for card_id in card_ids if card_ids.count(card_id) > 1})
        if duplicates:
            details.append(f"duplicate card id(s): {', '.join(str(card_id) for card_id in duplicates)}")
    if details:
        raise ResourceCardValidationError("Resource-card registry is invalid:\n- " + "\n- ".join(details))


def load_resource_registry(path: str | Path) -> dict[str, Any]:
    registry_path = Path(path)
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    validate_resource_registry(registry)
    return registry


def resource_cards_for_task(registry: Mapping[str, Any], task: str) -> list[dict[str, Any]]:
    """Return cards that declare an exact supported task, in registry order."""
    return [
        dict(card)
        for card in registry["cards"]
        if task in card["supported_tasks"]
    ]
