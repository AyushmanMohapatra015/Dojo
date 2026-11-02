# Repeatable local runtime acceptance

Executed on 2026-11-02: all twelve cases passed in the final v2 report.
Independent checks confirmed unique case coverage, final cleanup, zero-provider
flags and current selected-source hashes. Two focused report-safety tests pass
(0.10s), and Ruff passes. Historical v1 remains preserved.

Task 5e4r7 turns the individual rehearsals into one twelve-case command:

```powershell
.venv\Scripts\python.exe -m scripts.runtime_local_rehearsal --matrix --output data/runtime/local-runtime-matrix-v2.json
```

Use a new report filename for an intentional repeat. Existing reports are
refused before any case runs. The output directory must already exist. The
report is a private local diagnostic under Git-ignored `data/runtime/`.

The matrix uses both synthetic scoring profiles, `pallets/click` and
`more-itertools/more-itertools`, with a common local solver sandbox and the
profile-specific actual Docker scorer. Every model response and token count
is scripted. No provider, sponsor or credential access occurs.

| Scenario, for each profile | Required observation |
|---|---|
| Unchanged source | Failed scoring, unsolved |
| Correct scripted source fix | Passed scoring, solved |
| Syntax error in candidate | Candidate error, unsolved, fresh baseline verified |
| Replace protected test file | Failed scoring after evaluator restoration |
| Command timeout | Uncertain attempt, no scoring, no settled cost |
| Run original visible tests | Visible tests pass while separate scoring fails |

All non-timeout cases must settle the fictional ledger. Timeout must retain
uncertainty. Every case checks owned-container cleanup. A final cleanup check
also runs if a case fails. Failures produce exit 2 and a fixed, sanitized
failure reason; raw exception messages are excluded. An abrupt process death
can leave an incomplete or empty report, which is not acceptance evidence and
must not be overwritten as a recovery shortcut.

Reports bind selected orchestration source hashes before and after the suite;
these hashes are not a full environment authenticity claim. Individual results
retain false registration, provider-verification, live, benchmark and public
eligibility flags. Independent temporary stores prevent scripted scenarios
from sharing cached outcomes. Fictional costs are not actual Nebius charges.

This milestone tests local orchestration, not Nemotron coding performance,
adversarial scoring integrity, real registered task execution or deployment.
The next critical work remains model/template token bounds, current financial
admission, scorer scope and verified genuine execution evidence.
