# Group-Level Benchmark Splits

Headline benchmark results must hold out a physically independent group, not
individual frames, rows, or overlapping sequence windows. Typical group units
are experiment run, specimen/surface, fluid, pressure, geometry, facility, or
operating trajectory.

Generate a deterministic manifest from a reviewed group list:

```powershell
py -3.12 -m thermal_ai_commons.cli split examples/synthetic-groups.json `
  --out outputs/synthetic-split.json --seed 42
```

The input group list must document why the selected group unit is independent.
The generated manifest freezes the group-to-partition assignment. It does not
prove that groups are independent, representative, or sufficient for external
generalization.

Do not overwrite a split manifest after using it for a reported result; create
a new manifest version instead.
