# Scripted solver-to-scorer flow: action-plan task 4f

The known synthetic more-itertools package now runs through the actual bounded
controller, actual Docker commands, workspace/diff export and isolated hidden
scoring. No provider transport, benchmark task or live cost measurement is used.

The sandbox receives only SolverInput(issue_text, source_archive), containing
original files. The evaluator owns the contract, hidden test overlay and final
receipt. It scores after the scripted model stops; it makes no new model call
and cannot change the retained agent workspace or recorded model contexts.

Regression guards check all model-visible contexts for a hidden-only canary,
hidden test IDs and scoring transport markers. These checks and structural
separation cover this synthetic flow; they are not a proof against arbitrary
Python runtime attacks. The known scoring threat model remains unchanged.

| Case | Visible feedback | Hidden evaluation |
|---|---|---|
| Correct source fix | Pass | Pass |
| Unchanged source | Pass | Fail |
| Replace visible tests with a trivial test | Pass | Fail after restoration |
| Command timeout | Incomplete workspace | Not scored |

Agent self-reported completion and passing visible feedback do not establish
correctness. Agent SimulationResult remains not_scored; the separate evaluator
result carries the hidden decision. Synthetic byte-based token counters are
not provider tokens or cost estimates. All provider calls/costs remain zero.

Evidence: data/development/solver-flow/flow-smoke-v1.json. Every created container
was cleaned up. The smoke command preserves existing evidence:

```powershell
.venv\Scripts\python.exe -m dojo.eval.flow_development smoke
```

Task 4g separately supplies profile-specific image, installation, native
collector and original-suite selection for both repositories. Stage B and
financial/live-provider gates remain pending.
