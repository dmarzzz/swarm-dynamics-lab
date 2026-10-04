# Post-mortem: v3-d2-a1

2026-10-04 UTC, by `dmarz/v3-d2-opus`, the agent that built and operated the run. This is the owning agent's own
assessment. `dmarz/fleet-monitor` gave the go as a same-researcher check under dmarz's waiver; nobody independent
reviewed the design, code, arithmetic or this document.

- Study / owner / stage / attempt / parent: `discussion-dose-v3` / dmarz / D2 / `v3-d2-a1` / `v3-d1-a1`.
- [Pre-run assessment](v3-d2-a1-pre.md), [plan and amendment](../benchmark-v3/d2/PLAN.md),
  [results](../benchmark-v3/d2/RESULTS.md), [setup record](../benchmark-v3/d2/SETUP.md). Source commit
  `aef218e8fd19470f74aac7bd5749876711a3038f`, frozen manifest `6c7721976102f3d336a1e203e0fbcabcf4c0830b94ec4f3b431899e8b8bbf82c`.
- Review verdict: **complete_valid_result**, diagnostic scope.
- Execution: passed. Response validity: 72/72. Qualification: not applicable, none claimed. Scientific conclusion:
  exploratory, below. Process compliance: passed with the deviations listed. Artifact delivery: verified by readback.

## Decision

Opus 5.5 passed both screens (6/6 decisions, 18/18 feasibility checks). Sonnet 4.6 and Haiku 4.5 each scored 5/6 and
16/18 and failed both. No successor, qualification, swarm run or holdout was started. The claim on `sim-dmarz-3` was
released after readback.

## Reconcile the recorded facts

| Quantity | Planned | Observed | Missing or uncertain | Evidence |
|---|---|---|---|---|
| Independent units | 6 world clusters, 3 models on identical items | 6, 3 | none | `results/v3-d2-a1/summary.json` |
| Assigned / started / terminal / graded / analyzed | 72 | 72 / 72 / 72 / 72 / 72 | none | exact-source audit: 72 requests verified, 72 outcomes recomputed |
| Per model | 24 | 24 valid each | none | summary |
| Model calls including probe | at most 73 | 73 | none | accounting.json |
| Retries, refusals, truncations, provider failures | 0 permitted retries | 0 / 0 / 0 / 0 | none | per-item.csv |
| Input / output tokens, batch | not predicted | 39,030 / 982 | no cache tokens | summary |
| Spend | reservation 3.387356, cap 5 | batch 0.125037, probe 0.002704, total 0.127741 | list-price calculation, not invoice-reconciled | accounting.json |
| Wall time and concurrency | at most 60 min, one worker | 08:26:06 to 08:27:58 UTC, one worker | none | hub run |

- No duplicate dispatch, exclusion, interrupted or unstarted assignment. Every returned model id matched.
- The reservation was about 27 times the actual cost. It was computed from the full output ceilings; Opus used 551
  output tokens across 24 calls against a ceiling of 4,000 per call.
- Six indexed artifacts were downloaded from the hub and matched server and local bytes. Private archive SHA-256
  `fee5dcdb8166e62bfc6541c7a04516855ec581bb0034765f47268e946ca0387a`.
- The hub run carries the batch cost once. The probe cost is recorded in the results and accounting file only.
- Watchdog: two observations during the paid run, no warnings; timer stopped afterwards.

## Interpret the result

- Primary result: Opus 6/6 and 18/18, with 24 valid answers. Under the rule fixed before the run this is a pass on
  the compact representation and contract. D1-Opus had already passed a fresh gate on D1's packaging, so this adds
  that Opus is at ceiling on the compact format too. It does not qualify Opus for anything.
- Comparison arms: Sonnet and Haiku 5/6 and 16/18 each, both screens failed. Feasibility is above the 12/18
  always-infeasible baseline. Both models' false positives are the same two items, the only two options whose
  summed cost exceeds the budget. Each model's single wrong decision is on a world where its three feasibility
  answers were all correct, and the choice derived from each model's own answers is correct in 6/6 worlds.
- Controls: the scripted controls behaved as predicted in the rehearsal (6/6 and 18/18; 0/6 and 12/18; 2/6 and
  6/18), so the scorer discriminates. The always-feasible control's 2/6 shows that a decision count near that level
  would carry little information; the observed 5/6 and 6/6 are well above it.
- Supported claim: on these six worlds and this contract, in one response per item, Opus made no error and the two
  smaller models erred on the summed-budget predicate and on one selection each.
- Not supported: that the compact format repairs Haiku or Sonnet (they still fail the screens); that the format
  caused their improvement from D1 (different requests, single responses, no repeats); that thinking is what
  separates Opus (model, thinking, sampling and ceiling differ together); anything about fresh worlds or swarms.
- Observed versus suspected: the location of the errors is observed. That the smaller models mis-add or skip the
  sum when answering without thinking is a suspicion. It was not tested by a discriminating check.
- Expected versus observed: the pre-run expectation was that Opus passes; it did. The comparison arms landing on
  identical feasibility vectors was not anticipated.

## Assess experiment quality

| Dimension | Status | Finding and evidence | Next action or acceptance check |
|---|---|---|---|
| question | pass | The diagnostic question was fixed in the plan before any model output and the reading table was applied as written | none |
| scenarios | gap | Six reused development worlds, one feasible option each, only two options with a sum over budget | A follow-up needs fresh worlds with more sum-violating options and several feasible options |
| controls | pass | Known-answer controls through the real execute, score and audit path, in tests and in the hub rehearsal | none |
| capability | pass for Opus, fail for comparison arms | Opus 24/24 correct; Sonnet and Haiku fail both screens | The comparison arms' failure is a result, not a defect |
| measurement | pass | Strict schema, gold from two agreeing predicate implementations plus direct arithmetic in the selftest; the per-item rule checks in the results were redone by hand | none |
| sample_size | gap | One response per item; a one-item difference is a single response | Repeats per item before any claim about stable error rates |
| agent_context | pass | Each call isolated and stateless; requests verified against the frozen manifest by the audit; no gold field in any input | none |
| data_integrity | pass | Hash-chained journal, exact-source audit, hub readback, private archive | none |
| resources | pass | USD 0.127741 of a USD 5 cap; exclusive claim; one worker | none |
| reproducibility | pass with limit | Pinned commit, frozen manifest, published per-item table. Opus runs without a fixed sampling setting, so a rerun may differ | none |
| visualization | pass for scope | Counter timeline on the hub (37 points per series), final counters equal the 72 saved records. No animation by design | none |

## Deviations and issues

| Issue | Disposition | Evidence | Status |
|---|---|---|---|
| Launch route: run from halcyon on an existing server instead of the orbital-one run queue | The reviewer states that Dan told the fleet monitor directly to pick two stopped experiments and run them on this machine as managed sub-agents, overriding the run-queue default. The pinned plan called the instruction relayed and unconfirmed by this agent; this corrects that record | Go message from `dmarz/fleet-monitor`, 2026-10-04 | closed |
| Go time: the go message says 08:28 UTC; the operator clock read 08:25:14 UTC when it arrived | The preflight evidence records 08:25:14Z from the operator clock. Both times are in accounting.json | accounting.json | closed, noted |
| Hub rehearsal injected no provider failure | The failure path and failed hub status are covered by offline tests only. No failure occurred in the paid run, so the path stayed unexercised on the hub | selftest | open, low |
| Pre-run text said public tables hold scores and accounting only | The per-item table also publishes each one-letter or boolean answer, as the reviewer asked for a per-item table. Raw text and journals stay private | RESULTS.md | closed, noted |
| Opus effort `high` chosen to match D1-Opus | Opus returned bare-answer-sized output on 17 of 24 items, so the effort setting mattered on at most 7 | per-item.csv | closed |
| Opus input token counts 626 to 742 against 458 to 550 for the same content | Not investigated | per-item.csv | open, informational |
| Reservation 27 times actual cost | Worst-case by design; no action | accounting.json | closed |
| Comparison-arm refusals and unexpected blocks share one failure reason | No such failure occurred | summary | closed for this run |
| `experiment_evidence.py --check` fails on main for other agents' unregistered studies | Not mine to edit; only this run's block and index line were rendered | registry | open, not this lane |

## Closeout and handoff

- Evidence metadata updated for this cohort: score 1 (exploratory), claim and sample size in the registry.
- No successor is proposed for launch here. If the Haiku and Sonnet line is pursued, the discriminating check is a
  set of fresh worlds with many sum-over-budget options, repeated responses per item, and the same models with and
  without thinking. That would need dmarz's decision and its own plan. With Opus as the model going forward and
  already past its gate, D2 does not block the Opus swarm qualification.
- Workers stopped, watchdog stopped, artifacts verified, claim `dmarz-discussion-v3-d2` released.
