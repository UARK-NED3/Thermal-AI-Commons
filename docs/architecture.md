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

## Implemented in the current development version

1. `thermal-ai-commons validate` validates JSON experiment manifests against
   the packaged v0.1 contract without changing the referenced data.
2. The component registry pins released SeqReg, BubbleID, and BubbleID-Flow
   versions with their rights status.
3. `TimeAlignmentRecord` stores an explicit source-to-reference-clock mapping
   and residual timing metadata without inferring sensor alignment.
4. The adapter contract distinguishes successful, abstained, and failed runs.
5. The split generator creates immutable train/validation/test assignments by
   declared independent group and rejects frame-, row-, and window-level groups.

## Next interfaces

1. Concrete adapters for released SeqReg and BubbleID using rights-cleared
   synthetic fixtures.
2. Report object with metrics, calibration, and inspected failure cases.
