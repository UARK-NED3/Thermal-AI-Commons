# NED³ Thermal AI ecosystem

Thermal AI Commons is the interoperability and evidence layer for a family of
independently maintained NED³ research repositories. The ecosystem is designed
for reproducible AI for boiling heat transfer while keeping data, software,
model, and archival responsibilities separate.

## Component roles

| Component | Scientific role | Integration boundary |
| --- | --- | --- |
| [BoilingBench-Multimodal](https://github.com/UARK-NED3/BoilingBench-Multimodal) | Versioned data, annotations, benchmark tasks, and leakage-safe splits | Commons consumes manifests and declared data revisions; it does not mirror raw data. |
| [BoilingLab](https://github.com/UARK-NED3/BoilingLab) | Acquisition context, clock synchronization, thermal reconstruction, heat flux, spectra, hysteresis, and exports | Commons consumes documented outputs and processing metadata; derived heat flux remains derived, not ground truth by default. |
| [BubbleID](https://github.com/cldunlap73/BubbleID) | Bubble detection, segmentation, tracking, and interface features | Commons consumes versioned image-derived tables or adapter outputs. |
| [BubbleID-Flow](https://github.com/UARK-NED3/BubbleID-Flow) | Vapor-area and flow-boiling image analysis | Commons requires a rights-cleared release before redistribution or automated packaging. |
| [SeqReg](https://github.com/cldunlap73/SeqReg) | Sequence-to-value and sequence-to-sequence regression | Commons records model configuration, training split, normalization, and evaluation outputs. |

## Reference release path

For a citable result, record a tuple containing:

```text
commons_registry_version
dataset_id + dataset_release_or_doi
processing_tool + release_tag + commit
feature_extractors + release_tag + commit
sequence_model + release_tag + commit
manifest_hash + split_hash + environment
```

Use immutable releases for published results. Development branches and moving
latest revisions are permitted for adapter prototyping only. A component update
requires a compatibility check, new registry version, and new evidence report;
it must never silently alter an earlier benchmark result.

## Reference workflow

1. Select a dataset profile and inspect its README, rights, units, calibration,
   and time-base declarations.
2. Run BoilingLab or another authorized processor and retain the processing
   version, parameters, quality flags, and derived-data status.
3. Run BubbleID/BubbleID-Flow only on the applicable image data and keep human
   annotations separate from predictions.
4. Build temporal features with SeqReg or another declared model, fitting
   normalization and feature selection on training runs only.
5. Evaluate run-, specimen-, condition-, or dataset-held-out splits, report
   uncertainty and failure cases, and generate a Commons evidence report.

## What the ecosystem does not claim

The linked repositories are not one software package, and integration does not
make their licenses interchangeable. A Commons report does not establish that
an inferred heat flux is independently measured, that a model generalizes to a
new geometry or facility, or that a random-window score is leakage-safe.
Calibration, physical applicability, rights, and external validation remain
component- and dataset-specific gates.
