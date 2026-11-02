# Next Argon assignment: browser explorer v2 in two parts

Current override (10j5, 2026-10-31): Part 1 was received, independently reviewed,
adapted and integrated. Do not resend it. See browser-v2-part1-primary-assessment-v1.md
and browser-v2-part1-git-checkpoint-v1.md. UI Part 2 remains queued; the owner
requested Nemotron/provider integration next. Instructions below preserve the
original launch/continuation workflow as historical context.

ACTION_PLAN 10j0-10j4, prepared 2026-10-31. This replaces the completed explorer
export/bundle assignment as Argon's NEXT work. Provider response review remains
primary work; Agent 2's old v1 acceptance assignment is an independent read-only
snapshot review. Do not resend completed export or provider assignments.

## Step 1: send the current Part 1 packet

Start a fresh Argon chat. Attach ONLY:

`docs/reviews/argon/browser-v2-part1-packet-v1.md`

This single file embeds the assignment, 37 hashed reference/context entries,
selected complete v1 reuse sources, current backend validators and 14 canonical
JSON artifacts across seven fictional cases. It is 481,371 UTF-8 bytes. These
bytes are not a token count or a guarantee of any web agent's context limits.
The separate assignment, fixtures, manifests and source folder do not need
additional attachments. No account, keys, real hidden tasks or folder access
is required. The Python sources are static wire-schema references; their full
runtime dependencies are not needed to write the browser JavaScript.

Paste this exact launch prompt:

> Read the attached packet through END OF ARGON BROWSER V2 PART 1 PACKET.
> Implement the two assigned groups, 10j1 and 10j2, using the embedded accepted
> v2 contract and fixtures. Reuse useful supplied frontend code after adapting
> it to v2. Return the nine complete files in the specified order, beginning
> with the concise API/design map. Preserve the fixed APIs, exact fractions,
> seed denominators, unknown-cost behavior and synthetic/UNVERIFIED scope.
> Do not implement React Part 2 or regenerate the accepted Python work.
> If output is running short, finish the current file, stop and list exact
> delivered/remaining paths. I will ask you to continue in this same chat.
> Mark any unavailable syntax/test/browser checks UNEXECUTED; never invent
> execution results or hashes. End complete delivery with
> END OF ARGON BROWSER V2 PART 1 DELIVERY.

## Step 2: continue an interrupted delivery

If Argon stops after complete files, continue the SAME chat and paste:

> Continue the browser v2 Part 1 assignment using the same attached packet.
> First list which exact files you have already delivered and which remain.
> Produce only the remaining complete files; do not repeat accepted completed
> files or move to React Part 2. If the last file was cut off mid-body, resend
> that one file completely and label it as its replacement. Keep execution
> claims honest and update the final verification ledger accordingly.

The ledger/manifest must not call a clipped delivery complete. Save all returned
file sections and any explicit replacements; primary resolves their provenance.

## Step 3: save the response

Save the complete response as UTF-8 text:

`docs/reviews/argon/browser-v2-part1-feedback-v1.txt`

Markdown is also usable, but keep all code text, file headings and fences. Do
not convert it to PDF or copy only the design summary. Tell primary when saved.
The response will be archived, reviewed, reproduced and adapted before adoption.

## Step 4: primary acceptance before the UI packet

Primary checks source completeness/syntax, real Node tests against supplied
fixtures, arithmetic/validation counterexamples and stable return schemas. It
compares browser acceptance and point metrics with the accepted Python outputs.
Expected Node command after adopting the proposed files:

```powershell
node --test dashboard/src/v2/exact.test.mjs dashboard/src/v2/data.test.mjs dashboard/src/v2/derive.test.mjs
```

This uses Node's built-in tests without npm installation. It does not establish
React, Recharts, build, browser or hosted-site correctness. Application adoption
is a separate reviewed step; current dashboard still has only README.md.

## Step 5: prepare and send Part 2 after review

Part 2 is reserved under 10j3, then 10j4 primary acceptance; its exact-source
packet is deliberately prepared AFTER the new JavaScript interfaces are
reviewed. There is no Part 2 implementation packet to upload yet. This avoids
asking Argon to guess how returned Part 1 code differs from the request.

Its scope will advance existing 10b-10g tasks: wire reviewed v2 functions into
the existing UI design; preserve upload cancellation/reset behavior; present
seed-aware task/run details with reachable pages; render exact-metric cards,
both cost/success frontiers and accessible table equivalents; expose frozen
cascade comparisons/family diagnostics and method/uncertainty caveats; improve
keyboard/responsive/error/empty states; return component tests and reproduction
instructions. It cannot turn synthetic metadata into approved real results.

That fresh packet will include the reviewed Part 1 bytes/contract/tests, full
UI/CSS/test/build proposal, known frontend findings, canonical fixture files and
precise acceptance commands. Primary owns isolated dependency resolution,
actual component/build/browser/CSP/accessibility checks and later publishing.
Do not add provider calls, telemetry, sponsor integrations or deployment to
either browser assignment. Our primary next task remains 8h5 provider review.

## Optional manual Git checkpoint for this handoff

These commands stage this packet/context and related plan updates. Earlier
uncommitted runtime work has its own reviewed Part 2 checkpoint guide; preserve
those prerequisites when committing the application. No Git action was run by
primary. From the repository root:

```powershell
git add -- ACTION_PLAN.md PROGRESS.md docs/agent-work-queue-v1.md scripts/prepare_argon_browser_v2.py
git add -- docs/reviews/argon/browser-v2-part1-assignment-v1.md docs/reviews/argon/browser-v2-part1-packet-v1.md docs/reviews/argon/browser-v2-two-part-guide-v1.md docs/reviews/argon/browser-v2-context-v1
git diff --cached --check
git diff --cached --stat
git commit -m "Prepare Argon browser v2 data-layer handoff"
git push origin main
```

Review the staged summary before committing and stop on an unexpected error.
Do not use reset/clean/force-push to work around one. Uploading the packet does
not depend on committing or publishing it.
