# Gravity follow-up: adversarial scorer design, exactly TWO tasks

Tasks 13l5/13l6, supporting 4j/7e/7g. Read AGENTS.md and this assignment,
context-manifest-v2.json, then context-v2/ and the preserved prior reports.
This is a NEW bounded design assignment, not a request to repeat the old audit.

Current state: 1,014 offline application tests; 63 constructed tasks (37/26),
ZERO real provider calls or measured model outcomes. The accepted statistics
foundation is unrelated to your boundary assignment. Primary owns 9g4e/5e/5f;
Argon owns frontend refinement. Do not implement or duplicate those tasks.

Your first review correctly acknowledged same-interpreter pytest evasion, but
some contract/security advice was incorrect. Start with the primary assessment
in context-v2. In particular, a process split alone does not authenticate
evaluation, seccomp does not generally prevent Python object writes, Git
timestamps do not prove prior commitment, and hashes cannot establish origin.
Those corrections are constraints, not new defects to rediscover.

## Task 1 — concrete 4j decision/design

Write outputs/gravity-scorer-threat-model-v2.md. Define exact trusted/untrusted
actors, host/container/interpreter/process/filesystem/receipt boundaries and
assets for this repository. Trace the CURRENT candidate and collector call
sites. Use the supplied actual harness/source policies, not an invented service.

Compare (A) a narrowly stated cooperative-solver benchmark with known interpreter
evasion retained versus (B) a stronger, concretely enforceable evaluation design.
For B, explain how candidate code is invoked and how a test actually executes
without sharing attacker-controlled evaluator state. Address Python APIs/imports,
object identity, serialization, process ownership, files/descriptors, resource
limits, result authentication and cleanup. Do not assume arbitrary Python test
suites can transparently cross a process/RPC boundary. Identify unsupported tests,
performance/portability costs and exact new versioned modules/interfaces needed.
Reject designs whose claimed boundary does not withstand their own threat model.
Give a realistic recommendation for the remaining hackathon scope and truthful
public claims. A recommendation is NOT owner sign-off, production security or
permission to activate benchmark runs. Do not change frozen construction code.

## Task 2 — adversarial acceptance and falsification plan

Write outputs/gravity-scorer-acceptance-matrix-v2.md. For each supported claim,
specify a small fictional case, expected outcome, exact enforcement layer and
what evidence would falsify the claim. Cover pytest monkeypatches, import/path
shadowing, module/process-state manipulation, forged receipts, descriptor/shutdown
behavior, collector/image mismatches, patch/test-transfer integrity, timeout and
cleanup uncertainty. Distinguish already reproduced known cases, static inference,
new hypotheses and missing implementation. Preserve all unresolved cells; do not
turn integrity/infra failure into a convenient unsolved/omitted result.

Mark each proposed test as executable later against current APIs or dependent on
a named future interface. Favor behavioral tests over source-string/signature
checks. Do not execute payloads, host commands, Docker, Python, packages, network,
provider calls or Git. No credentials/real hidden tasks/reference fixes needed.
Optional pseudocode is design only; no implementation patch is requested.

Include a compact source/function/call-site ledger and checklist in these two
documents. Do not claim all sources were read or hashes verified unless they
were; hashes describe the supplied snapshot, not proof of your reading. Name
missing slices rather than following imports outside the review workspace.
Write only the two new outputs; preserve old reports and all context snapshots.
Stop at the two complete documents. END OF GRAVITY FOLLOW-UP V2.
