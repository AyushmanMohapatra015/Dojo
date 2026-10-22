# Defect-aware handoffs and chat continuity

Task 13m; primary research/checkpoint, 2026-10-22.
Use this with `web-agent-review-guide.md` and the live ACTION_PLAN, not instead
of an assignment packet. The following controls are based on reproduced project
defects and primary technical documentation; they do not establish a measured
Argon error rate or guarantee error-free output.

## Chat choice

Keep the current primary project chat while work is active. Repository files
preserve work across chats, but a new chat still needs a current handoff; it does
not automatically know the previous conversation. At a clean task boundary a
fresh primary chat is reasonable after saving PROGRESS/ACTION_PLAN and any
uncommitted changes. No reset, reclone, reinstall or Git write is needed.

For the next external web-agent assignment, prefer a fresh chat with one current
self-contained packet. Avoid attaching all historical deliveries. This is a
workflow judgment to reduce conflicting instructions, not proven lower token
cost for the unidentified Argon service. Attachments themselves consume context.
OpenAI documents compaction for long-running conversation context, but this does
not establish Argon's limits, billing or a guaranteed cheapest chat strategy:
[official compaction documentation](https://developers.openai.com/api/docs/guides/compaction).

When restarting the primary chat, use:

> Continue Dojo in D:\NVIDIA X NEBIUS. Read Rules.txt, ACTION_PLAN.md and the
> latest PROGRESS.md checkpoint first; inspect existing files and Git status.
> Primary next is 9g4b (A R1–R10), then 9g4e (B corrections/integration), then 5e.
> Read both Argon assessments and gravity-primary-assessment-v1.md before using
> proposals. Agent 2 owns frontend 10a2/10a3. Preserve frozen artifacts and owner
> exercise 16c. User performs Git writes. No live calls or paid usage authorized.
> Explain the next small step before changing anything.

## Observed defect → required check

| Pattern observed | Next assignment requirement |
|---|---|
| Ten-task overload, interruption, duplicate A labeled B, clipped CLI | At most two implementation groups; list exact files first, complete a file before starting another, use numbered parts and an explicit remaining-work ledger. Stop at a file boundary if output is running short. No repeated foundation rewrite. |
| Unverified references mistaken for accepted implementation | Label every source accepted/proposed/frozen; provide import/signature manifest, callers, locked dependency excerpts and exact baseline. Ask for AST/public-interface comparison and explicitly list any deviation. |
| Stale audit/hash trusted after record replacement | Test constructed/replaced public objects, not just JSON parser entry. Recompute structural validation and canonical bindings at consuming boundaries. |
| bool seeds, duplicate subsets, invalid metrics and series | Boundary matrix: exact types, uniqueness, out-of-range values, nulls, direct construction, cross-field invariants; include row permutation and hidden-outcome routing invariance. |
| Unicode false rejection | Pair equivalent UTF-8 and ASCII-escaped non-BMP JSON inputs; reject decoded lone surrogates, duplicate keys, non-finite numbers and excessive nesting separately. |
| Resource checks after allocation; family/pair costs omitted | Bound declared Cartesian products before expansion; count worst-case family occurrences, pairs, candidate selection, sensitivities and output. Include tiny cap tests and sentinels proving rejection before allocation/resampling. |
| Short numeric string with enormous exponent | Bound exponent and integer work before Fraction/Decimal/power construction on CLI, JSON, saved-artifact and direct API paths. Use a sentinel constructor, never allocate a huge number to demonstrate risk. |
| Wrong quantile and workload test answers | Give independent hand-calculated oracles with units, named method and exact rational answers. Test below/at/above bounds. A test expectation must be checked against the specification, even if agent code agrees with it. |
| Saved selection accepts a policy outside its candidate list | Cross-check selected policy/hash/evaluation, candidate membership, floor, tie rules, version and provenance. Separate internal consistency from trusted registration approval. |
| Blacklist described as whitelist; metadata described as authentication | Require an explicit output schema plus unknown-key/value-canary tests; name the trusted verifier and concrete evidence, not only a boolean/hash. |
| Passing tests only inspect text/signatures | Mark static checks separately. For behavioral claims use actual pure functions, fictional DBs, fake transports and independently derived expected effects. Report what each test cannot establish. |

Python's dataclass annotations do not generally validate field types, and frozen
dataclasses only emulate read-only attributes; they do not authenticate contained
data: [dataclasses documentation](https://docs.python.org/3/library/dataclasses.html).
Python also recommends limiting untrusted JSON size because parsing can consume
substantial resources: [JSON documentation](https://docs.python.org/3/library/json.html).
Input byte limits alone do not bound later Cartesian products or number expansion.

For quantiles, specify the method rather than guessing from two extrema. The
linear method uses the n−1 index convention (Hyndman–Fan type 7):
[NumPy quantile reference](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html).
Use exact hand-calculated Fractions as our oracle; no new NumPy dependency is
required. Organize boundary-case matrices with existing pytest parametrization:
[pytest documentation](https://docs.pytest.org/en/stable/how-to/parametrize.html).

## Prompt addendum for future packets

> Treat this packet's accepted/proposed/frozen labels as authoritative. Work only
> on the listed task IDs and exact deliverable files. Preserve supplied public
> interfaces and gates; explicitly justify every deviation. Before implementation,
> list input invariants, all allocation/work limits and mathematical oracles.
> Include direct-object mutation, bool/int, duplicate, Unicode, exponent,
> family/pair budget and saved-artifact consistency cases where relevant.
> Never claim a hash or metadata flag authenticates provenance. Use tiny resource
> caps and refusal sentinels; do not execute exhaustion payloads. Distinguish
> behavioral tests from source/signature checks. Return complete files with exact
> paths; use four-backtick outer Markdown fences when the file contains triple
> fences. End each file explicitly, then list delivered and remaining files.
> If code cannot be executed, write UNEXECUTED. Do not invent test counts or mark
> downstream integration complete. Use at most two task groups per delivery;
> checkpoint before the output limit instead of clipping a file.

Primary still reviews sources before execution, reproduces important findings,
keeps originals and records dispositions before adoption. Count incomplete
deliveries, interface mismatches, oracle errors and independently found defects
per reviewed batch; compare like scopes before claiming any error-rate reduction.
These are generated-artifact defects, not evidence of a bug in the Argon service.
