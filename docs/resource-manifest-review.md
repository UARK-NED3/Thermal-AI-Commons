# Resource-manifest review gate

This checklist is the maintainer review that may change a public repository's
manifest from `pending` to `reviewed`. Schema validation alone checks metadata
shape; it does not establish that the statements, repository reference, or
reuse boundaries are correct.

## Review record

For the repository and commit named in `canonical_repository`, a designated
maintainer should record the review date and evidence in that repository's
issue, pull request, release notes, or manifest update. Do not mark a
collaborator-owned repository as reviewed from the Commons alone.

## Checklist

1. Confirm canonical ownership, default branch, and pinned commit reference.
2. Confirm the stated users, supported tasks, inputs, outputs, and explicit
   non-use match the checked repository state.
3. Confirm that the evidence ceiling and validation status do not overstate
   available data, tests, calibration, model evaluation, or independent
   validation.
4. Confirm license, data-rights, citation, and third-party dependency claims
   against the repository and applicable project records. Retain
   `verify_before_reuse` or `not_declared` when no authoritative declaration
   is available.
5. Run the documented minimal verification command when an execution path is
   claimed, and record unavailable dependencies or unrun checks.
6. Confirm that no private, licensed, sponsor-restricted, or collaborator
   sensitive content will be exposed by a public registry entry.

## Decision

Mark `lifecycle.maintainer_review` as `reviewed` only when every applicable
item above has been checked. Leave it `pending` when evidence is incomplete,
and use `not_reviewed` when a maintainer decides not to endorse the metadata.
Only public manifests marked `reviewed` are eligible for a public Commons
registry entry.
