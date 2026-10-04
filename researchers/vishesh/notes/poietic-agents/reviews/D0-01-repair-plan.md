# D0-01 offline repair and error diagnosis

Prospective revision, 2026-10-04. The owner requests formatting repair, error diagnosis and a cost estimate for replacing Qwen with Haiku. This authorizes offline changes and non-billable status reads; it does not choose the alternative model or authorize a new native attempt. Read the [completed D0 post-mortem](D0-01-post.md) and [scientific assessment](D0-01-scientific.json). Preserve source 38544138, native grades, all 40 physical calls and USD 0.568560890 cumulative conservative exposure.

## Question and decisions

Can a bounded serialization adapter execute the already-correct fenced action without admitting malformed actions, and can transport telemetry distinguish a future provider refusal? The saved Haiku response resolves its first failure: exactly one JSON fence enclosed the correct flat action. Qwen's first action succeeded, then HTTP 429 supplied no usable answer. Its retained markers do not identify the responsible rate-limit layer. This is engineering diagnosis; no swarm-efficacy or general model-competence claim follows.

## Implementation before any new run

1. Add an explicit chat response policy accepting either a bare JSON object or exactly one complete lowercase `json` fence with line breaks. Do not extract JSON from prose, repair syntax, unwrap nested actions or accept multiple objects. Reject duplicate keys and nonfinite numbers in the new policy. Retain the raw provider object and hash; add a receipt stating whether a fence was removed. Keep historical strict policy available and old frozen runs unchanged. All existing action-field, route, usage, permission and engine checks remain.
2. Improve both relay error paths with allowlisted metadata: HTTP/body status, normalized Retry-After, numeric rate-limit headers, provider identity only if pinned, and known typed error/limit-source categories. Never emit free-form messages, raw metadata, headers, request IDs, credentials or account identifiers. Detect provider error bodies even when HTTP 200 is returned. Preserve complete uncertain reservations and the global transport stop; add no retry or fallback.
3. Verify public endpoint tariffs/status and current per-key exhaustion through non-billable GET requests. Return only verification booleans. These checks cannot prove the historical 429 cause or current inference availability.
4. Estimate a Qwen-to-Haiku substitution at equal token counts and at the existing maximum 8,192 input / 1,024 output bound. Show diagnostic and full-qualification request counts, cumulative original-budget headroom and inference limits. Do not alter the model selection as part of an estimate.

## Offline sample, controls and acceptance

Use all retained D0 started records (3 requests, 2 returned answers, 1 provider error) as inspected development evidence, never fresh qualification. Synthetic format fixtures cover bare/fenced valid actions, surrounding prose, nested/multiple actions, duplicate fields, nonfinite values, incomplete fences, unknown fields and protected access. Whole-worker rehearsals use development worlds only and fake providers, exercising correct action effects, retained known billing, role-local invalid stops and global 429/HTTP 200-error stops. Fault metadata includes secret-shaped strings and unknown types to ensure none can reach receipts. No new independent experimental unit is collected.

Acceptance: the retained fenced answer parses and executes in a labeled retrospective replay; its original native score stays invalid. New faults must never become accepted actions. One provider error causes one dispatch with no retry, retained full reserve and sanitized diagnostics. All previously valid controls and historical strict-parser fixtures remain reproducible. Original ledgers and spending remain unchanged; no allocation is held.

## Next native decision

A changed response policy requires a fresh prospective attempt and source/runtime/public admission. D0-01 IDs are consumed; all inspected roots are retired. A future screen must cover fetch, answer, refresh and the three structural variants across fresh paired roots, distinguish 12 dependent decisions per role from independent roots, preserve the original full qualification threshold and disclose weak precision. Any model substitution must be an explicit separate cohort: two Haiku roles no longer test cheap-generative model differentiation. Prepare and obtain approval of that concrete next-run plan before allocating or dispatching. No automatic successor is included in this repair.
