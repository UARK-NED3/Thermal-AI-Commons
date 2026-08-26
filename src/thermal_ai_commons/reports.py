"""Machine-readable provenance records for reported Thermal AI results.

An evidence report records *what was claimed* alongside immutable references to
the data manifest, benchmark split, and released software components.  It does
not execute a model or establish scientific validity.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Mapping, Sequence


EVIDENCE_CLASSES = {"measured", "simulated", "derived", "synthetic", "mixed"}
CLAIM_STAGES = {
    "demonstration",
    "verification",
    "validation",
    "generalization",
    "deployment_readiness",
}
METRIC_REQUIRED_STAGES = {"validation", "generalization", "deployment_readiness"}


def sha256_file(path: Path) -> str:
    """Return a content digest without changing the referenced artifact."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


@dataclass(frozen=True)
class EvidenceReport:
    """A non-promotional record of a result and its reproducibility boundary."""

    report_version: str
    report_id: str
    task: str
    method: str
    physical_boundary: str
    evidence_class: str
    claim_stage: str
    manifest_sha256: str
    split_manifest_sha256: str
    components: Sequence[Mapping[str, object]]
    metrics: Mapping[str, float]
    calibration: Mapping[str, object]
    uncertainty: Mapping[str, object]
    failure_cases: Sequence[str]
    limitations: Sequence[str]

    def __post_init__(self) -> None:
        required_text = {
            "report_id": self.report_id,
            "task": self.task,
            "method": self.method,
            "physical_boundary": self.physical_boundary,
        }
        if any(not isinstance(value, str) or not value.strip() for value in required_text.values()):
            raise ValueError("report_id, task, method, and physical_boundary must be non-empty strings")
        if self.evidence_class not in EVIDENCE_CLASSES:
            raise ValueError(f"evidence_class must be one of {sorted(EVIDENCE_CLASSES)}")
        if self.claim_stage not in CLAIM_STAGES:
            raise ValueError(f"claim_stage must be one of {sorted(CLAIM_STAGES)}")
        if not all(isinstance(value, str) and len(value) == 64 for value in (self.manifest_sha256, self.split_manifest_sha256)):
            raise ValueError("manifest and split manifest must be SHA-256 digests")
        if not self.components:
            raise ValueError("at least one pinned component is required")
        for value in self.metrics.values():
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError("metrics must be finite numeric values")
        if self.claim_stage in METRIC_REQUIRED_STAGES and not self.metrics:
            raise ValueError(f"metrics are required for claim_stage={self.claim_stage}")
        for field_name, declaration in (("calibration", self.calibration), ("uncertainty", self.uncertainty)):
            if not isinstance(declaration.get("status"), str) or not declaration["status"].strip():
                raise ValueError(f"{field_name} must declare a non-empty status")
        for field_name, entries in (("failure_cases", self.failure_cases), ("limitations", self.limitations)):
            if not entries or any(not isinstance(entry, str) or not entry.strip() for entry in entries):
                raise ValueError(f"{field_name} must contain at least one non-empty statement")

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _pinned_components(component_ids: Sequence[object], registry_path: Path) -> list[Mapping[str, object]]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    by_id = {component["id"]: component for component in registry["components"]}
    if not component_ids or any(not isinstance(item, str) for item in component_ids):
        raise ValueError("component_ids must be a non-empty list of component IDs")
    unknown = sorted(set(component_ids) - set(by_id))
    if unknown:
        raise ValueError(f"component IDs not found in registry: {', '.join(unknown)}")
    return [by_id[component_id] for component_id in component_ids]


def create_evidence_report(
    report_input_path: Path,
    manifest_path: Path,
    split_manifest_path: Path,
    registry_path: Path,
) -> EvidenceReport:
    """Bind result declarations to immutable artifact content and release pins."""
    source = json.loads(report_input_path.read_text(encoding="utf-8"))
    components = _pinned_components(source.pop("component_ids", []), registry_path)
    return EvidenceReport(
        report_version="0.1.0",
        manifest_sha256=sha256_file(manifest_path),
        split_manifest_sha256=sha256_file(split_manifest_path),
        components=components,
        **source,
    )


def write_evidence_report(path: Path, report: EvidenceReport) -> None:
    """Write a stable JSON evidence record; callers retain the source artifacts."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.as_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
