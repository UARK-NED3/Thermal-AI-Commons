# NED3 Thermal AI Commons

[![CI](https://github.com/UARK-NED3/Thermal-AI-Commons/actions/workflows/ci.yml/badge.svg)](https://github.com/UARK-NED3/Thermal-AI-Commons/actions/workflows/ci.yml)

Open research infrastructure for trustworthy thermal AI: interoperable data
contracts, benchmark protocols, model adapters, and reproducible evaluation for
thermal-fluid and energy systems.

## Status

**Seed infrastructure (v0.1.0-dev).** This repository does not yet provide a
validated universal model, a field-ready diagnostic, a digital twin, or a
public benchmark dataset. No raw experimental, confidential, licensed, or
sponsor-restricted data are included.

## Flagship ecosystem

Thermal AI Commons is the NED³ flagship interoperability hub for AI-enabled
boiling and thermal-fluid research. It connects independent repositories while
preserving their authorship, issue history, licenses, and release cadence.

The canonical workflow is:

`BoilingBench-Multimodal → BoilingLab → BubbleID/BubbleID-Flow → SeqReg → Commons evidence report`

This is a versioned integration path, not a monorepo. See the
[ecosystem integration guide](docs/ecosystem.md) for component roles, release
pinning, and the minimum provenance recorded for a benchmark result.

## Why a Commons?

The Commons connects independently maintained NED3 tools through shared
interfaces and evaluation rules. It does not replace them or claim ownership of
their source code, data, or release processes.

| Component | Role in the Commons |
| --- | --- |
| [BoilingLab](https://github.com/UARK-NED3/BoilingLab) | Experimental protocols, acquisition, and synchronization context |
| [BubbleID-Flow](https://github.com/UARK-NED3/BubbleID-Flow) | Optical flow-boiling analysis adapter target |
| [BubbleID-Workflow](https://github.com/UARK-NED3/BubbleID-Workflow) | Image-analysis workflow adapter target |
| [BubbleID](https://github.com/cldunlap73/BubbleID) | Bubble segmentation, tracking, and interface-dynamics feature extraction |
| [SeqReg](https://github.com/cldunlap73/SeqReg) | Sequence-regression framework for temporal and multimodal prediction |
| [AELab](https://github.com/UARK-NED3/AELab) | Acoustic-emission sensing adapter target |
| [BoilingBench-Multimodal](https://github.com/UARK-NED3/BoilingBench-Multimodal) | Seed benchmark/data collaboration target |
| [FlowLab](https://github.com/UARK-NED3/FlowLab) | Cooling-loop experimental context |

The Commons supplies shared contracts and evaluation—not a claim that every
component is itself a validated heat-transfer model. BoilingLab is a
physics-aware processing and synchronization tool; BubbleID and BubbleID-Flow
are computer-vision feature extractors; SeqReg is a reusable temporal-learning
framework.

## Initial capabilities

The first development target is a reproducible multimodal boiling workflow:

1. validate experiment metadata and time-base declarations;
2. register optical, acoustic, and thermal modalities without altering raw data;
3. run adapters for independently released analysis tools;
4. evaluate fixed condition-level splits; and
5. generate a traceable report with uncertainty and failure cases.

See [architecture](docs/architecture.md), the [data contract](docs/data-contract.md),
and the [seed benchmark protocol](docs/benchmark-protocol.md).

## Quick start

```powershell
py -3.12 -m pip install -e ".[dev]"
py -3.12 -m pytest
```

Python 3.10 or later is required; the commands above use the supported Python
3.12 interpreter available in the NED3 development environment. The package
does not download or process experimental data.

Validate a manifest without changing its referenced data:

```powershell
py -3.12 -m thermal_ai_commons.cli validate examples/synthetic-experiment-manifest.json
```

For a data package intended to support a quantitative multimodal analysis,
require alignment, calibration, and uncertainty declarations as well:

```powershell
py -3.12 -m thermal_ai_commons.cli validate `
  examples/synthetic-quantitative-multimodal-manifest.json `
  --profile quantitative-multimodal
```

Released component references are listed in
[`components/registry-v0.1.json`](components/registry-v0.1.json). See the
[component integration policy](docs/component-integration-policy.md) for the
pinning and upgrade rules, the [time-alignment record](docs/time-alignment.md),
and the [adapter contract](docs/adapter-contract.md).

Generate a deterministic independent-group split manifest with
[`examples/synthetic-groups.json`](examples/synthetic-groups.json); see
[group-level benchmark splits](docs/group-splits.md) for leakage boundaries.

Create a machine-readable [evidence report](docs/evidence-reports.md) that
hashes the exact manifest and split, resolves pinned component releases, and
records the claim stage, uncertainty declaration, failure cases, and
limitations:

```powershell
py -3.12 -m thermal_ai_commons.cli report `
  --input examples/synthetic-report-input.json `
  --manifest examples/synthetic-quantitative-multimodal-manifest.json `
  --split examples/synthetic-split-v0.1.json `
  --out $env:TEMP\thermal-ai-commons-evidence-report.json
```

## Repository layout

```text
src/thermal_ai_commons/  Minimal shared Python API
schemas/                 Versioned machine-readable contracts
components/              Pinned external component registry
docs/                    Architecture, benchmark, and governance documents
examples/                Safe synthetic/example manifests only
tests/                   Contract smoke checks
```

## Data, rights, and contribution boundaries

Use the [data-rights manifest template](docs/data-rights-manifest-template.csv)
before linking or releasing any data, derived result, model weight, or external
tool. A public catalog or repository does not by itself establish redistribution
or training rights. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation

For the current infrastructure release, see [CITATION.cff](CITATION.cff). Cite
the specific dataset, software release, and associated paper actually used;
Commons integration does not replace component-level citation.

## License

Source code and documentation are released under the [MIT License](LICENSE).
Data, weights, and third-party components may have separate terms and are not
licensed by this repository unless stated in their own manifests.
