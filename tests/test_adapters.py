from pathlib import Path

import pytest

from thermal_ai_commons.adapters import AdapterResult, ComponentAdapter, ComponentReference


def component() -> ComponentReference:
    return ComponentReference(
        component_id="synthetic",
        repository="https://example.invalid/synthetic",
        release_tag="v0.1.0",
        commit="a" * 40,
        package_version="0.1.0",
    )


def test_adapter_result_requires_explicit_failure_state() -> None:
    result = AdapterResult(
        status="abstained",
        component=component(),
        failure_reason="synthetic fixture has no declared calibration",
    )

    assert result.status == "abstained"
    assert not result.output_paths
    assert isinstance(result, AdapterResult)


def test_adapter_result_rejects_success_with_failure_reason() -> None:
    with pytest.raises(ValueError, match="successful"):
        AdapterResult(status="success", component=component(), failure_reason="not applicable")


def test_component_adapter_protocol_is_runtime_checkable() -> None:
    class SyntheticAdapter:
        component = component()

        def validate_inputs(self, manifest: dict[str, object], input_paths: dict[str, Path]) -> None:
            return None

        def run(self, manifest: dict[str, object], input_paths: dict[str, Path]) -> AdapterResult:
            return AdapterResult(status="success", component=self.component)

    assert isinstance(SyntheticAdapter(), ComponentAdapter)
