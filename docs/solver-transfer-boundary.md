# Solver transfer review (7e1)

This review covers the current offline, host-prepared cell. It does not approve
genuine provider execution or establish protection against hostile candidate
code in the scoring interpreter.

| Transfer | Current boundary | Remaining verification |
|---|---|---|
| Host task to solver | The pinned issue manifest and parent source archive produce a two-field `SolverInput` (`issue_text`, `source_archive`). `BoundPlan` holds the evaluator separately. The checked Click cell has a restored scoring archive that differs at one path from the solver archive. | Editorial review still matters: byte/hash checks cannot prove natural-language issue text has no semantic answer hints. |
| Initial provider request | The offline regression builds the same `ModelRequest` shape used by `runtime_bridge`: system policy and exact issue text only. The codec's message payload has those two messages; evaluator fields are absent. | Actual live dispatch remains locked. A real transport needs its own provenance and redaction checks. |
| Sandbox feedback | The bridge bounds output and checks message text against known hidden canary/test-node identifiers before subsequent model turns. Scoring runs after solver messages are fixed and does not append a scorer reply. | A substring guard is diagnostic, not a proof that arbitrary hidden content cannot leak through a malicious environment or candidate. Test with the approved real boundary later. |
| Doc search | `SolverIdentity.docsearch.enabled` is fixed false by construction and its type rejects true. | Re-review all retrieval content paths before enabling doc search. |
| Local traces | `TraceEvent` permits aggregate enums, timings and counters; the local sink is disabled by default. The event schema has no prompt, output, query, URL, patch or task-ID field. | Any future hosted LangSmith/Toloka/Tandem export needs a separate payload and consent review. |
| Private observations | The local journal can retain request/response hashes and scoring evidence for diagnostics; it is not a public report or proof of actual provider execution. | Define a verified execution protocol and public whitelist before promotion. |

The focused host-prepared regression is
`test_actual_solver_view_and_wire_request_exclude_evaluator`. It checks the
real pinned Click cell without a model, container, network or sponsor call.
Other repository profiles and genuine runtime traffic remain to be checked.
