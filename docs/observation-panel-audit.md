# Read-only observation panel audit (5f3f)

From the project root, pass an existing v6 diagnostic store:

```powershell
.venv\Scripts\python.exe -m dojo.bench.panel_journal_audit --snapshot data/development/stage-b-preflight-v4 --store PATH_TO_EXISTING_OBSERVATION_STORE
```

Replace the store placeholder with the actual local diagnostic database path.
The command refuses missing stores without creating them. Exit 2 means refusal
or incomplete diagnostic coverage; exit 0 means only diagnostic completeness,
with all execution and publication authority flags still false.

The CLI also has an actual malformed-SQLite regression: it refuses the file,
preserves its bytes, and prints only the fixed diagnostic reason. Three CLI
tests pass, including the missing-file and sanitized-error cases.

`dojo.bench.panel_journal_audit.audit_observation_panel(directory, store)`
checks the exact host-verified expected cell plan against a local v6
ObservationStore. It reads every intent and validates each append-only
observation chain through the store's existing reader. It also counts parent
attempts that crashed before intent association.

The result counts missing cells, duplicate cells, unexpected attempts, foreign
snapshot attempts, orphan attempts, unsettled attempts and invalid scoring
diagnostics. No attempt is selected as the winner. A settled diagnostic attempt
does not erase missing cells, and orphan attempts block completeness. Reads are
bounded to 20,000 attempts; oversize histories are refused. The function does
not mutate the journal, replay an attempt, or reconcile provider billing.

`diagnostic_panel_complete` describes this local, unverified journal only.
All registration, provider-verification, execution-authority and publication
flags remain false. An actual registered denominator and genuine execution
provenance require separate host review and financial/scorer gates.

Two focused fictional-store tests cover a single settled attempt with 251
missing planned cells and a crash before intent association. No model,
container, network or paid service is used.
