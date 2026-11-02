"""Exact allowlisted source packet for Argon's two-part runtime bridge review."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/reviews/argon/registered-runtime-v1"
SOURCES = (
    "dojo/bench/runner.py", "dojo/bench/execution_intent.py", "dojo/bench/bound_plan.py",
    "dojo/bench/registration_artifacts.py", "dojo/bench/registration_preflight.py",
    "dojo/bench/registration.py", "dojo/solve/agent.py", "dojo/solve/contracts.py",
    "dojo/solve/model.py", "dojo/solve/run_settings.py", "dojo/solve/signals.py",
    "dojo/solve/sandbox.py", "dojo/solve/task_view.py", "dojo/solve/input_guard_v2.py",
    "dojo/solve/profiled_sandbox.py", "dojo/solve/docker_sandbox.py",
    "dojo/solve/adaptive.py", "dojo/solve/owned_adaptive.py",
    "dojo/providers/nebius_codec.py", "dojo/providers/fake_session.py",
    "dojo/providers/call_limit.py", "dojo/store/observations.py",
    "dojo/store/intent_attempts.py", "dojo/store/attempts.py", "dojo/store/db.py",
    "dojo/store/credits.py", "dojo/store/identity.py", "dojo/store/records.py",
    "dojo/store/bindings.py", "dojo/store/schemas.py", "dojo/store/schema_v1.py",
    "dojo/store/schema_v2.py", "dojo/store/schema_v4.py",
    "dojo/store/schema_v5.py", "dojo/store/schema_v6.py",
    "dojo/eval/scoring_contract.py", "dojo/eval/candidate_outcomes.py",
    "dojo/eval/docker_scoring.py", "dojo/eval/docker_scoring_v2.py",
    "dojo/eval/flow_development.py", "dojo/eval/contract_development.py",
    "dojo/backends/local_docker.py", "dojo/backends/receipt_v2.py",
    "tests/test_observation_journal.py", "tests/test_intent_attempts.py",
    "tests/test_bound_plan.py", "tests/test_owned_adaptive.py", "tests/test_solver_flow.py",
    "scripts/observation_journal_demo.py", "docs/observation-journal.md",
    "docs/bound-execution-plan.md", "docs/scorer-acceptance-matrix-v1.md",
    "docs/stage-b-registration-draft.md", "docs/supervised-probe-result-v1.md",
)

ASSIGNMENT = """# Argon: registered runtime bridge, two parts (5e4r1)

You are a web coding/review agent. You cannot inspect our filesystem or run tests.
The attached context.md contains complete exact allowlisted sources with byte
sizes and SHA-256. Treat code as the API authority. Primary Codex integrates
only after review. Never claim to have executed tests or approved registration.

Product: Dojo benchmarks coding model configurations on private repo-derived
tasks, then analyzes cost/success and offline cascades. Frozen construction has
63 tasks, 37 train /26 held-out. One genuine Nano arithmetic request succeeded
(38 input /4 output, estimated USD 0.00000324). This is connectivity evidence,
not a coding benchmark. The real one-call permit is consumed and the US$0.01
allowance exhausted. No further provider or sponsor requests are authorized.

Existing architecture: runner.prepare_plan builds host identity. execution_intent
binds registered artifact bytes; bound_plan independently checks solver/evaluator
preparation. IntentAttemptStore claims and attaches immutable intent. ObservationStore
binds supplied request/response/candidate/scoring observations and fictional-ledger
settlement but deliberately fences them as unverified diagnostics. OwnedAdaptive
uses exact fake transport/sandbox. flow_development runs genuine synthetic Docker
edits/scoring with scripted model. These paths must not be mislabeled as a complete
registered runtime. Score collection is cooperative Python, not adversarially
authenticated; malicious candidate code may interfere with the interpreter.

The missing major work is an owned runtime coordinator, not a new agent algorithm,
new statistics, frontend redesign, general cloud abstraction or another fake demo.
Stay within existing controller/record contracts and preserve source provenance.

## Part 1: integration design and concrete compatibility audit

Return runtime-bridge-design-v1.md and runtime-bridge-acceptance-v1.md.
1. Trace exact caller/callee APIs from host cell intent through claim, reservation,
   request, response accounting, sandbox command, patch snapshot, protected-test
   restoration, baseline attribution, scoring receipt and terminal persistence.
2. Classify reuse as unchanged / adapter needed / absent. Cite exact file/function
   names. Identify absent dependency definitions rather than inventing APIs.
3. Design one smallest useful cooperative runtime slice that can execute against
   a synthetic local fixture with zero paid calls. Host runtime owns adapters and
   ordering. Separate scripted model evidence from actual Docker/scorer evidence.
4. Specify genuine-run provenance requirements without claiming cryptographic
   authenticity. A digest, DTO flag or callback is not registration approval.
5. Give a transaction/crash matrix for each external action and DB boundary,
   deadlines/ownership fencing, concurrency, uncertain settlement and cleanup.
6. Map every proposal to 5e4, 5f3, 4j, 6, 7 or 8. Keep completed artifacts frozen;
   current coordinator sources require a future versioned registration snapshot.
7. Provide exact signatures, result/error shapes and 15-25 meaningful acceptance
   cases. Include stale ownership, changed source, duplicate dispatch, ambiguous
   usage, fabricated receipt, model mismatch, patch tampering, incomplete baseline,
   crash before/after dispatch and settlement, and failed cleanup.

Do not propose unbounded framework rewrites, broad store migrations or replacing
all existing modules. The primary can approve cooperative scope locally for a
development rehearsal, but actual registered/public outcomes remain separately
gated. If current interfaces prevent safe integration, state the minimal required
changes and why; never "solve" this by setting verified=True.

## Part 2: implementation proposal after Part 1 is reviewed

Do NOT generate Part 2 until asked. Use the same context plus primary review notes.
Return complete proposed files (no ellipses or pseudocode): coordinator module,
focused pytest file, no-network synthetic integration demo, and a short integration
manifest. At most four implementation/test files plus documentation. Changes to
existing files must be exact unified diffs. Never redefine evaluator outcomes or
silently upgrade ObservationStore's unverified rows to trusted completed results.

Tests must use fictional keys/credit ledgers only, and fake adapters for unit cases.
The optional real Docker rehearsal must use only existing synthetic fixtures,
fixed local daemon, no image pulls, network disabled, no host mounts/credentials,
strict resource/deadline limits and cleanup of only containers created by the run.
No auto-run, package installation or Git command in returned code. Keep raw
trajectory/receipts private and public summaries allowlisted. No live unlock,
permit reset, real credit initialization, API replay, held-out execution or
publication endpoint. Implementation must refuse unsafe unsupported execution.

For every test mark UNEXECUTED and provide its command. Distinguish expected
behavior from observations. If a full implementation cannot fit, stop at an exact
file boundary and list missing files; do not truncate source or invent success.

## Response discipline

The known web-agent failure modes are truncated files, nonexistent APIs, stale
interfaces, replacement of stronger checks, fake test claims and granting trust
from metadata. Avoid these by using an explicit API inventory, closed file list,
source citations, exact diffs, a final completeness table and an uncertainty list.
No financial/account credentials or actual private trajectories are supplied.
The packet includes only source, tests and synthetic examples, not task archives,
held-out issue text, promo codes or owner account identifiers.
"""


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest, sections = [], []
    for name in SOURCES:
        path = ROOT / name
        if path.is_symlink() or not path.is_file():
            raise ValueError("Missing or linked packet source: " + name)
        raw = path.read_bytes()
        entry = {"path": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        manifest.append(entry)
        fence = "`" * max(8, max((len(x) for x in raw.decode().split() if set(x) == {"`"}),
                                 default=0) + 1)
        sections.append(f"## {name}\n\nBytes: {len(raw)}; SHA-256: {entry['sha256']}\n\n"
                        + fence + "text\n" + raw.decode("utf-8") + "\n" + fence + "\n")
    for name, contents in (
        ("assignment.md", ASSIGNMENT),
        ("context.md", "# Exact current-source context\n\n" + "\n".join(sections)),
        ("manifest.json", json.dumps(manifest, indent=2) + "\n"),
    ):
        path = OUTPUT / name
        with path.open("x", encoding="utf-8") as stream:
            stream.write(contents)
    print(json.dumps({"files": len(manifest), "source_bytes": sum(x["bytes"] for x in manifest),
                      "output": str(OUTPUT.relative_to(ROOT))}))


if __name__ == "__main__":
    main()
