import json

import pytest

from thermal_ai_commons.splits import make_group_split


def test_group_split_is_deterministic_and_has_no_group_overlap() -> None:
    groups = [f"run-{index:03d}" for index in range(1, 10)]
    first = make_group_split(groups, experiment_id="demo", group_unit="experiment_run", seed=42)
    second = make_group_split(reversed(groups), experiment_id="demo", group_unit="experiment_run", seed=42)

    assert first.assignments == second.assignments
    assert set(first.assignments) == set(groups)
    assert set(first.assignments.values()) == {"train", "validation", "test"}


def test_group_split_rejects_frame_level_leakage_unit() -> None:
    with pytest.raises(ValueError, match="prohibited"):
        make_group_split(["f1", "f2", "f3"], experiment_id="demo", group_unit="frame")


def test_group_split_rejects_too_few_independent_groups() -> None:
    with pytest.raises(ValueError, match="at least three"):
        make_group_split(["run-1", "run-2"], experiment_id="demo", group_unit="experiment_run")


def test_synthetic_group_list_has_required_fields() -> None:
    with open("examples/synthetic-groups.json", encoding="utf-8") as handle:
        document = json.load(handle)

    manifest = make_group_split(
        document["groups"], experiment_id=document["experiment_id"], group_unit=document["group_unit"]
    )
    assert manifest.experiment_id == document["experiment_id"]
