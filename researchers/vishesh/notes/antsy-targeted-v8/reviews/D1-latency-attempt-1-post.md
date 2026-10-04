# D1: the slow call finished, but still did not yield a total

2026-10-04, vishesh/codex-methods. Same-author assessment of **D1-latency-attempt-1**, execution source `1dea9b40971fa1b666ab31930ce4cd0d523f22fd`. The [prospective plan](../execution-repair-v1/PLAN.md) and [condition-specific assessment](../execution-repair-v1/D1-PRE.md) preceded execution and were explicitly approved by the owner. This post-mortem is retrospective.

## Decision and result

**FINISH this diagnostic; keep fresh qualification closed.** All three started calls returned valid outputs with full phase traces. The third took 46.25s, above the unchanged45s eligibility threshold, so the runner correctly left the remaining three planned repetitions unstarted. There was no timeout, retry, hosted-model call, new infrastructure charge or automatic successor. This is a valid adverse diagnostic result, not an execution crash or a passed qualification.

The new observation is useful: the call that previously timed out can finish, but its returned candidate is still an abstention. Extra waiting alone did not supply a usable receipt total. D1 does not demonstrate complementary error correction, independent errors or a benefit from multiple agents.

## Plan versus observations

Three reused CORD-v2 receipt units; at most two cold-process repetitions each in order60,61,62,60,61,62. Only the first repetition occurred. These are **three distinct development receipts, not six independent samples**, and no within-receipt variability can be estimated. Same host, pinned model/package fingerprints, original image hashes, parser, thread settings and cold-process contract as specified. No gold reference, peer output or operator conversation entered the OCR worker.

| Receipt | Dimensions | Imports | Reader initialization | Combined OCR | Total wall | Candidate | Eligibility |
|---|---|---:|---:|---:|---:|---|---|
| train60 | 576×864 | 4.43s | 4.35s | 12.26s | 22.25s | 161000.00 | met |
| train61 | 576×864 | 4.32s | 3.88s | 9.02s | 18.34s | 17000.00 | met |
| train62 | 960×1706 | 4.37s | 4.07s | 36.63s | 46.25s | abstain | not met |

Extraction and output each took under 0.01s. The remaining wall time includes interpreter/parent overhead and gaps between instrumented phase boundaries; phase sums are not asserted to be complete end-to-end latency. The [saved-data audit](../results/D1-latency-attempt-1/audit.json) gives full precision and all six assignment statuses. The [native phase plot](../results/D1-latency-attempt-1/final_frame.png) displays the three unstarted calls.

The planned 90-second censoring ceiling was never reached. It was diagnostic observation time, not a relaxed qualification rule. Stopping at the first slow call is the preregistered rule; it does not authorize consuming the unused three calls elsewhere. The summary's `complete: false` means not all six assigned calls executed; the manifest's `complete: true` means the diagnostic reached its terminal reporting step. Preserve both original files and their distinct meanings.

## Native trace review and interpretation

All 3/3 started calls have retained private raw OCR, stdout, stderr, phase events and terminal records. Their stream, phase and output hashes match saved receipts. All three candidates reproduce exactly when saved words pass through the unchanged parser. Six assignments reconcile to 3 valid and 3 unstarted, with 0 unresolved starts. The [trace audit](../results/D1-latency-attempt-1/audit.json) publishes only numeric decisions/timings/hashes; raw receipt words and operator context remain private.

For train62, combined OCR accounts for 36.63/46.25s, approximately 79% of wall time. Imports plus reader initialization account for 8.45s. This localizes most **observed** cost to the OCR phase, not to parsing or output. The phase includes detection and recognition, so D1 cannot identify which component dominates. Larger image area and more detected words are plausible contributors; size/content/layout are confounded, and one receipt does not identify a causal size effect. No host-variability or repeatability estimate exists because the second repetitions were not run.

The two smaller receipts reproduce the same candidates as Q0. On train62 the checker emitted 54 OCR words but the shared parser rejected its only recognized total-anchor row: it contained `Qty` and two numeric tokens. The [field trace](../results/D1-latency-attempt-1/field-trace.json) records that decision. This is observed conservative rejection, not proof of an incorrect parser or a correct alternative amount. D1 did not attach a new ground-truth reference for this partial-Q0 case. Do not remove exclusions or select the largest number merely to obtain a success.

There are two distinct remaining obstacles: cold-call latency eligibility and field-level answer coverage. A persistent reader might save some initialization work, but subtracting 8.45s from the wall total is only an illustrative accounting counterfactual; a warm service was not measured and changes the execution contract. Even if it met45s, this saved output would still abstain. Thus a performance-only repair would not establish that this checker earns its cost.

## Quality assessment

The question and sample were appropriate for a bounded diagnostic of a known failure; they are inadequate for efficacy or rare-error claims. Strong points were prospective stopping, exact retained-input/runtime binding, complete phase/stream retention, cold-process isolation and full assignment reconciliation. The [eleven-dimension review](D1-latency-attempt-1-quality.json) marks latency capability as a gap and explicitly limits all passes to this diagnostic scope. Same-author replays and fault tests are not independent replication.

The native visualization agrees with saved data and visibly marks unstarted assignments. Its phase bars omit interpreter/parent overhead as labeled; use the wall labels for eligibility. The hub initially displayed 6/6 because its `done` event forces completed progress, even though only 3 calls ran. A reporting-only follow-up restored explicit 3/6 progress and added `started_calls:3`, preserving terminal status and the original artifacts. This did not rerun or change any outcome. The public page was checked after the correction.

## Closeout and next action

Five original hub artifacts were read back with matching SHA256. Private evidence was backed up locally; worker/native-child absence was verified at 18:09:45 UTC before releasing the exclusive allocation. The next host user was notified after the merged release. No new charges or hosted calls; historical Antsy costs and reservations carry forward without a new allowance. The operational finalize record and this scientific assessment are separate; finalize's generic scaffold does not claim scientific review automatically.

No successor is launched. Before requesting another native run, assess whether a checker can add field-level value on these development traces using a justified alternative extraction contract and independent labeled development cases. Preserve abstention when evidence is genuinely ambiguous. Only then decide whether a warm service or other performance change merits a separate controlled comparison. Any such changed design needs a concrete prospective plan and owner approval; the unused D1 calls and failed Q0 allowance are not retry authority.

A valid stopping decision is to park this checker under the current cold45s contract. D1 answered its narrow question: retained traces now explain the observable bottleneck, and simply allowing the slow call to finish did not rescue the missing field.
