# Retrospective issue descriptions v1

The active construction pool has 63 tasks: Click v1 contributes 34 and
more-itertools v2 contributes 29. No historical more-itertools v1 task is added.
The original labels remain 37 train and 26 held out. No solver outcomes exist.

The issue inventory now contains one authored description per task. These are
retrospective behavioral requests authored from local upstream commit subjects
and non-test source changes, not original user-filed issues. The author reviewed
reference implementation changes to understand intended behavior. Hidden test
assertions were not used as authoring input. This is reference-informed task
authoring and must be disclosed in reports; these prompts must not be presented
as independently collected historical issues.

Review was performed by the same Codex author, not an independent reviewer.
Descriptions specify observable behavior, public API contracts and necessary
error categories, with no patch hunks, replacement code, hidden test IDs,
reference hashes or solution links. New public API names are requirements for
feature requests, not claims those APIs exist in the parent tree. Automated
checks detect binding/artifact errors, not every possible semantic hint.

## Suitability findings

This is a mixed coding-task pool, including new features, API contract changes,
compatibility restorations and bug fixes. It is not exclusively a bug benchmark.
The inventory records an editorial task_kind per description. This does not
change construction eligibility, membership or labels.

Distinct full patches do not guarantee semantically independent problems:

- more_itertools_1fd388bc2379 and more_itertools_670b715b307a have identical
  non-test Python source changes, though their construction records differ.
  Both remain held out. Report this duplication rather than claiming 63 unique
  underlying programming problems.
- more_itertools_d63a26e56eac and more_itertools_93c1cf8484f0 request opposite
  first_true keyword changes at different base snapshots; both are train.
- Numeric range, seekable and Click pager/help/completion tasks recur across
  history. Some families cross the train/held-out boundary. Chronological
  splitting does not ensure semantic family isolation or absence of training
  contamination from the public upstream repositories.

Keep frozen task IDs and labels intact. Before model evaluation, separately
register the primary metric and treatment of related tasks, and consider a
clearly labelled family/duplicate sensitivity analysis. Do not silently count
related tasks as independent evidence or reshuffle the existing split.

## Checking and freezing

Run `.venv\Scripts\python.exe -m dojo.solve.issue_review freeze` once after
editorial approval. It verifies all construction evidence, exact task order,
labels, hashes and approval status. It builds every solver input from the local
original base tree, records archive/text hashes, then exclusively creates
data/issue-prompts-v1.lock.json. No archives are extracted or executed.

Use the same module with `check` to recompute and compare the manifest. This
freezes issue content and source identity; it is not Stage B model registration
and does not enable any solver or paid provider call. Model evaluation remains
unregistered and inference stays locked. An independent review is recommended
before completing Stage B.
