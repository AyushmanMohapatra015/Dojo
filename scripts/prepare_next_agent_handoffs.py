"""Create two immutable allowlisted handoffs; do not contact agents or run code."""

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARGON_TARGET = ROOT / 'docs/reviews/argon/frontend-refinement-packet-v1.md'
GRAVITY = ROOT / 'docs/reviews/Gravity'

ARGON_PROMPT = '''# Argon: refine the delivered frontend, exactly TWO task groups

Task 10a4; primary preparation 10a7. Read through END OF FRONTEND REFINEMENT PACKET.
This is a self-contained snapshot; no repository access or prior chat is needed.
Use the supplied implementation, not a replacement built from scratch.

## Current authority and ownership

Dojo is an Apache-2.0 repository-derived coding-agent evaluation/routing toolkit
for the NVIDIA x Nebius hackathon, Coding/Agentic Engineering track. Construction:
63 tasks (37 train/26 held-out), NOT evaluated model outcomes. Current application
checkpoint: 1,014 offline Python tests. ZERO real provider requests or measured
model costs/savings. Primary accepted the repaired offline statistics foundation;
primary now owns B cascade/report/CLI corrections 9g4e, then runner 5e.
You own the proposed dashboard refinement only. Agent 2 reviews your returned
revision later; Gravity separately studies scorer isolation. No overlapping edits.

The original Agent 2 assignment below is historical but its exact temporary
dojo-explorer-view-v1 schema remains binding. This section overrides its stale
test counts/ownership. The supplied primary assessment overrides optimistic
author claims. Dashboard code remains proposed, not installed or accepted.
No provider/store/Python/packaging/input-manifest changes, real-data schema,
account/tracing/billing activation, deployment, external uploads or Git writes.
No new UI frameworks, external assets/fonts/CDNs, telemetry, backend or login.

## Task group 1: parser and evidence correctness

Fix F1-F4 in explorer-primary-assessment-v1.md using the supplied code:
- Exact scorer/outcome/evidence matrix. Healthy candidate_error is unsolved;
  invalid_evidence is undetermined/invalid; infrastructure_error is
  undetermined/unknown. Refuse unsupported unverified candidate_error states.
- Reject duplicate object keys at every depth, including escape-equivalent
  keys. Preserve quoted delimiters/escapes and legitimate Unicode pairs.
- Validate numeric meaning before lossy Number conversion: reject a noninteger
  count/money that rounds to an integer, overflow and negative zero. Explicitly
  specify handling of mathematically integral decimal/exponent syntax; bound
  token/exponent work BEFORE BigInt construction, powers or allocation.
- Keep unresolved cells visible with their full denominator, but do not plot
  their config as an ordinary completed success/cost point. Provide a reason
  for blocked comparison without promoting evidence or zero-filling unknowns.

Preserve public data.js exports and exact v1 field names. Retain strict keys,
1 MiB, 10k rows/100 configs, depth32, all stated string bounds, one seed/task,
synthetic-only/no-real-calls/no-publication rules and exact unknown-cost policy.
Add independent acceptance cases at boundary values, escaped keys, pathological
numeric inputs, nested duplicates and cross-field contradictions. Use tiny
allocation/refusal sentinels instead of exhausting memory or output.

## Task group 2: UI reliability and verification readiness

Fix F5-F8: null costs last in BOTH sort directions, valid config ID 'all'
filterable without sentinel collisions, truthful local-network wording, and
coherent unknown/error/empty/loading/recovery behavior. Improve existing visual
hierarchy, responsive layout, chart/table correspondence, focus/labels/contrast
and detail selection. Preserve all synthetic labels and no ranking/savings.
This is a complete developer-facing demo, not an ornamental landing page.

Keep the existing React/Vite/Recharts stack. If tools are available, check
dependencies against primary official docs/registry, install project-locally
only after inspecting scripts, generate a lockfile from an ACTUAL install, run
real Vitest/RTL, Vite build and real Recharts in a browser. Otherwise mark these
UNEXECUTED/UNVERIFIED and provide exact primary commands; do not substitute a
custom test runner or chart stub and call it acceptance. No global installs,
hosted services, cloud APIs, API keys or real benchmark requests.
Bind dev/preview to 127.0.0.1 only. Verify production CSP and accessibility with
specific observed checks if tools allow it. Source scans alone are not proofs.

## Delivery contract

Return complete changed files with their original project-relative paths, plus
new helpers/tests only where necessary, a manifest of changed versus unchanged
files, F1-F8 disposition and an honest execution ledger in
docs/frontend-refinement-handoff-v1.md. Include exact known answers and any
unresolved decisions. Preserve original files that do not need changing.
Do not edit frozen CLI/packaging or invent a lockfile, test counts or screenshots.
The full baseline below is sufficient for these two groups; do not silently
invent other project APIs. State a missing dependency explicitly if necessary.

Finish a complete file before starting the next. Use four-backtick outer fences
for Markdown files containing triple fences. If output is running short, stop at
a file boundary and list remaining files, then continue in numbered parts when
asked. Do not write COMPLETE if delivery is partial. End a completed delivery:
END OF ARGON FRONTEND REFINEMENT V1.

Primary independently reviews/runs returned code before integration. The owner's
learning exercise, provider/financial gates and actual result claims remain open.
'''

GRAVITY_PROMPT = '''# Gravity follow-up: adversarial scorer design, exactly TWO tasks

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
'''

GRAVITY_SOURCES = (
    'dojo/eval/docker_scoring_v2.py', 'dojo/eval/candidate_outcomes.py',
    'dojo/eval/scoring_contract.py', 'dojo/solve/docker_sandbox.py',
    'dojo/solve/input_guard_v2.py', 'dojo/solve/patches.py',
    'dojo/backends/receipt_v2.py', 'dojo/backends/profiles.py',
    'docs/candidate-outcome-policy.md', 'docs/contract-docker-scoring.md',
    'docs/development-scoring.md', 'docs/model-controller-boundary.md',
    'docs/patch-export.md', 'docs/profiled-sandbox.md',
    'docs/reviews/gravity-primary-assessment-v1.md',
    'docs/reviews/principal-review-assessment-v1.md',
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as output:
        output.write(data)


def check():
    text = ARGON_TARGET.read_bytes().decode('utf-8')
    names = []
    fence = None
    for line in text.splitlines():
        if fence:
            if line == fence:
                fence = None
        elif re.fullmatch(r'`{4,}[a-z]+', line):
            fence = line[:line.index(next(char for char in line if char != '`'))]
        elif line.startswith('## FILE: '):
            names.append(line.removeprefix('## FILE: '))
    if fence or len(names) != 17 or len(set(names)) != 17:
        raise ValueError('Incomplete or duplicate outer reference blocks')
    if not text.endswith('END OF FRONTEND REFINEMENT PACKET\n'):
        raise ValueError('Missing packet end marker')
    manifest = json.loads((GRAVITY / 'context-manifest-v2.json').read_text(encoding='utf-8'))
    for row in manifest['files']:
        data = (GRAVITY / row['snapshot']).read_bytes()
        if len(data) != row['bytes'] or sha(data) != row['sha256']:
            raise ValueError('Gravity snapshot mismatch')
    if manifest['snapshot_id'] != sha(json.dumps(manifest['files'], sort_keys=True,
                                                separators=(',', ':')).encode()):
        raise ValueError('Gravity snapshot ID mismatch')
    print(json.dumps({'argon_outer_reference_files': len(names),
                      'gravity_verified_files': len(manifest['files']), 'valid': True}))


def main():
    targets = (ARGON_TARGET, GRAVITY / 'context-v2', GRAVITY / 'ASSIGNMENT-2.md',
               GRAVITY / 'context-manifest-v2.json')
    if any(path.exists() for path in targets):
        raise FileExistsError('Preserve shared handoffs; create a new version')
    base_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    proposal = ROOT / 'docs/reviews/agent2/proposals/explorer-v1'
    manifest = json.loads((proposal / 'intake-manifest.json').read_text(encoding='utf-8'))
    files = []
    for entry in manifest['files']:
        name = entry['path']
        data = (proposal / name).read_bytes()
        if sha(data) != entry['sha256']:
            raise ValueError('Frontend reference differs from its intake hash')
        files.append((name, data))
    files += [(name, (ROOT / name).read_bytes()) for name in (
        'docs/reviews/agent2/agent2-explorer-packet-v1.md',
        'docs/reviews/agent2/explorer-primary-assessment-v1.md',
        'docs/agent-handoff-quality.md',
    )]
    sections = [ARGON_PROMPT, (f'\nSnapshot base commit: `{base_commit}`; '
                'exact supplied working-tree bytes are identified below.\n'),
                '\n## Exact reference file manifest\n',
                '| Path | Bytes | SHA-256 |\n|---|---|---|\n']
    for name, data in files:
        sections.append(f'| {name} | {len(data)} | {sha(data)} |\n')
    for name, data in files:
        language = {'py': 'python', 'js': 'javascript', 'jsx': 'jsx', 'json': 'json',
                    'css': 'css', 'html': 'html', 'md': 'markdown'}.get(name.rsplit('.', 1)[-1], 'text')
        content = data.decode('utf-8')
        # Longer fence than any run in the embedded file avoids nested-fence loss.
        longest = max((len(run) for run in re.findall(r'`+', content)), default=0)
        fence = '`' * max(4, longest + 1)
        sections.append(f'\n## FILE: {name}\n\n{fence}{language}\n{content}\n{fence}\n')
    sections.append('\nEND OF FRONTEND REFINEMENT PACKET\n')
    gravity_files = [(name, (ROOT / name).read_bytes()) for name in GRAVITY_SOURCES]
    # Read every source before mutations so missing inputs cannot leave a half packet.
    write_new(ARGON_TARGET, ''.join(sections).encode('utf-8'))
    snapshot_rows = []
    for name, data in gravity_files:
        destination = GRAVITY / 'context-v2' / name
        write_new(destination, data)
        snapshot_rows.append({'source': name, 'snapshot': 'context-v2/' + name,
                              'bytes': len(data), 'sha256': sha(data)})
    gravity_manifest = {
        'base_commit': base_commit,
        'snapshot_date': '2026-10-22', 'purpose': '13l5/13l6 read-only scorer design',
        'files': snapshot_rows, 'provider_calls': 0, 'execution_authorized': False,
        'snapshot_id': sha(json.dumps(snapshot_rows, sort_keys=True,
                                      separators=(',', ':')).encode()),
    }
    write_new(GRAVITY / 'context-manifest-v2.json',
              (json.dumps(gravity_manifest, indent=2) + '\n').encode())
    write_new(GRAVITY / 'ASSIGNMENT-2.md', GRAVITY_PROMPT.encode())
    print(json.dumps({'argon_packet': str(ARGON_TARGET.relative_to(ROOT)),
                      'argon_reference_files': len(files),
                      'argon_packet_bytes': ARGON_TARGET.stat().st_size,
                      'gravity_context_files': len(snapshot_rows),
                      'gravity_context_bytes': sum(row['bytes'] for row in snapshot_rows),
                      'agents_contacted': False}, indent=2))


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        check()
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit('Use no arguments to create or --check to verify')
