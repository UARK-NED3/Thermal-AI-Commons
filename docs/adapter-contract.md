# Component Adapter Contract

An adapter wraps one immutable component release. It must declare the component
repository, release tag, full commit SHA, and package version through
`ComponentReference`.

Before execution, `validate_inputs` checks declared modalities, units, time
bases, and local input paths. The adapter must not modify raw inputs. It returns
an `AdapterResult` with one of three states:

- `success`: outputs and provenance were created;
- `abstained`: the input is out of the adapter's stated domain or has incomplete
  metadata; and
- `failed`: execution could not complete, with a recorded reason.

Adapters may not treat an abstention, missing metadata, or unsupported input as
a scientific prediction. They must preserve the component release identity in
every result report.
