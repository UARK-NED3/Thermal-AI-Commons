# Evidence reports

An evidence report is a machine-readable record for a reported result. It
binds the claim to the exact SHA-256 contents of the experiment manifest and
split manifest, plus immutable entries from the component registry. It is
intended for figures, tables, benchmark runs, and manuscript supplements.

The report contains the task, method, physical boundary, evidence class,
claim stage, named metrics, calibration and uncertainty declarations, known
failure cases, and limitations. It creates provenance; it does **not** execute
components, check physical independence, verify metrics, or promote a claim to
a higher evidence stage.

Claim stages are deliberately separate:

- `demonstration`: a workflow or interface has been exercised;
- `verification`: implementation behavior has been checked against a specified
  requirement or reference;
- `validation`: a stated model task has been tested against a relevant measured
  target and protocol;
- `generalization`: validation has been extended to independently held-out
  conditions; and
- `deployment_readiness`: operational suitability has been evaluated under a
  stated use boundary.

`validation`, `generalization`, and `deployment_readiness` require at least one
numeric metric in the report, but that structural rule is not evidence that the
metric is correct or adequate. Every report must explicitly state at least one
failure case and one limitation.

Create an evidence report without modifying the source artifacts:

```powershell
py -3.12 -m thermal_ai_commons.cli report `
  --input examples/synthetic-report-input.json `
  --manifest examples/synthetic-quantitative-multimodal-manifest.json `
  --split examples/synthetic-split-v0.1.json `
  --out $env:TEMP\thermal-ai-commons-evidence-report.json
```

The included synthetic example is only a provenance demonstration. It does not
perform model inference or establish any thermal, multimodal, or engineering
claim.
