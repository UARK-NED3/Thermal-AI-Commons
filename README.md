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

## Why a Commons?

The Commons connects independently maintained NED3 tools through shared
interfaces and evaluation rules. It does not replace them or claim ownership of
their source code, data, or release processes.

| Component | Role in the Commons |
| --- | --- |
| [BoilingLab](https://github.com/UARK-NED3/BoilingLab) | Experimental protocols, acquisition, and synchronization context |
| [BubbleID-Flow](https://github.com/UARK-NED3/BubbleID-Flow) | Optical flow-boiling analysis adapter target |
| [BubbleID-Workflow](https://github.com/UARK-NED3/BubbleID-Workflow) | Image-analysis workflow adapter target |
| [AELab](https://github.com/UARK-NED3/AELab) | Acoustic-emission sensing adapter target |
| [BoilingBench-Multimodal](https://github.com/UARK-NED3/BoilingBench-Multimodal) | Seed benchmark/data collaboration target |
| [FlowLab](https://github.com/UARK-NED3/FlowLab) | Cooling-loop experimental context |

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
currently exposes only the schema version and does not download or process
experimental data.

## Repository layout

```text
src/thermal_ai_commons/  Minimal shared Python API
schemas/                 Versioned machine-readable contracts
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

Citation metadata will be added at the first tagged release. Until then, cite
the specific component repository and associated paper or dataset actually used.

## License

Source code and documentation are released under the [MIT License](LICENSE).
Data, weights, and third-party components may have separate terms and are not
licensed by this repository unless stated in their own manifests.
