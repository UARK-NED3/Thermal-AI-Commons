import pytest

from thermal_ai_commons.alignment import TimeAlignmentRecord


def test_alignment_maps_source_clock_to_reference_clock() -> None:
    record = TimeAlignmentRecord(
        source_clock="camera_s",
        reference_clock="daq_s",
        method="trigger",
        offset_s=0.003,
        drift_ppm=100.0,
        residual_std_s=0.0002,
        status="synthetic",
    )

    assert record.to_reference_time_s(10.0) == pytest.approx(10.004)
    assert record.transform([0.0, 1.0]) == pytest.approx([0.003, 1.0031])


def test_alignment_rejects_negative_residual_uncertainty() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        TimeAlignmentRecord(
            source_clock="camera_s",
            reference_clock="daq_s",
            method="trigger",
            offset_s=0.0,
            residual_std_s=-0.001,
        )
