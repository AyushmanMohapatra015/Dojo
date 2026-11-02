# Offline cascade analysis and JSON reports

Task 9g4e; adapted from reviewed Argon Batch B sources. Archived originals remain
unchanged. This command reads local JSON and performs pure arithmetic; it does
not run an agent, score patches, invoke a provider, access billing or approve
publication. The frozen top-level construction CLI remains unchanged.

## Run the fictional example

From the project root, choose an output path that does not already exist:

```powershell
.venv\Scripts\python.exe -m dojo.bench.analyze --input tests/fixtures/analysis/valid_panel.json --output analysis-example.json --policy-file tests/fixtures/analysis/visible-tests-policy.json --bootstrap-replicates 20
```

The synthetic four-task fixture produces these exact point estimates:

| Series | Success | Expected one-attempt panel cost, nano-USD |
|---|---|---|
| A | 1/2 | 6,000,000 |
| B | 1/2 | 40,000,000 |
| A then B when visible tests are not true | 3/4 | 26,000,000 |

These are fictional known answers, not measured Nemotron results or provider
spending. The output remains `eligibility_status.status=UNVERIFIED` and
`publishable=false`, even if input rows claim real evidence or registration IDs.
Default bootstrap count is 10,000; the smaller example is for a quick smoke run.

## Routing and selection

A routing policy accepts only the exact ObservableSignals DTO. Hidden outcomes,
costs and scorer fields cannot be passed as that argument. A cold restart pays
A's cost plus B's mean cost on escalated A runs. B's result replaces A's result;
the calculation never ORs the two outcomes. Independent A/B sample averages
handle unequal seed counts without pretending additional provider calls occurred.

Use at most one policy mode:

- `--policy-file`: evaluate a specified observable policy.
- `--candidate-policies-file` with `--min-success-floor`: select on a complete
  train-only panel. The document has schema_version=1 and a candidates list.
- `--frozen-policy-file`: apply a saved `policy_selection` object without retuning.

Candidate selection minimizes expected total cost subject to the train success
floor, then higher success and lexicographically smaller policy hash. Saved
selections validate candidate membership, unique hashes, feasibility, versions,
canonical numeric metadata, selected evaluation and the exact winning rule.
No-feasible-policy is explicit and is not silently converted to a chosen policy.
The selected object is `report.policy_selection`; pass that object, not the whole
report, as a frozen-policy file. A caller can still fabricate internally
consistent metadata: these checks do not authenticate prior commitment, model
identity or Stage B approval. That remains 5f/7.

## Fail-closed input, workload and export

- Panel/audit/hash bindings are rechecked before analysis. Numeric thresholds
  are syntax/length/exponent bounded before Fraction construction; saved
  numerator/denominator integers are bounded before normalization. Huge exponent
  strings are rejected without constructing their represented huge numbers.
- Preflight sums primary/family bootstrap, pairwise comparisons, policy selection,
  cascade composition, metric scans and optional seed sensitivity. Family draws
  use worst-case expansion. Stored-point and estimated output-node budgets are
  checked before analysis; a blocked audit performs no metric/sampling work.
- JSON export uses explicit permitted object fields/types at every nested section,
  with no arbitrary metadata mapping. Unknown fields, private payload sections
  and forged publication flags fail. This is structural validation, not a way
  to determine whether an arbitrary permitted label contains a secret.
- Exports have a 250,000-node traversal budget and an 8 MiB serialized-byte limit.
  JSON is deterministic and finite, preserving exact fractions and explicit
  undefined reasons. Caller-selected indentation is bounded. Long valid source
  IDs receive deterministic hashed derived-series IDs; source IDs stay separate.
- Input/policy files are read with a MAX_INPUT_BYTES+1 bounded read. Output uses
  exclusive creation: an existing file or a race-created file is never overwritten.
  Errors print fixed codes rather than paths, raw JSON keys/values or tracebacks.

Every report is an unverified offline artifact. It is not the frontend's temporary
`dojo-explorer-view-v1` schema; a reviewed adapter/new data version is still needed.

## Status and exit codes

| Code | Meaning |
|---|---|
| 0 | Report written, including explicit success-only mode, or help printed |
| 1 | Invalid arguments/input/policy, workload/size refusal, output conflict or other error |
| 2 | Structurally parsed panel audit blocks a complete report |

`--write-blocked-report` writes an audit-only report on code 2; otherwise no output
is created. Missing cost blocks cost comparisons. `--allow-success-only` permits
an outcome-only summary when outcomes are valid; it never enables cost frontiers
or a cost-dependent cascade. Invalid/infrastructure outcomes are not dropped from
the panel to manufacture a better rate. A stale constructed envelope raises
AnalysisInputError before report assembly rather than receiving a new approval.

Verification: 26 adapted continuation tests plus 55 independent acceptance cases;
full application suite **1,095 passed in 55.75s**, Ruff clean. A separate real
`python -m dojo.bench.analyze` subprocess smoke produced the fictional 3/4 cascade,
26,000,000 nano-USD expected cost and non-publishable output. No provider calls.

Next: trusted runner/store/scorer wiring and product commands at 5e, then verified
registration/publication 5f/7 and separately authorized financial/live gates.
The owner's written math exercise 16c remains distinct from this implementation.

## Synthetic explorer projection (Part 1)

The reviewed `dojo.bench.explorer_export` and
`dojo.bench.sensitivity_diagnostics` pure APIs now provide exact multi-seed
projection and nonprimary leave-one-family-out diagnostics. See
[explorer v2 contract](explorer-v2-contract.md) for fields, examples, limits,
verification commands and source/adoption boundaries. These are synthetic-only;
frontend v1 does not consume v2. Bundle/verify/export CLI remains Part 2.
