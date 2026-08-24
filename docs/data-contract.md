# Data Contract v0.1

The machine-readable contract is
[`experiment-manifest-v0.1.json`](../schemas/experiment-manifest-v0.1.json).
Every submitted run must include a manifest separate from the raw files.

## Required fields

| Field | Meaning |
| --- | --- |
| `schema_version` | Contract version; currently `0.1.0` |
| `experiment_id` | Stable non-sensitive experiment identifier |
| `evidence_class` | Measured, simulated, derived, synthetic, or mixed |
| `modalities` | Signal types, units, time bases, access level, and sampling where applicable |
| `rights` | Owner, redistribution decision, and review state |

## Required before quantitative multimodal claims

Record synchronization reference, offset/registration procedure, residual
uncertainty, sensor calibration, and operating-condition definitions. Missing
information must remain marked as unavailable; it cannot be silently inferred.

## Data access classes

- **public:** cleared for the stated public release.
- **controlled:** access requires an approved process.
- **private:** retained by the owner; not redistributed.
- **not_released:** data exist but have no approved access route.

Raw files remain immutable. Processed and derived artifacts must record the
source manifest, code version, environment, parameters, and output checksum.
