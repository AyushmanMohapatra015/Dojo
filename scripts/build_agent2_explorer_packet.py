"""Fixed allowlist and fictional fixture for Agent 2's independent UI work."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'docs/reviews/agent2/agent2-explorer-packet-v1.md'
PROMPT = r'''# Agent 2: exactly TWO implementation tasks - static Dojo explorer

Read through END OF EXPLORER PACKET. This assignment requests COMPLETE FRONTEND
CODE, not another audit/storyboard. Your earlier documents were reviewed; the
primary assessment below corrects them. Do not implement provider/storage/math.

## Product/context/ownership

Dojo benchmarks coding configurations on repository-derived tasks, with separate
patch scoring and intended cost/success comparisons. Construction: 63 tasks
(37 train/26 held-out), NOT model results. Latest offline application checkpoint
879 tests. ZERO real model requests, ZERO measured model results/savings. Static
dashboard currently contains ONLY the README included below. Primary owns 5d2
storage; Argon/Agent 1 owns statistics (five tasks at once); Agent 3 unassigned.
You own dashboard/ frontend only. Do not require access to any private service.

## Task 1 - complete static results-explorer prototype (10a/10b/10d/10f)

Build Vite + React + Recharts with a small, coherent developer-facing experience.
This is the existing planned stack, not a request to deploy or enable paid APIs.
Use plain JavaScript/JSX and ordinary CSS; avoid extra UI/state/icon libraries.
No CDN, external font/image, telemetry, login, analytics, cloud SDK or backend.
All dependencies local to dashboard/package.json. Do not change root pyproject,
uv.lock, dojo/cli.py, bench/cascade/store/solver code or construction files.

Required screens/interactions in one small app:
- Persistent prominent SYNTHETIC UI FIXTURE / NOT MODEL RESULTS label. Show
  evidence_kind, eligibility, evaluated fixture task count, constructed task
  count separately, and explicit unavailable real runtime/usage. Do not imply
  the actual 63-task pool has been benchmarked. No logo implying certification.
- Configuration comparison cards/table plus accessible labeled cost/success
  chart using supplied display values. Success denominator and synthetic cost
  units visible; unknown CI/metrics shown as unavailable with reason, not 0.
  Do not compute a new frontier/CI/savings, rank a best model or fit a policy.
- Task/config grid with accessible sorting/filtering by config/outcome and
  a selected-row detail panel for SANITIZED fields only. Visible-test evidence
  is distinct from final correctness; a self-report is not an evaluator score.
- Method/limitations panel: synthetic demo, equal-task definition, n/seeds,
  unverified eligibility, pinned repositories, small samples, contamination,
  cold restart future work and scorer threat-model limitations.
- Responsive readable layouts for narrow/desktop screens; keyboard focus,
  semantic controls, labels, adequate contrast, non-color status cues and a
  tabular alternative to charts. Empty/invalid/error/loading states are real
  code paths, with friendly actionable wording and no raw private payload dump.
- Built-in fixture plus bounded local JSON upload for the view model below.
  Never execute/interpret input as JS/HTML/URLs; React text rendering only,
  no dangerouslySetInnerHTML, eval, pickle, imports or remote fetch from fields.
  Refuse files over 1 MiB and excessive rows/strings/nesting. Reject incompatible
  schema, unknown/private fields, nonfinite/negative values, unsafe integer
  money, duplicates and contradictory counts/statuses. Do not auto-accept real
  data/publication flags: this v1 prototype supports synthetic input ONLY.
  Add deterministic fixture variants/UI controls for empty and invalid inputs
  so verification is possible without rewriting source.

## Frozen temporary FRONTEND view-model boundary

The supplied JSON is dojo-explorer-view-v1. It is NOT Argon's input or report
schema. A future primary-reviewed trusted adapter will map actual analysis
output. Never guess Argon's signatures or import its modules. Keep all parsing
and mapping in dashboard/src/data.js. Preserve exact input key names/types.
The top-level required keys are exactly those in the JSON fixture. Config and
row required keys are exactly those in its objects; no additional arbitrary
private metadata is accepted. Allow displayed strings only within documented
bounds; IDs <=160 chars, text/reasons <=1000, <=10k rows, <=100 configs, depth32.
Require schema_version=1, evidence_kind=synthetic, eligibility=UNVERIFIED and
real_provider_calls=0. source_kind must be synthetic_ui_fixture. construction
counts are informational; evaluated_task_count comes from distinct fixture IDs.
config.task_count/solved_count/expected_total_cost_nano_usd must agree with its
one-seed rows in this v1; each task has one row per declared config, seed=0.
row.cost_nano_usd may be null only when the config cost is also unknown/null;
never substitute zero. Require numeric money to be nonnegative JS safe integers.
Rows use outcome solved/unsolved/undetermined and evaluator evidence
valid/invalid/unknown; solved requires valid/passed, unsolved valid/failed or
healthy-baseline candidate_error, undetermined corresponds to invalid_evidence
or infrastructure_error. supplied nullable visible_tests_pass is independent.
CI fields in this v1 are always null with a reason. No test accuracy inferred.
All cost numbers in this fictional fixture are hypothetical UI values, not
actual spending or measured provider cost. Format units clearly and exactly.

## Task 2 - UI verification and primary integration handoff

Deliver complete meaningful parser/component tests using a minimal local test
setup (Vitest + React Testing Library is acceptable). Verify valid fixture,
unknown/zero distinctions, duplicate/missing rows, count mismatches, hidden/private
extra fields, malicious markup as inert text, invalid sizes/inputs, keyboard
interaction/filter selection, persistent fixture label and empty/error states.
Provide a manual browser checklist for mobile/desktop, tab/focus, chart/table,
file upload/recovery and no remote-network calls. Do not claim browser/tests
executed if your environment cannot run them; give commands and expected checks.

## Complete source delivery map

dashboard/package.json, dashboard/index.html, dashboard/vite.config.js,
dashboard/src/main.jsx, App.jsx, styles.css, data.js,
dashboard/src/fixtures/synthetic.json, relevant test files/setup under dashboard/,
dashboard/README.md and docs/explorer-integration.md.
Add files only if needed and list every complete path in a manifest. No missing
helpers, ellipses, fake screenshots or precomputed claimed test logs. Do not
invent a lockfile: include one only if generated by an actual dependency install.
Pin a mutually compatible dependency set; verify versions against official
package documentation if available and record what was checked, otherwise flag
dependency resolution UNVERIFIED for the primary. No global installations.
Use scripts for local dev, build, test and preview; bind local commands to
127.0.0.1, not all interfaces. Public hosting, uploads and account actions are
not authorized. No API key or provider endpoint belongs in frontend code.

README: exact install/dev/test/build/preview commands from dashboard/, local
only; how to use fixtures/upload; synthetic-only scope; no real runtime claims.
Integration doc: view-model schema, accepted bounds/errors, accessibility review,
files/public exports and remaining trusted-adapter work. Include a concise file
manifest, both-task checklist and honest verification ledger. Return all code
as complete fenced files, not PDFs. Number parts if necessary and finish with
END OF AGENT 2 EXPLORER DELIVERY.
'''


def main():
    fixture_source = ROOT / 'docs/reviews/statistics-cascade-packet-v2.md'
    text = fixture_source.read_text(encoding='utf-8')
    raw = text.split('## Complete fictional fixture\n\n```json\n', 1)[1].split('\n```', 1)[0]
    panel = json.loads(raw)
    rows = []
    for row in panel['records']:
        rows.append({key: row[key] for key in (
            'task_id', 'config_id', 'seed', 'outcome', 'scorer_status',
            'evidence_validity', 'baseline_verified', 'cost_nano_usd')}
                    | {'visible_tests_pass': row['signals']['visible_tests_pass']})
    fixture = {
        'schema_version': 1, 'view_model': 'dojo-explorer-view-v1',
        'source_kind': 'synthetic_ui_fixture', 'evidence_kind': 'synthetic',
        'eligibility': 'UNVERIFIED', 'real_provider_calls': 0,
        'construction_counts': {'total': 63, 'train': 37, 'held_out': 26},
        'evaluated_task_count': 4,
        'configs': [{'config_id': config, 'label': f'Fictional configuration {config}',
                     'task_count': 4,
                     'solved_count': sum(r['outcome'] == 'solved' for r in rows if r['config_id'] == config),
                     'expected_total_cost_nano_usd': sum(r['cost_nano_usd'] for r in rows if r['config_id'] == config),
                     'confidence_interval': None, 'interval_reason': 'Synthetic UI fixture; no empirical interval'}
                    for config in ('A', 'B')],
        'rows': rows,
        'limitations': ['Synthetic UI demonstration, not real model performance.',
                        'No verified registration or public-result eligibility.',
                        'Initial construction covers two pinned Python repositories.',
                        'Visible tests do not determine separate evaluator correctness.',
                        'No cold-restart cascade has been evaluated.'],
    }
    parts = [PROMPT, '\n## Complete synthetic frontend fixture\n\n```json\n',
             json.dumps(fixture, indent=2), '\n```\n']
    for name in ('dashboard/README.md', 'docs/reviews/agent2-review-assessment-v1.md'):
        data = (ROOT / name).read_bytes()
        parts.extend([f'\n## FILE: {name}\nSHA-256: {hashlib.sha256(data).hexdigest()}\n\n````text\n',
                      data.decode('utf-8'), '\n````\n'])
    parts.extend(['\nFixture provenance: original synthetic statistics packet SHA-256 ',
                  hashlib.sha256(fixture_source.read_bytes()).hexdigest(),
                  '\n\nEND OF EXPLORER PACKET\n'])
    with TARGET.open('x', encoding='utf-8', newline='\n') as output:
        output.write(''.join(parts))
    print(f'Created {TARGET.relative_to(ROOT)} ({TARGET.stat().st_size} bytes)')


if __name__ == '__main__':
    main()
