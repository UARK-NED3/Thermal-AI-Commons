import json
from pathlib import Path

import pytest

from thermal_ai_commons.reports import create_evidence_report, sha256_file


def test_evidence_report_binds_artifact_hashes_and_release_pins() -> None:
    report = create_evidence_report(
        report_input_path=Path("examples/synthetic-report-input.json"),
        manifest_path=Path("examples/synthetic-quantitative-multimodal-manifest.json"),
        split_manifest_path=Path("examples/synthetic-split-v0.1.json"),
        registry_path=Path("components/registry-v0.1.json"),
    )

    assert report.claim_stage == "demonstration"
    assert report.manifest_sha256 == sha256_file(Path("examples/synthetic-quantitative-multimodal-manifest.json"))
    assert report.split_manifest_sha256 == sha256_file(Path("examples/synthetic-split-v0.1.json"))
    assert [component["release_tag"] for component in report.components] == ["v0.1.0", "V0.0.9"]


def test_evidence_report_rejects_unknown_component(tmp_path) -> None:
    source = json.loads(open("examples/synthetic-report-input.json", encoding="utf-8").read())
    source["component_ids"] = ["not-a-registered-component"]
    report_input = tmp_path / "invalid-report-input.json"
    report_input.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(ValueError, match="not found"):
        create_evidence_report(
            report_input,
            Path("examples/synthetic-quantitative-multimodal-manifest.json"),
            Path("examples/synthetic-split-v0.1.json"),
            Path("components/registry-v0.1.json"),
        )


def test_validation_stage_requires_a_metric(tmp_path) -> None:
    source = json.loads(open("examples/synthetic-report-input.json", encoding="utf-8").read())
    source["claim_stage"] = "validation"
    report_input = tmp_path / "invalid-stage-report-input.json"
    report_input.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(ValueError, match="metrics are required"):
        create_evidence_report(
            report_input,
            Path("examples/synthetic-quantitative-multimodal-manifest.json"),
            Path("examples/synthetic-split-v0.1.json"),
            Path("components/registry-v0.1.json"),
        )
