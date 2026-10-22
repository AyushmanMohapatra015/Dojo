# Solver input preparation

Run `.venv\Scripts\python.exe -m dojo.solve.task_view inventory` once to create
the evaluator-only `data/issue-review-v1.json` queue from active Click v1 and
more-itertools v2 evidence. It checks registration, record hashes, repeated
quality evidence, export identity and split consistency. It refuses to overwrite
an existing queue. The queue contains no automatically approved commit messages.

For each task, write a behavioral issue description with observed symptoms,
expected behavior and sufficient public API context. Review for solution leakage:
omit patch hunks, replacement code, implementation instructions, fixed test
assertions/IDs, reference commit identities and links that reveal the fix.
Do not select or rewrite issues based on model success. Public repository
contamination remains possible. Keep every existing train/held-out label.

Approval requires `status: approved`, a named `reviewer`, and `text_sha256` equal
to the UTF-8 SHA-256 of the exact `text`. The issue is bound to `record_sha256`;
changing text or task requires another review. These hashes prove identity,
not that a reviewer made a sound semantic judgment. Obvious patch artifacts are
rejected by code; meaningful content review remains necessary.

`build_solver_input` accepts an approved issue and verifies the repository and
commit parent. Its result has exactly two fields: issue text and an archive read
from the original base commit. Existing base tests are visible. It never uses
the construction snapshot containing fixed tests, and provides no Git history,
fix identity, reference patch, receipts, hidden tests, split label or scorer
metadata to the agent. The caller must pass only this result to the future
agent. Repository text and issues remain untrusted input. Base files have the
existing path/type/size checks and execute only in the future sandbox.

The queue now contains 63 authored descriptions with semantic self-review;
independent review has not occurred. See [issue review](issue-review-v1.md) for
provenance, task-family limitations and the separate issue manifest check.
Solver inputs may be constructed in memory to verify their identity; no
benchmark agent has received them. Stage B model evaluation is unregistered.
