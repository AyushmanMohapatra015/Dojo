# Primary review: four-view integration

Accepted the structure, mounted view wrappers, dataset disclosure, source label
and test migration. Primary adapted code to actual source instead of applying
the diffs directly: app context was ambiguous, the CSS context did not match,
and the test diff incorrectly marked an async signature as unchanged context.

Corrections integrated:

- One persistent restriction component owns blocked/incomplete-cost notices;
  removed the duplicate notices from Method, preserving their original messages
  and accessible labels. Evaluated denominator and synthetic status remain
  visible across all four views, including complete-cost views.
- Scoped the hidden rule to .explorer-view[hidden], retained native details
  markers and made its summary comfortably clickable. Added clear view headings.
- Simplified introductory copy without exposing protocol jargon or deleting
  detailed evidence, uncertainty, exact values or limitations from Method.
- Replaced the proposed negative 'Select' text assertion (which matched
  'Selected run details') with a real filter/page/selection persistence test.
  Primary corrected its own initial button-name lookup, then verified reset and
  focus behavior through the actual controls.

Verification scoped to the frontend: 46 checks passed in the initial UI suite,
with one faulty proposed test; 24 App checks passed in the next run, and the
corrected remaining App case passed independently. The unchanged navigation and
hygiene files already passed. Production build passes with the existing bundle
size advisory. Data modules/backend code are unchanged; no backend/math suite
rerun was needed. Real-browser chart sizing/reflow remains 10k4.

Use context-batch3/ for further work. Earlier snapshots and original responses
are preserved. The next assignment is moderate visual/copy polish, not another
navigation or data-layer rewrite.
