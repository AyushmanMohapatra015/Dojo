"""Build a self-contained, hash-checked read-only Agent 2 acceptance packet."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'docs/reviews/argon/proposals/frontend-refinement-v2'
TARGET = ROOT / 'docs/reviews/agent2/frontend-acceptance-packet-v1.md'
PROMPT = '''# Agent 2: independent acceptance review of Argon's actual revised frontend

Task 10a6. Read through END OF FRONTEND ACCEPTANCE PACKET. This single file
contains the full 15-file proposed revision, primary findings, original contract
and the primary independent Node probe. You do not need repository access or
prior conversation. Review the supplied code; do not review an imagined version.

Dojo benchmarks coding-agent configurations on repository-derived tasks, then
analyzes cost/success and cold-restart cascades. It targets the NVIDIA x Nebius
Coding/Agentic Engineering track. Current main application: 1,095 offline Python
tests; 63 constructed tasks (37 train/26 held-out). ZERO real provider calls or
measured model outcomes/cost/savings. Backend offline analysis is implemented,
but trusted runner/registration/real evidence remain gated. The temporary
frontend contract is dojo-explorer-view-v1, synthetic only. It is NOT the backend
analysis-report contract. The dashboard proposal is not installed or accepted.

Primary owns backend/runner/scorer and final acceptance. Argon completed its two
frontend refinement groups and is idle. Gravity's scorer review is a separate
workstream. You own independent review of this exact frontend revision, not a
parallel redesign. No provider/Python/storage/registration changes or invented
data adapters. No account/card/tracing activation, deployment, Git writes, API
calls, telemetry, external assets/fonts, service sign-ups or hidden task data.

Complete exactly two review groups:

1. Parser/evidence/arithmetic acceptance: independently assess F1-F4, numeric
   lexical scanner, duplicates at every depth including escaped equivalent keys,
   Unicode and JSON grammar/depth/size boundaries. Use an independent exact oracle
   rather than repeating implementation logic. Check all cross-field semantics,
   denominators, unknown vs zero money, no promotion of synthetic metadata, and
   clear bounded errors. Primary's 20 probes/90 matrix states/5,285 numeric cases
   are limited actual evidence; seek meaningful counterexamples, not repeated
   congratulatory checks. State attacker-controlled inputs and expected layers.
2. UI/tooling acceptance: F5-F8 plus upload races/recovery, dataset switches,
   filter IDs ('all', '*', 'cfg:all', Unicode), null-last sorts both directions,
   chart exclusion/table denominator agreement, exact money presentation,
   keyboard/focus/labels/responsiveness/CSP and honest local/hosted network copy.
   Assess the inherited first-200-row cap and inability to reach later details
   using just config/outcome filters. Inspect provided tests for actual failures
   and false-positive assertions. Prioritize coherent working demo behavior.

If you have no terminal/browser, do STATIC analysis and label all suggested
tests UNEXECUTED. Do not claim npm, Vitest/RTL, build, real Recharts, accessibility
or browser acceptance from a custom runner, chart stub or source reading.
If tools ARE available, inspect package scripts first; work only in an isolated
review folder, no global installs. Any actual project-local resolution/build
must report exact versions/commands/results and preserve evidence. No keys or
paid services are needed. Production CSP and runtime behavior require observed
checks, not only configuration strings. Web source checks are not local runs.

Deliver exactly TWO complete Markdown documents:
- outputs/agent2-frontend-acceptance-v1.md: prioritized findings with exact file/
  function/line evidence, before/after behavior, minimal fictional reproducer,
  expected vs observed (or inferred), classification confirmed/hypothesis/
  unverified, integration risk and F1-F8 dispositions. Include useful positive
  controls and the precise remaining acceptance gates. Do not invent findings.
- outputs/agent2-frontend-regressions-v1.md: proposed focused tests/minimal
  patches for confirmed defects only, exact known answers, executable-context
  requirements, browser checklist, honest execution ledger and files read.
  Code inside Markdown is welcome; no wholesale replacement files required.

Review first; do not make large code rewrites. If you find no defect in a
category, say what was checked and its limits. Respect the original schema and
all synthetic/privacy/financial gates. Hashes establish snapshot identity, not
correctness. Primary will independently review and run proposed changes.
Use FOUR or more backticks outside Markdown containing triple code fences.
Finish a complete document before the next; checkpoint at document boundaries
if interrupted. Never label a partial response complete. End full delivery with
END OF AGENT 2 FRONTEND ACCEPTANCE V1.
'''


def sha(data):
    return hashlib.sha256(data).hexdigest()


def references():
    manifest = json.loads((BASE / 'intake-manifest.json').read_text(encoding='utf-8'))
    files = []
    for row in manifest['files']:
        data = (BASE / row['path']).read_bytes()
        if sha(data) != row['sha256'] or len(data) != row['bytes']:
            raise ValueError('Proposal differs from reviewed snapshot')
        files.append((row['path'], data))
    for name in ('docs/reviews/argon/frontend-primary-assessment-v1.md',
                 'docs/reviews/agent2/agent2-explorer-packet-v1.md',
                 'docs/reviews/agent2/explorer-primary-assessment-v1.md',
                 'scripts/review_argon_frontend.mjs'):
        files.append((name, (ROOT / name).read_bytes()))
    return files


def main():
    files = references()
    sections = [PROMPT, '\n## Exact reference manifest\n\n',
                '| Path | Bytes | SHA-256 |\n|---|---|---|\n']
    for name, data in files:
        sections.append(f'| {name} | {len(data)} | {sha(data)} |\n')
    for name, data in files:
        content = data.decode('utf-8')
        longest = max((len(run) for run in re.findall(r'`+', content)), default=0)
        fence = '`' * max(4, longest + 1)
        language = {'js': 'javascript', 'mjs': 'javascript', 'jsx': 'jsx', 'json': 'json',
                    'css': 'css', 'html': 'html', 'md': 'markdown'}[name.rsplit('.', 1)[-1]]
        sections.append(f'\n## FILE: {name}\n\n{fence}{language}\n{content}\n{fence}\n')
    sections.append('\nEND OF FRONTEND ACCEPTANCE PACKET\n')
    expected = ''.join(sections).encode('utf-8')
    if sys.argv[1:] == ['--check']:
        if TARGET.read_bytes() != expected:
            raise ValueError('Packet differs from its exact reviewed references')
    elif not sys.argv[1:]:
        with TARGET.open('xb') as output:
            output.write(expected)
    else:
        raise SystemExit('Use no arguments to create or --check to verify')
    print(json.dumps({'reference_files': len(files), 'packet_bytes': len(expected),
                      'packet_sha256': sha(expected), 'valid': True, 'agents_contacted': False}))


if __name__ == '__main__':
    main()
