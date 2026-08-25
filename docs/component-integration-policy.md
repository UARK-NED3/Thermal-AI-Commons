# Component Integration Policy

Thermal AI Commons integrates independently maintained projects through pinned
interfaces. It neither vendors component code nor follows a component's live
default branch.

## Two integration channels

| Channel | Reference | Permitted use |
| --- | --- | --- |
| Development | Exact commit on a named development branch | Adapter prototyping and non-archival testing |
| Released | Immutable release tag, commit, package version, and environment record | Cited results, benchmark reports, and Commons releases |

Every archived Commons result records its component identifier, repository,
release tag, commit SHA, package version, adapter version, input manifest, and
environment. Older reports are never re-run against a newer component without a
new report version.

## Current registry

`components/registry-v0.1.json` pins SeqReg `v0.1.0`, BubbleID `V0.0.9`, and
BubbleID-Flow `v0.1.0`. BubbleID-Flow has no declared repository license, so it
is catalogued only for metadata and compatibility planning; its code must not
be redistributed through Commons until the rights status changes.

## Upgrade workflow

1. A component maintainer publishes a release and changelog.
2. Commons opens a compatibility update with the new immutable reference.
3. Adapter, contract, baseline, and regression tests run against the candidate.
4. Review approves or rejects the compatibility update.
5. A new registry version and Commons report version are created when accepted.

No update may silently change a published benchmark result.
