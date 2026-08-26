"""Deterministic group-level benchmark partitions with leakage safeguards."""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Mapping


FORBIDDEN_GROUP_UNITS = {"frame", "row", "window"}


@dataclass(frozen=True)
class GroupSplitManifest:
    """Immutable partition assignment for independently held-out groups."""

    split_version: str
    experiment_id: str
    group_unit: str
    seed: int
    assignments: Mapping[str, str]

    def __post_init__(self) -> None:
        if not self.experiment_id.strip() or not self.group_unit.strip():
            raise ValueError("experiment_id and group_unit must be non-empty")
        if self.group_unit.strip().lower() in FORBIDDEN_GROUP_UNITS:
            raise ValueError("frame-, row-, and window-level groups are prohibited for headline splits")
        expected = {"train", "validation", "test"}
        if len(self.assignments) < 3 or set(self.assignments.values()) != expected:
            raise ValueError("assignments must contain at least one train, validation, and test group")

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _allocation_counts(group_count: int, fractions: tuple[float, float, float]) -> tuple[int, int, int]:
    if group_count < 3:
        raise ValueError("at least three independent groups are required")
    if len(fractions) != 3 or any(value <= 0 for value in fractions):
        raise ValueError("train, validation, and test fractions must each be positive")
    total = sum(fractions)
    normalized = tuple(value / total for value in fractions)
    remaining = group_count - 3
    raw_extra = [remaining * value for value in normalized]
    counts = [1 + int(value) for value in raw_extra]
    for index in sorted(range(3), key=lambda item: (raw_extra[item] % 1, -item), reverse=True)[
        : group_count - sum(counts)
    ]:
        counts[index] += 1
    return tuple(counts)  # type: ignore[return-value]


def make_group_split(
    group_ids: Iterable[str],
    *,
    experiment_id: str,
    group_unit: str,
    seed: int = 0,
    fractions: tuple[float, float, float] = (0.7, 0.15, 0.15),
) -> GroupSplitManifest:
    """Assign independent groups to train, validation, and test partitions.

    Input order does not affect the result. A caller must choose a physical
    independence unit such as experiment run, surface, fluid, geometry, or
    operating trajectory; this function cannot establish independence itself.
    """
    groups = list(group_ids)
    if any(not isinstance(group, str) or not group.strip() for group in groups):
        raise ValueError("group IDs must be non-empty strings")
    unique_groups = sorted(set(groups))
    train_count, validation_count, _ = _allocation_counts(len(unique_groups), fractions)
    shuffled = unique_groups.copy()
    random.Random(seed).shuffle(shuffled)
    assignments = {
        group: "train" if index < train_count else "validation" if index < train_count + validation_count else "test"
        for index, group in enumerate(shuffled)
    }
    return GroupSplitManifest(
        split_version="0.1.0",
        experiment_id=experiment_id,
        group_unit=group_unit,
        seed=seed,
        assignments=dict(sorted(assignments.items())),
    )


def write_group_split_manifest(path: Path, manifest: GroupSplitManifest) -> None:
    """Write a deterministic JSON manifest; never alter source data."""
    path.write_text(json.dumps(manifest.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
