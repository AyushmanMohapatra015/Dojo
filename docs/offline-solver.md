# Offline solver controller

Run `.venv\Scripts\python.exe -m dojo.solve.simulation demo` for a synthetic
read/edit/test/finish walkthrough. Every model response, command output, patch
and visible-test verdict is scripted. Commands are never executed, archives
are not extracted and no provider is called. This is controller development,
not evidence that a model solved a task or that a patch passed hidden tests.

The controller accepts only the exact ScriptedModel and FakeSandbox types.
Its default limits are 40 model turns, 3,000 output characters per observation,
60 seconds per command, 300 seconds per run and 500,000 synthetic token units.
Token units are UTF-8 bytes divided by four, rounded up; they are fake accounting,
not a Token Factory tokenizer, billing estimate or live spending guard. The
next reply allowance is reserved before a model turn; oversized replies stop
without executing partial commands. Deadline checks bound dispatch, and the
timeout sent to a command cannot exceed the remaining run allowance.

The initial action contract is one JSON bash action or an explicit finish.
Malformed, duplicate or extra-key actions are not executed. Invalid responses
consume a turn and receive format feedback. no_command_rate is invalid turns
divided by attempted command turns plus invalid turns, excluding explicit
finish actions. Step limits include invalid and finish turns. Sandbox/runtime
failure stops without feeding raw host exceptions to the model.

Only explicitly identified visible-test feedback sets visible_tests_pass; an
ordinary successful command cannot set it. A later patch change invalidates
the old visible-test verdict. has_patch means a nonempty scripted diff, not a
validated patch. self_reported_done is a runtime signal, never a correctness
score. All simulation results are marked simulation_only and not_scored.

For local task preparation, simulate_task requests inputs through input_guard_v2.
The synthetic CLI demo uses its separate tiny fixture, not a benchmark task.
Issue text and command observations are labelled untrusted data, and archives,
reference patches, receipts, split labels and hidden-test outcomes are not
passed to model messages. No trajectories are written by default.

This slice does not implement mini-swe-agent integration, a real Docker solver
sandbox, patch application, hidden-test restoration/scoring or provider billing.
Those adapters require separate implementation and review. Existing live
inference gates remain locked; Stage B model evaluation stays unregistered.
Next: a bounded offline Docker adapter on synthetic development fixtures, then
the scoring boundary, before any real model integration.
