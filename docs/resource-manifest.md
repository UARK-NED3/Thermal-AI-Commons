# Repository-owned resource manifests

The NED3 resource manifest is a small, versioned record committed by the
canonical repository maintainer. It lets a portfolio index or future
investigator-supervised navigator answer what a resource is for, what it needs,
what it produces, and where its evidence and reuse boundaries stop.

It does not certify a result, a model, a release environment, data rights, or
permission to copy another repository. A public catalog entry is likewise not
an endorsement or validation of the underlying artifact.

## Placement and scope

Place the file at `.ned3/resource-manifest-v0.1.json` in the canonical
repository. Keep source code, data, issue history, contributors, and release
cadence in that repository; the Commons only validates and indexes declared
metadata. A collaborator-owned repository remains collaborator-owned.

Use one manifest per independently maintained repository. Do not use a parent
catalog manifest to make claims for third-party entries. If a value has not
been checked by the maintainer, use `unknown`, `pending`, `not_declared`, or
`verify_before_reuse` where the schema permits rather than guessing.

## Required decision boundaries

Every manifest records:

- a pinned repository reference and access date for the reviewed state;
- intended users, supported tasks, and at least one explicit non-use;
- inputs, outputs, and execution setting;
- an evidence ceiling, validation status, and limitations; and
- software-license, data-rights, and citation status.

`evidence.ceiling` is a routing constraint, not a quality score. For example,
`screening` may support a transparent scenario comparison but not a
facility-specific operational conclusion; `model_evaluation_required` requires
case-specific assessment before accuracy claims; and `workflow` documents how
an analysis is performed without independently validating its result.

## Validate

```powershell
py -3.12 -m thermal_ai_commons.cli resource-manifest validate `
  .ned3/resource-manifest-v0.1.json
```

Use the [example manifest](../examples/ned3-resource-manifest-v0.1.example.json)
as a structural starting point, then replace every illustrative value with
repository-specific evidence. Validation checks structure only. A maintainer
review and a runnable reproduction check remain separate portfolio-audit
steps.

## Portfolio adoption sequence

1. Inventory accessible repositories privately, including visibility and
   canonical ownership.
2. Add manifests first to public, maintained NED3 repositories where the
   maintainer can review the declared scope.
3. Index only reviewed public manifests in a public Commons registry.
4. Keep private, licensed, sponsor-restricted, and collaborator-sensitive
   inventory records out of public indexes unless their owners approve release.
5. Run one data-center and one multiphase vertical slice from declared inputs
   through an evidence report before allowing an AI navigator to recommend an
   end-to-end workflow.
