"""Stable interfaces for Thermal AI Commons component adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Protocol, Sequence, runtime_checkable


@dataclass(frozen=True)
class ComponentReference:
    """Immutable identity of a component used by one Commons run."""

    component_id: str
    repository: str
    release_tag: str
    commit: str
    package_version: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.component_id,
                self.repository,
                self.release_tag,
                self.commit,
                self.package_version,
            )
        ):
            raise ValueError("component references require non-empty immutable identifiers")
        if len(self.commit) != 40:
            raise ValueError("commit must be a full 40-character Git SHA")


@dataclass(frozen=True)
class AdapterResult:
    """Traceable result returned by a component adapter.

    ``status`` is one of ``success``, ``abstained``, or ``failed``. An adapter
    must not represent an unsupported modality or out-of-domain input as a
    successful scientific inference.
    """

    status: str
    component: ComponentReference
    output_paths: Mapping[str, Path] = field(default_factory=dict)
    metrics: Mapping[str, float] = field(default_factory=dict)
    warnings: Sequence[str] = ()
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if self.status not in {"success", "abstained", "failed"}:
            raise ValueError("status must be success, abstained, or failed")
        if self.status == "success" and self.failure_reason:
            raise ValueError("a successful adapter result cannot include a failure reason")
        if self.status in {"abstained", "failed"} and not self.failure_reason:
            raise ValueError("abstained and failed results require a failure reason")


@runtime_checkable
class ComponentAdapter(Protocol):
    """Protocol implemented by an adapter around a pinned component release."""

    component: ComponentReference

    def validate_inputs(self, manifest: Mapping[str, object], input_paths: Mapping[str, Path]) -> None:
        """Raise a clear error if the declared inputs are incompatible."""

    def run(self, manifest: Mapping[str, object], input_paths: Mapping[str, Path]) -> AdapterResult:
        """Run the component without mutating raw inputs and return traceable outputs."""
