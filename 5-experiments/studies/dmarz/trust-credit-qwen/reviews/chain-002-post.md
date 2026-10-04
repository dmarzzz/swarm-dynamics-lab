# Post-mortem for trust-credit-qwen, chain-002 (S0, P0, Q0, S1), gpt-6-luna

Status: assessment completed by the attempt's builder on 2026-10-04. It is the builder's own review; no independent review took place. Follows [the review cycle](../../../../toolkit/agent-experiments/RUN-REVIEW.md) and [the quality rubric](../../../../toolkit/agent-experiments/RUN-QUALITY.md).

- Study / owner / stage / attempt / parent / assessed at: trust-credit-qwen (research program v5, line T) / dmarz / S0, P0, Q0, S1 / chain-002 (second model on attempt 001's packets) / chain-001 ([chain-001-post.md](chain-001-post.md), complete_valid_result) / 2026-10-04.
- Assessor and scope: dmarz/openai-route, builder of attempt 002, working offline from the saved records the operator copied off the server (results directories without images, and the chain log). The run was operated by dmarz/fleet-monitor on sim-dmarz-9 from launch commit `ca15e8ed`. Cross-researcher review was waived by dmarz for these exploratory runs; nothing here is an independent review.
- Pre-run assessment, plan, source, model, manifest: [chain-002-pre.md](chain-002-pre.md); [preregistration](../preregistration.md) section "Attempt 002: gpt-6-luna" with its implementation note; launch commit `ca15e8ed659ee200ad369776f870224d86ff7fb4`, code commit `2c399a6a`, source hash `5155d2c6ec89a232db0c46bd025f2dfba5759991cac1b0c6a27b806d916f4b84` (the run's recorded hash equals the code's); `gpt-6-luna` via OpenAI Chat Completions, `reasoning_effort: low`, `max_completion_tokens: 1500`, JSON-object mode; manifest digest `e09119d1…`, identical to attempt 001's (every stage's saved assignments reproduce it).
- Native outcomes and durable artifacts: [records/attempt-002/](../records/attempt-002/) (chain status with server paths replaced, per-stage summaries and analyses, gzipped rows, assignments and audits, recomputed numbers, the per-cell CSV, the paired comparison with attempt 001); results in [RESULTS.md](../RESULTS.md), section "Attempt 002 (gpt-6-luna)". Frames and the replay are on the hub and were not in the records. The raw chain log is not committed: besides the chain's own lines it holds the throwaway hub's access-log noise, including unrelated scanner requests to the hub port; nothing of the study is only in it.
- Review verdict: **complete_valid_result**, with one process gap: **`chain.py verify` was not run** (the server claim expired before the operator could run it).
- Execution: complete. Response validity: 528 of 528 valid. Qualification: passed (24 of 24 on set a). Scientific conclusion: descriptive second-model answers on identical packets; the scripted primary is unchanged by construction. Process compliance: plan (before the code), pre-run review and same-researcher check preceded the run; verify missing. Artifact delivery: hub artifacts not checked.

## Reconcile the recorded facts

| Quantity | Assigned or planned | Observed | Missing, partial or uncertain | Evidence |
|---|---|---|---|---|
| Independent roots and paired cells | 24 comparison roots × 21 cells; 8 qualification roots × 3 shapes (set a); 8 engineering roots (scripted) | 24 roots, all 21 cells; 24 fixtures; 8 engineering roots | none | records/attempt-002/s1-episodes.jsonl.gz |
| Assigned / started / terminal / graded / analyzed, S0 | 216 | 216 / 216 / 216 / 216 / 216 | none | records/attempt-002/report-numbers.json (reconciliation) |
| Assigned / started / terminal / graded / analyzed, P0 | 1 | 1 / 1 / 1 / 1 / 1 | none | same |
| Assigned / started / terminal / graded / analyzed, Q0 | 23 | 23 / 23 / 23 / 23 / 23 | none | same |
| Assigned / started / terminal / graded / analyzed, S1 | 504 | 504 / 504 / 504 / 504 / 504 | none | same |
| Model calls, including retries | caps 1, 23, 504; 640 transport attempts | 1, 23, 504 calls; 528 transport attempts (one per call); no retry; no billing pause; 0 voided | none | records/attempt-002/chain-status.json (ledger) |
| Input / output / reasoning tokens | byte bound at most 3.08 M input; output at most 528 × 1,500 | P0 2,572 / 33; Q0 59,156 / 1,271; S1 1,296,288 / 80,720; total 1,358,016 input, 82,024 output, of which 63,325 reasoning (0 on 358 of 528 calls, at most 840) | input tokens reported as exactly 2,572 on every call; cause not determined | report-numbers.json, s1-episodes |
| Actual spend / reservations / cap | expected USD 0.2 to 0.4, bound 0.79; cap USD 5 | P0 USD 0.000338; Q0 0.008031; S1 0.200960; total 0.209329 settled (computed from the pinned price row with reported cache writes; OpenAI reports no cost); no unsettled reservation | cost is computed, not provider-reported | ledger totals in chain-status.json |
| Wall time, concurrency, machine | S1 6 to 13 minutes expected at 3 to 6 s per call; 4 in flight | chain 12:43:56Z to 12:51:04Z (7 min 8 s); S1 worker 374.1 s; sim-dmarz-9; one call took 97.2 s (timeout 120 s), median 1.14 s | none | chain-status.json, rows |

- Reconciliation differences, duplicates, exclusions, unstarted assignments: none. Every assignment id occurs once; no row is excluded.
- Cost estimate versus actual: estimate USD 0.2 to 0.4, actual USD 0.209. Every call reported `prompt_tokens_details.cache_write_tokens` (2,569 on 523 calls, 0 on 5) and `cached_tokens` (2,569 on those 5, each a repeat of an identical packet), so input was priced from reported cache writes, not from the adapter's upper bound.
- Readback: `chain.py verify` was not run. Offline, this review regraded all 744 rows with the study's code and recomputed every stage's totals and saved analysis: all equal; every stage's assignment digest equals the manifest. Not checked: artifact checksums on the hub.
- Corrections to the generated facts: none.

## Interpret the result

- Primary contrast: +20.75 attacker seats (17.33 to 24.21), positive in 24 of 24 roots, identical to attempt 001 by construction: every S1 row has the same id, packet hash and admission outcome in both attempts (checked by `reporting/compare_attempts.py`). Not a new observation.
- Model answers: gpt-6-luna qualified 24 of 24. On attacked packets it was correct on 84.9% (strong checks) and 39.2% (weak) of rare answers against Qwen's 82.9% and 41.5%; it repeated the fabricated value less (9.3% and 49.4% against 14.2% and 55.4%) and returned null more (5.9% and 11.4% against 2.9% and 3.1%). Every wrong answer of both models was the fabricated value. Clean endpoints: both 100%. Same six values on 305 of 504 packets; 23 or 24 of 24 per cell where seats were clean. Per-cell paired differences with root-bootstrap intervals are in RESULTS.md and records/attempt-002/paired-luna-minus-qwen.csv; 8 of 63 cell differences have intervals excluding zero, without multiplicity correction.
- What this does and does not support: a second model family, reasoning at effort low, shows the same qualitative pattern as Qwen (answers follow the seated reports; under weak checks most wrong answers are the fabricated value; clean endpoints perfect), with more abstention where fabricated reports are plentiful. It does not separate model family from reasoning (Qwen ran with reasoning disabled), and one call per packet per model gives no within-model variance.
- Deviations and retrospective analyses: the attempt was planned after attempt 001's results were seen (stated in the preregistration). The paired comparison script `reporting/compare_attempts.py` was written after the run, following the planned description; outside the source hash.

## Assess experiment quality

| Dimension | Status | Finding and evidence | Next action / acceptance check |
|---|---|---|---|
| question | pass | The planned descriptive second-model comparison, written before the code | none |
| scenarios | gap | As attempt 001 (one graph family, audit policy, fabrication) | as attempt 001 |
| controls | pass | Clean endpoints 100% for both models; reference plurality on identical packets | none |
| capability | pass | Qualification 24 of 24 on set a; 528 of 528 valid structures; no answer cut by the 1,500-token limit (output at most 885) | none |
| measurement | gap | Model and reasoning setting confounded; one call per packet | a successor would vary effort within one model |
| sample_size | gap | 24 roots; most per-cell differences have intervals including zero | not a power claim |
| agent_context | pass | Request body exactly the frozen template plus two messages; every response named `gpt-6-luna` | none |
| data_integrity | gap | Rows regraded and totals recomputed offline, all equal; `chain.py verify` not run, hub checksums unchecked | someone with hub access runs the launcher's `verify` at `ca15e8ed`, or compares artifact checksums for runs 2ad24f38, 26b9409b, bf31bec5, f874bc50 |
| resources | pass | 528 calls within caps, USD 0.209 of USD 5, 7 min 8 s | none |
| reproducibility | pass | Records, `reporting/build_report.py --out records/attempt-002` and `reporting/compare_attempts.py` reproduce every number offline | none |
| visualization | unknown | Images not in the records | open the hub frames of run f874bc50 |

## Resolve issues and prior suggestions

| Issue or prior suggestion | Accepted / revised / rejected and why | Evidence / cause confidence | Offline repair or proposed diagnostic | Acceptance check and verified result | Owner / status |
|---|---|---|---|---|---|
| First live use of the reference OpenAI adapter on this study | accepted as working for the paths exercised | 528 calls: model `gpt-6-luna` (undated; no dated id seen); `system_fingerprint` null; `prompt_tokens_details.cache_write_tokens` and `cached_tokens` present; `completion_tokens_details.reasoning_tokens` present (0 to 840); `x-ratelimit-*` headers present (10,000 requests, 10,000,000 tokens per minute); finish `stop` | reference README corrected with these observations | P0 passed on the first call | closed |
| Constant reported input tokens (2,572 on every call, 5,818 to 5,875-byte requests) | accepted as unexplained | Qwen's counts varied 3,033 to 3,101 on the same packets | none; cost depends on it only through input pricing | not applicable to the answers | open, low priority |
| Billing and retry paths of the OpenAI adapter | accepted as an open limit | no 429, 5xx or quota stop in this run | none possible offline | first live occurrence | open, dmarz/openai-route |
| `chain.py verify` not run | accepted as a process gap | claim expired before the operator ran it | offline regrade and recomputation (all equal) | hub-side verify | open, operator |
| 97.2 s call | accepted | one call of 528, inside the 120 s timeout | none | S1 completed | closed |

## Closeout and handoff

- Completed assessment: this file, dmarz/openai-route, 2026-10-04.
- Evidence metadata: one sentence added to the registry row (score unchanged at 1).
- Next decision: `complete-valid-result`; no rerun. The repair fixture set b remains frozen and unused.
- Workers stopped and allocation: the operator reports the chain completed and the server claim released (expired).
