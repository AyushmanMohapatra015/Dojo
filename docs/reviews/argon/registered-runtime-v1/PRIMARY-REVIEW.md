# Primary review of Argon runtime bridge Part 1

Status: reviewed design; implementation pending. The original response is preserved in `../registered-runtime-part1-feedback-v1.txt`; the two complete extracted deliverables are in `outputs/`. Argon did not execute code or tests.

## Accepted

- The claim → reservation → request intent → response observation → candidate → scoring → settlement sequence is a useful implementation map. Preserve the existing owner and lease fencing and the durable `uncertain` terminal state.
- The crash matrix and 22 proposed cases are a strong test checklist. Every external dispatch needs an intent recorded before it, and unknown usage or cleanup status must stop replay.
- Scripted transport, fake sandbox, and local Docker evidence must stay separately labeled. Their rows remain `unverified_diagnostic`; a successful rehearsal is not a registered benchmark result.
- A new versioned Stage B source snapshot is required before the runtime coordinator can participate in registered execution. Do not change frozen v1 artifacts.

## Required corrections before adopting Part 2

1. **Synthetic binding is not implemented by a DTO.** `ObservationStore.claim_cell` invokes `prepare_bound_plan` and `build_intent`; `candidate_observation` and `scoring_observation` invoke `load_contract` internally. A `SyntheticCellAdapter` alone cannot redirect these calls. Test monkeypatching does not establish a production path. Either propose narrow explicit synthetic interfaces with host-verified provenance, or keep synthetic rehearsal outside the registered observation store. Never forge Stage B records.
2. **Do not call `docker_scoring_v2._execute` as the scoring entrypoint.** Its public `run_development_score` checks the synthetic-only gate, reviewed profile, timeout, selector restoration, and pinned local image before calling `_execute`. A direct adapter would bypass those checks. A versioned, guarded public scorer that returns candidate and conditional baseline raw receipts is the preferred minimal change; keep all current checks and cleanup behavior.
3. **Do not infer omitted APIs.** The packet manifest contains 54 files, not 24. Signatures in omitted helpers are not established by imports. Part 2 must either receive their exact current sources or avoid depending on them. The supplement below lists the missing files.
4. **Separate settlement from success.** `scoring_observation` accepts a canonical raw receipt and requires raw baseline evidence only when `assess_candidate` returns `requires_baseline`. Known model cost can settle after an intact workspace is scored even when the agent stops at a limit. Record the stop reason; scorer outcome must remain independent. A failed/unknown sandbox or cleanup cannot be scored and must remain uncertain.
5. **Clarify ownership of injected adapters.** The proposed signature accepts transport, sandbox, scorer, pricing, and clock from a caller. That is appropriate for isolated tests, but a trusted entrypoint must construct or verify these on the host and bind the exact sources. Do not let caller flags or a digest alone grant execution or publication authority.
6. **Treat AC-13 and AC-14 precisely.** A canonical receipt that yields `invalid_evidence` can settle known cost while its outcome stays undetermined; malformed bytes stop as uncertain. Protected-test edits must be removed by restoration and must not influence visible agent messages. Test patch mismatch and source-policy violations separately.

The proposed API inventory and acceptance matrix are design inputs, not evidence that the bridge exists. No real provider, sponsor, or Docker call was made during this review. The one real probe permit remains consumed.
