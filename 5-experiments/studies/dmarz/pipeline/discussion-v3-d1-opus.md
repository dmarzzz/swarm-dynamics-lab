# discussion-v3-d1-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/d1-opus (orbital-one), server sim-dmarz-9, claim `dmarz-d1-opus` to 15:44Z. Not a review. Last updated 2026-10-04T08:18Z.

## 1. Results so far

`d1o-a1` finished at 08:00:54Z and **passed the fresh gate**: hub metrics `fresh_justified: 12`, `qualification_passed: 1`.

- 72 of 72 calls terminal, 0 invalid, 0 missing usage, USD 1.47, 7 minutes (07:53:55Z to 08:00:54Z). About 5.8 s and USD 0.020 per call at effort high.
- Fresh gate: 12 of 12 evidence-justified choices on worlds 52001 to 52012 (gate 10 of 12). For comparison, on the six reused full-evidence worlds Haiku was 2 of 6 and Sonnet 3 of 6 in D1. The development comparison (Opus on the same six worlds and the saved-report quorums) is in the audit, which is not on main yet; I have only the hub summary.
- Before the run: rehearsal 72 of 72 scripted, probe `d1o-p1` valid, dmarz's waiver recorded 07:53Z (commit 9315f76a).
- Confidence: 12 of 12 on fresh worlds is a clear pass of this gate. It is 12 clean single-agent decisions, with thinking at effort high. It does not show how Opus behaves in the three-agent swarm arms or under attacked evidence.

### From the audited results (RESULTS.md on main, 08:07Z)

| Measure | Haiku 4.5 (D1) | Sonnet 4.6 (D1) | Opus 5.5 | Denominator |
|---|---:|---:|---:|---|
| Full-evidence correct, reused worlds | 2 | 3 | 6 | 6 |
| Fresh clean full-evidence, worlds 52001-52012 | not run | not run | 12 | 12 |
| Correct post-report ballots | 2 | 8 | 10 | 18 |
| Unnecessary post-report abstentions | 16 | 10 | 8 | 18 |
| Correct three-agent report quorum | 1 | 3 | 4 | 6 |
| Correlated-copies memory fixtures, policy-justified | 0 | 1 | 3 | 6 |

Opus fixed the full-evidence failure completely. It did not fix the reports-only side: 8 of 18 answerable ballots were unnecessary abstentions and two of six worlds (20004, 20005) ended with no quorum. Those ballots were cast on reports written by Haiku in `v3-q0-a1`, so they do not show what Opus does with reports Opus wrote.

## 2. Gate forecast

Done. Passed. Post-mortem verdict: advance. Claim `dmarz-d1-opus` released 08:05:21Z; sim-dmarz-9 is free and has been idle since 08:01Z.

## 3. Next run

Named in the post-mortem: a fresh v3 swarm qualification on Opus, lane `dmarz/v3-q0-opus` on sim-dmarz-9, same shape as `v3-q0-a1` (96 cases, 636 calls), fresh world ids, the D1-Opus request path ported into `bench_v3`, F1/F2 fixes pinned, new manifest, pre-run review and claim. At tonight's pace about 65 minutes and USD 13 at effort high. The plan is on main since 08:11Z as `discussion-dose/v3-opus` (attempt `v3o-a1`, Q0 chained into a 24-world S1); see [discussion-v3-opus.md](discussion-v3-opus.md). An earlier version of this file said no plan was on main; that was out of date by a few minutes.

Forecast for that run's two clean gates (5 of 6 each), from the D1-Opus numbers:

- Clean full-evidence decisions: pass expected (6 of 6 reused, 12 of 12 fresh).
- Clean reports-only votes: **depends on the reports, not the ballots.** On the saved reports Opus reached quorum in 4 of 6 worlds, one short of the gate. I read the ballot breakdown in `records/d1o-a1/summary.json` (group `report_snapshot`): all 8 abstentions are `choice_claim_incomplete` (the ballot's own extracted claims did not cover every needed value), 0 are `choice_claim_inconsistent`, and the 10 ballots with every value extracted are exactly the 10 correct ones. Opus never abstained with a complete set of claims and never cast a wrong vote. In `v3-q0-a1` Haiku abstained despite its own claims identifying a winner in four worlds; Opus shows none of that. The saved reports were written by Haiku and at least one world's reports are known to omit a needed fact (20001 in the Q0 results). So the reports-only gate in the Opus swarm run turns on whether Opus-written reports carry every needed value. Nothing run so far measures that.

Pre-decided branches for the swarm qualification:

- **Both clean gates pass:** the configuration is qualified for the v3 sweep. The sweep's plan (which arms, how many worlds, holdout 30000-30023 stays closed) should be written while the qualification runs.
- **Full-evidence passes, reports-only fails on abstention:** from the D1-Opus breakdown the expected cause is a needed value missing from the reports (report writing), not ballots abstaining against their own claims. Check `choice_claim_incomplete` against `choice_claim_inconsistent` in the new run to confirm. If it is report completeness, the change to test is the report contract (require every option's constraint values), on fresh worlds. Do not change the model.
- **Any invalid, truncated or refused call:** request shape; the D1-Opus adapter ran 72 of 72 clean, so compare the ported `bench_v3` request body with it byte for byte.

Two things that would shorten the loop:

- Dispatch order. If the clean arms run first, both clean gates are decided in roughly the first 100 calls (about 10 minutes). A software stop there saves about 55 minutes and USD 11 when a gate fails, and costs nothing when it passes.
- A cheap pre-check exists for the at-risk gate: the report-writing step alone (6 clean worlds x 3 agents = 18 calls) can be scored for whether every needed value appears in at least one report, before the remaining 600 calls are spent.

## 4. Design notes for later runs

- 60 of the 72 calls are reused development requests and do not count toward the gate. The gate rests on 12 calls, about 75 seconds of this run. A fresh-only screen of 12 to 24 worlds would give the same decision at the same cost and a larger denominator.
- This run and D2 overlap on Opus. D2's operator has recorded this result as context and set its Opus arm to effort high (commit aef218e8).
- Setup for this 8-minute run included a rehearsal, a probe, a preflight that expires in 30 minutes and a wait for a first-hand go. The probe and the run could be one command with the probe as a software gate.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 3 and 4.
