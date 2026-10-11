# Resource cards

Resource cards are versioned discovery and workflow-routing metadata for canonical NED3 resources. They give a future workflow navigator an auditable answer to four questions: what task a resource supports, what it needs, what it produces, and where its evidence stops.

They are not release certificates, reproducibility certificates, or permissions to copy code, data, weights, telemetry, or third-party artifacts.

## Registry rules

- Every card pins either a release tag or a commit snapshot and records the access date.
- A `commit_snapshot` is useful for discovery and maintenance review. It is not a substitute for an immutable released environment when producing a cited benchmark result.
- `evidence_ceiling` limits how a navigator may describe the card's output: metadata-only, screening, workflow, or model-evaluation-required.
- `not_supported` is mandatory. A router must surface it with any recommendation.
- The component registry remains the stricter source for evidence-report component pins. Resource cards do not silently add a component to a benchmark report.

## Use

```powershell
py -3.12 -m thermal_ai_commons.cli resources validate components/resource-cards-v0.1.json
py -3.12 -m thermal_ai_commons.cli resources list components/resource-cards-v0.1.json
```

The initial cards cover Commons infrastructure, data-center cooling discovery, OpenDC-LCA, CFDTwin, BoilingLab, and FlowLab. They are deliberately not a claim that all packages are mutually executable or that they share data rights.
