# Time Alignment Record

Each multimodal run declares one reference clock and one alignment record per
modality. The required mapping is:

```text
t_reference_s = t_source_s * (1 + drift_ppm * 1e-6) + offset_s
```

`residual_std_s` is the residual standard deviation after the stated alignment
method. It is not a substitute for a timing uncertainty budget, instrument
calibration, trigger verification, or spatial registration.

## Required record fields

| Field | Definition |
| --- | --- |
| `source_clock` | Clock used by the modality before alignment |
| `reference_clock` | Declared common clock for the run |
| `method` | Trigger, shared clock, cross-correlation, manual record, or another documented method |
| `offset_s` | Additive offset from source to reference time, in seconds |
| `drift_ppm` | Linear source-to-reference clock-rate correction, in parts per million |
| `residual_std_s` | Residual standard deviation after alignment, in seconds |
| `status` | Evidence state such as declared, measured, simulated, or illustrative_only |

The Commons records these inputs but cannot infer a physically valid alignment
from metadata alone. A result may only use a quantitative multimodal claim when
the alignment, calibration, and uncertainty evidence is documented for that
run.
