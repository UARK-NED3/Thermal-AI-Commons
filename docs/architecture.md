# Architecture

## Design principle

Thermal AI Commons is an interoperability layer. It does not merge the source
code, datasets, authorship, or release responsibilities of component projects.

```text
Experiment data and simulation outputs
             |
             v
Versioned manifest + rights/provenance record
             |
             v
Component adapters (optical | acoustic | sequence | thermal)
             |
             v
Fixed benchmark split + metrics + uncertainty checks
             |
             v
Traceable report and optional derived-data release
```

## v0.1 boundaries

- The repository contains no raw experiment data or trained weights.
- Adapters will call pinned, separately released component versions.
- A benchmark result is valid only for its documented task, data version,
  condition-level split, and uncertainty treatment.
- A model report must identify whether its evidence is measured, simulated,
  derived, synthetic, or mixed.
- A future agent may orchestrate approved tools and summarize their outputs; it
  cannot substitute for calibration, validation, or engineering review.

## Interfaces to implement next

1. `ExperimentManifest` reader/validator for the v0.1 schema.
2. Time-alignment interface that records reference clock, offset, and residual.
3. Adapter protocol for BubbleID-Flow and SeqReg.
4. Condition-group split generator.
5. Report object with metrics, calibration, and inspected failure cases.
