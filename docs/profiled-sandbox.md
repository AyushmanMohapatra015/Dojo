# Repository-specific solver environments (task 4g)

`dojo.solve.profiled_sandbox` selects reviewed immutable Docker images and
native collectors from `dojo.backends.profiles`. Click uses the legacy collector
and an offline installation into `/tmp/site`; more-itertools uses ReceiptV2
without installation. Containers retain the existing network, user, filesystem,
resource and cleanup restrictions. No provider credentials are forwarded.

Visible tests are Python files named `test_*.py` or `*_test.py` in the exact
approved original archive. The list is fixed before edits and never comes from
gold patches, hidden tests, expected node IDs or evaluator scope. Existing
conftest files can support collection; newly added test files do not expand the
reserved visible-test command. Agent-modified visible tests remain untrusted
feedback, separate from hidden scoring.

Each command uses a fresh container. Click installation is repeated offline
before commands, with dependencies/build isolation disabled and an eight-second
setup timeout. Broken project installation fails the command; repair behavior
for build-configuration edits remains a future interface/policy decision. Source
and `src` imports retain precedence. This policy can select more tests than the
construction scorer; real-suite timing and compatibility are not yet measured.

`prepare_task_environment` checks approved input bindings and prepares a sandbox
without starting Docker. All 63 approved inputs prepared successfully: 34 Click,
29 more-itertools; 2–43 original visible files each. This is not evidence that
their actual code or test suites have run successfully.

The preserved `data/development/profiled-solver/profile-smoke-v1.json` records
four synthetic controller-to-scorer cases on each native profile: fixed passes,
unchanged and test tampering fail, and timeout is not scored. Additional runtime
checks verify the unprivileged user, Click installation metadata and no exported
installation artifacts. Containers were cleaned up. Provider/model calls: zero.
These results are development evidence, excluded from benchmark results.

Next: task 4h provider/controller interface and reuse/license decision. Stage B
registration and credit/accounting gates still apply before actual model runs.
