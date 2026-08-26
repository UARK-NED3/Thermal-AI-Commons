"""Explicit time-base alignment records for multimodal experiments.

This module stores declared alignment parameters; it does not infer a physical
alignment from unverified sensor signals.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class TimeAlignmentRecord:
    """Map a source clock to a reference clock.

    The convention is ``t_reference_s = t_source_s * (1 + drift_ppm * 1e-6)
    + offset_s``. ``residual_std_s`` is the standard deviation of residuals
    after the stated alignment method, not a claim of absolute timing accuracy.
    """

    source_clock: str
    reference_clock: str
    method: str
    offset_s: float
    residual_std_s: float
    drift_ppm: float = 0.0
    status: str = "declared"

    def __post_init__(self) -> None:
        if not self.source_clock.strip() or not self.reference_clock.strip():
            raise ValueError("source_clock and reference_clock must be non-empty")
        if not self.method.strip() or not self.status.strip():
            raise ValueError("method and status must be non-empty")
        for name, value in {
            "offset_s": self.offset_s,
            "residual_std_s": self.residual_std_s,
            "drift_ppm": self.drift_ppm,
        }.items():
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.residual_std_s < 0:
            raise ValueError("residual_std_s must be non-negative")

    def to_reference_time_s(self, source_time_s: float) -> float:
        """Convert one source-clock time to the declared reference clock."""
        if not isfinite(source_time_s):
            raise ValueError("source_time_s must be finite")
        return source_time_s * (1.0 + self.drift_ppm * 1e-6) + self.offset_s

    def transform(self, source_times_s: Iterable[float]) -> list[float]:
        """Convert an iterable without modifying the input sequence."""
        return [self.to_reference_time_s(value) for value in source_times_s]

    def as_dict(self) -> dict[str, str | float]:
        """Return a JSON-serializable alignment record."""
        return asdict(self)
