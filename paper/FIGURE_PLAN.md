# Figure plan — BoilingBench-Multimodal and Thermal AI Commons paper

The following figures are required for an impactful benchmark paper. Figures marked **required before submission** need measured or independently verified inputs; they should not be populated with illustrative values.

1. **Ecosystem architecture and provenance flow (required before submission).** Show BoilingBench → manifest/rights/time alignment → BoilingLab/BubbleID/BubbleID-Flow adapters → SeqReg or other models → split-aware evidence report. Distinguish measured, derived, annotated, and inferred products.
2. **Dataset-family overview matrix (required before submission).** Seven tracks × modalities × physical conditions × acquisition rates × raw/processed products × data profile availability. Use icons or a compact matrix rather than a dense paragraph.
3. **Representative synchronized episode (required before submission).** A multi-panel time-aligned view of temperature, pressure/power, hydrophone/microphone/AE features, image-derived bubble or vapor-area features, and declared target. Include clock offsets and missingness.
4. **Data lineage and file/profile diagram (required before submission).** Full archive, Lite profile, omitted `.cine` files, processed exports, manifests, checksums, Hugging Face endpoint, and Zenodo snapshot.
5. **Benchmark task and split diagram (required before submission).** Show random-window versus run/condition-held-out splits and explicitly illustrate the leakage avoided by grouped temporal splitting.
6. **Baseline performance matrix (required before submission).** Heat map or dot plot of model × task × split, with MAE/RMSE/$R^2$ and confidence intervals. Report independent-run counts beside each score.
7. **Modality-ablation and missing-modality results (required before submission).** Compare thermal-only, acoustic-only, optical-only, multimodal, and degraded/missing-channel settings.
8. **Cross-domain generalization results (required before submission).** Hold out pressure/regime, surface geometry (flat Cu versus Cu foam), acquisition configuration, or dataset. Show in-domain versus transfer performance.
9. **Uncertainty and failure analysis (required before submission).** Reliability diagrams, prediction intervals, out-of-domain examples, and representative failure cases tied to quality flags or synchronization uncertainty.
10. **Reference reproducibility result (recommended).** A compact diagram or table showing the exact release tuple, hashes, environment, runtime, and regenerated outputs for the reference pipeline.
11. **Optional benchmark leaderboard figure (only after governance).** Include only if a documented submission protocol, hidden test policy, and versioned evaluation server or curator process exist.

## Figure rules

- Every quantitative panel must state the unit, split, number of independent runs, and target evidence class.
- Do not use random-frame splits as the headline result.
- Keep human annotations, derived labels, and model predictions visually distinct.
- Include uncertainty or variability, not only point estimates.
- Preserve a script and machine-readable source table for every figure.
