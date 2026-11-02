# Primary review: Argon browser UI Part 2 (10j3/10j4)

Original response: `browser-v2-ui-part2-feedback-v1.txt`, SHA-256
`9387cc523b3ee7d9eab310952b64f3b5656469f490b93dac460a24920decc7a2`.
The 12 named code blocks and their original bytes are preserved under
`proposals/browser-v2-ui-part2-v1/` with a delivery manifest. The embedded
Markdown guide contained nested code fences, so its extracted block was
truncated; the installed reproduction guide was written and verified locally.

The original `App.jsx` had ten `\\vert{}` and two `\\%` response escapes.
Those were normalized in the installed copy. Argon's two JSON fixture blocks
were valid JSON but **did not match** the accepted byte hashes or lengths.
The installed fixtures are copied from the canonical unequal-seeds pair.

The initial React/hygiene run had 11 failures among 26 tests. A major test
defect was a fixture loader using `import.meta.url`, which Vitest rewrote to an
HTTP-style URL. Its catch block silently substituted the bundled fixture for
every scenario. The installed test loader now reads the fixed local fixture
path and fails when it cannot read it. Remaining incorrect selectors, text
segmentation and large-number presentation expectations were corrected;
the denominator text in the UI was made grammatical. Accepted `src/v2/*.mjs`
modules were unchanged.

Final local evidence: `npm test` passed 43 Node v2 tests and 26 React/hygiene
tests; `npm run build` succeeded. A local preview returned HTTP 200 for HTML,
JS and CSS, and the production HTML contained `connect-src 'none'`. The build
warned about a 694 kB JS chunk (about 201 kB gzip). No manual browser or
assistive-technology inspection, hosted deployment, real model call, or real
result acceptance occurred. Source hygiene tests check selected client files;
they are not a substitute for a full security or dependency audit.
