# Batch 3 primary review

Read all three original outputs; originals preserved. Accepted the restrained
header/divider and spacing direction, source-label wrapping, status wording and
correction of literal question-mark separators. Adapted the patch manually.

Rejected flex display on the native summary: retain `display: list-item`,
the native disclosure marker, 44px minimum height and existing visible focus.
Kept readable mobile text sizes rather than shrinking controls to 0.88rem.
Retained short introductory copy instead of adding schema IDs, Pareto terminology
and claims of full arithmetic provenance to the first user-facing paragraphs.
Preserved evaluated counts, synthetic status and every blocked/cost warning.

Only App.jsx explanatory text and scoped shell CSS changed. No parsers, math,
state, headings/ARIA IDs, upload handlers, navigation or dependencies changed.
Production build and static bundle audit pass; existing chunk advisory remains.
All 12 existing source-hygiene tests pass (36.18s including environment startup).
Actual browser marker/reflow/chart/contrast verification remains under 10k4.
