# Post-mortem for trust-credit-qwen, chain-001 (S0, P0, Q0, S1)

Status: scientific assessment completed by the owning builder on 2026-10-04. It is the builder's own review; no independent review took place. Follows [the review cycle](../../../../../tooling/agent-experiments/RUN-REVIEW.md) and [the quality rubric](../../../../../tooling/agent-experiments/RUN-QUALITY.md).

- Study / owner / stage / attempt / parent / assessed at: trust-credit-qwen (research program v5, line T) / dmarz / S0, P0, Q0, S1 / chain-001 / no parent attempt / 2026-10-04.
- Assessor and scope of this review: dmarz/pipeline-split, the builder of the package, working offline from the run's saved records. The run was operated by dmarz/fleet-monitor (run queue 270, server sim-dmarz-8). Cross-researcher review was waived by dmarz for these exploratory runs; dmarz/fleet-monitor's check before the run was a same-researcher check. Nothing here is an independent review.
- Pre-run assessment, frozen plan, source, model and manifest: [chain-001-pre.md](chain-001-pre.md); [preregistration](../preregistration.md) with amendment A1; launch commit `e5f34521799e147fe4a77ed2d86bf2bdcc1a8eb1`, code commit `d3219ceb`, source hash `e24e85f52867232cfc1e673e601a1af1be5e092339bb393d1c68a7e4af726209` (the run's recorded hash equals the current code's); `qwen/qwen3.7-flash` via OpenRouter, provider Alibaba, reasoning disabled; manifest digest `e09119d1…` (every stage's saved assignments reproduce their manifest digest).
- Native outcomes and durable artifacts: [records/](../records/) (chain status, per-stage summaries and analyses, gzipped rows, assignments and audits, the launcher's verify output, recomputed numbers); results in [RESULTS.md](../RESULTS.md). Frames and the replay are on the hub; they were not part of the records handed to this review.
- Review verdict: **complete_valid_result**.
- Execution: complete. Response validity: 528 of 528 valid. Qualification: passed (24 of 24). Scientific conclusion: exploratory, scripted primary positive, with a level caveat. Process compliance: plan, amendment and pre-run review preceded the run; same-researcher check only. Artifact delivery: `verify` exit 0 on the server; images not inspected in this review.

## Reconcile the recorded facts

| Quantity | Assigned or planned | Observed | Missing, partial or uncertain | Evidence |
|---|---|---|---|---|
| Independent roots and paired cells | 24 comparison roots × 21 cells; 8 qualification roots × 3 shapes; 8 engineering roots (scripted) | 24 roots, all 21 cells each; 24 fixtures; 8 engineering roots | none | records/s1-episodes.jsonl.gz, s1-assignments.jsonl.gz |
| Started / terminal / graded / analyzed, S0 | 216 | 216 / 216 / 216 / 216 | none | records/s0-summary.json |
| Started / terminal / graded / analyzed, P0 | 1 | 1 / 1 / 1 / 1 | none | records/p0-summary.json |
| Started / terminal / graded / analyzed, Q0 | 23 | 23 / 23 / 23 / 23 | none | records/q0-summary.json |
| Started / terminal / graded / analyzed, S1 | 504 | 504 / 504 / 504 / 504 | none | records/s1-summary.json |
| Model calls, including retries | caps 1, 23, 504; 640 transport attempts | 1, 23, 504 calls; 528 transport attempts (one per call); no retry; no billing pause; 0 voided | none | records/chain-status.json (ledger) |
| Input / output / reasoning tokens | byte bound at most 3.13 M input | 1,620,024 input; 29,209 output; reasoning 0 on every call | cached tokens are not recorded by the adapter | records/report-numbers.json |
| Actual spend / retained reservations / cap | expected about USD 0.05; cap USD 2 | USD 0.052047 settled; no unsettled reservation | none | ledger totals in chain-status.json |
| Wall time, concurrency, machine | S1 6 to 13 minutes expected; 4 in flight | chain 11:33:17Z to 11:37:39Z (4 min 22 s); S1 worker 213.8 s; sim-dmarz-8 | none | chain-status.json, verify-summary.json |

- Reconciliation differences, duplicates, exclusions, interrupted or unstarted assignments: none. Every assignment id occurs once; no row is excluded from any analysis.
- Cost estimate versus actual: estimate USD 0.045 to 0.05, actual USD 0.0520 including qualification. The provider reported a cost on all 528 calls: equal to the snapshot-price computation on 523 and lower on 5 (30% to 32% of it). The cause of the 5 lower costs is not known; the adapter does not record cached-token counts.
- Readback: `python src/chain.py verify` on the server returned exit 0 with all 15 checks true in each of the four stages (artifact checksums against the hub, every grade, totals, gates, outcomes and the analysis recomputed). Offline, this review regraded all 744 rows and recomputed totals and analyses from the records with the same code: all equal.
- Corrections to the generated facts: none.

## Interpret the result

- Primary contrast: +20.75 attacker seats (root-bootstrap interval +17.33 to +24.21), 24 independent roots, positive in all 24. There was no pre-set useful-size threshold for this line; the prediction was positive and of the order of +20.
- Secondary and sensitivity: against `anchors` +26.83; at 64 checks +12.50; under weak checks +6.58 (1.75 to 11.13, positive in 15 of 24 roots). Levels: under strong checks `direct` seats 19.58, 17.00, 10.38 attacker identities at 32, 64, 108 checks against 4.38, 14.29, 15.92 under `propagated`. No outcome is missing, so bounds equal estimates.
- Manipulation, competence, controls, difficulty: the manipulation occurred as specified. `check_root` ran on the 24 comparison roots before the first S1 call and found no violation (audit identical across rules, pass-credit mass equal, seats, badges and row order held). Clean competence: 24 of 24 fixtures exactly right, including null on all 8 withheld facts. Controls discriminated: `anchors` shows no escalation under weak checks (−0.08) and a fall under strong checks; clean endpoints are 100% correct under all three rules while the same seats with fabricated reports give 35% to 46% correct. Truth availability was at its ceiling (1.00 in 17 of 18 cells) and did not discriminate.
- Supported claim: in this simulator, the rise of attacker seats with the coverage budget under strong checking appears with propagated pass credit and not with direct or no pass credit. Unsupported: that direct credit is safer (it seats more than four times as many attacker identities at 32 checks and yields worse answers there); anything about model agents, other graph families, audit policies or published defenses.
- Observed versus suspected versus verified: observed, the seat counts and answer profiles in RESULTS.md. Suspected, not verified: that propagation at small budgets helps by lifting honest specialists near passed identities. Verified by a discriminating check: the wrong answers under weak checks come from fabricated reports, not from seat composition (clean endpoints).
- Deviations and retrospective analyses: none in execution. Computed after the run and labelled as such in RESULTS.md: the dangling-rule audit on the comparison roots, the counts of roots where one rule seats more than the other, the share of wrong answers equal to the fabricated value, the pooled model-versus-reference profile and the repeated-packet agreement. The comparison assignments were generated before the run to build the manifest; the builder did not look at their admission outcomes until the records arrived.

## Assess experiment quality

| Dimension | Status | Finding and evidence | Next action / acceptance check |
|---|---|---|---|
| question | pass | One question and one primary, fixed before the run (preregistration items 1 and 7) | none |
| scenarios | gap | One graph family, one audit policy, one fabrication, one population size; the two counterfactual rules were written for this study | a successor would vary the graph family and add a published defense; not planned here |
| controls | pass | `anchors` rule, clean endpoints, reference plurality on identical packets; all behaved as controls should (above) | none |
| capability | pass | Qualification 24 of 24 on the exact packet format and size; 528 of 528 valid structures | qualification did not cover ties or conflicting evidence; the model's 3.0% abstention against the reference's 20.8% is an outcome, not a defect |
| measurement | gap | Seats are exact and scripted; truth availability is at ceiling and uninformative; the primary measures escalation, not level, and RESULTS.md leads with that | report levels beside the primary in any reuse of the number |
| sample_size | gap | 24 development-sized roots; primary positive in 24 of 24; weak-check contrast and model contrasts have wide intervals | not a power claim; a successor would size from these root-level spreads |
| agent_context | pass | The request body is the frozen template plus two messages; packets contain no evaluator field (asserted before S1); every response named model and provider | none |
| data_integrity | pass | Every row regraded, every total and analysis recomputed, manifest digests reproduced, verify exit 0 | none |
| resources | pass | 528 of 528 calls within caps, USD 0.052 of a USD 2 cap, 4 min 22 s | none |
| reproducibility | pass | Records and `reporting/build_report.py` reproduce every number offline; source hash pinned | none |
| visualization | unknown | The hub holds the frames and the replay (verify: every artifact present with matching checksum; 11 replay frames recorded in the summary); the images were not in the records given to this review. A frame re-rendered offline from the saved S1 rows shows the same primary, interval and cell bars as the analysis | someone with hub access opens `final_frame.png` and `replay.gif` of run d9c433dd and compares them with records/s1-analysis.json |

## Resolve issues and prior suggestions

| Issue or prior suggestion | Accepted / revised / rejected and why | Evidence / cause confidence | Offline repair or proposed diagnostic | Acceptance check and verified result | Owner / status |
|---|---|---|---|---|---|
| First live use of the reference OpenRouter adapter | accepted as working for the paths exercised | 528 calls: `provider` field present and `Alibaba`; `usage.cost` present on every call; model slug returned as `qwen/qwen3.7-flash` (not the dated form); `completion_tokens_details.reasoning_tokens` 0; finish reason `stop`; 0.514 to 0.520 tokens per byte | none needed | P0 passed on the first call; no failure category occurred | closed |
| Billing-error wording and the retry paths remain unverified against the live service | accepted as an open limit | no 402, 429 or 5xx occurred in this run | none possible offline | first live occurrence in any study using the adapter | open, dmarz/pipeline |
| Five calls billed below the snapshot price | accepted as unexplained | provider-reported cost 30% to 32% of the computed cost on 5 of 528 calls | record cached-token usage fields in the adapter if a later study needs to explain it | not applicable to this result (cost only) | open, low priority |
| Level caveat (direct credit seats more attacker identities at small budgets) | accepted; stated first in RESULTS.md, README and the pre-run review | measured on 24 roots: 19.58 against 4.38 at 32 checks | none | present in the write-up | closed |
| Truth availability at ceiling | accepted as a measurement gap | 1.00 in 17 of 18 cells | a successor would use scarcer truthful carriers | not applicable here | open for any successor |
| Images not reviewed | accepted as a gap of this review | records came without images | see visualization row | pending | open |

## Closeout and handoff

- Completed assessment: this file, dmarz/pipeline-split, 2026-10-04. No structured review file was produced.
- Evidence confidence and sample-size metadata: updated in the registry for this cohort (score 1, exploratory: a scripted mechanism result on one synthetic task with one model configuration answering the packets).
- Remaining gaps: visual audit of the hub images; billing and retry paths of the adapter unexercised.
- Next decision: `complete-valid-result`. No rerun and no repair attempt. The pre-registered repair attempt (002) was not needed and is closed unused.
- Successor: none proposed here. If one is wanted, it needs its own plan and the owner's approval.
- Owner update approval: not requested; nothing further is proposed for launch.
- Workers stopped, artifacts verified, allocation: the launcher reports no active chain or worker; verify exit 0; the operator reports the server claim released.
