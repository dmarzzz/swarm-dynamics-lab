# discussion-v3-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/v3-q0-opus (orbital-one), server sim-dmarz-9, claim `dmarz-v3-q0-opus`. Not a review. Last updated 2026-10-04T08:20Z.

## 1. Results so far

- Plan, Opus request path and launch record committed 08:11Z (commit eb7a4d3a): attempt `v3o-a1`, one chain of probe, Q0 (6 fresh worlds 54001-54006, 96 cases, 636 calls), software gate, S1 (24 fresh worlds, 276 cases, 2,436 calls). Opus 5.5, adaptive thinking, effort high. Review waived by the owner.
- Server rehearsals (scripted, 0 model calls): Q0 rehearsal 636 of 636 done 08:17:51Z; S1 rehearsal 2,436 of 2,436 at 08:19:54Z. No model call yet.
- Input from the parent run D1-Opus: full-evidence decisions 6 of 6 reused and 12 of 12 fresh; saved-report quorum 4 of 6.

## 2. Gate forecast

Q0 gate (unchanged from `bench_v3.analysis`): execution complete, at least 5 of 6 clean full-evidence diagnostics correct, at least 5 of 6 clean reports-only votes correct.

- Full-evidence gate: pass expected.
- Reports-only gate: open. In D1-Opus all 8 abstentions on the saved (Haiku-written) reports were `choice_claim_incomplete` and 0 were `choice_claim_inconsistent`; every ballot with a complete set of claims was correct. So this gate turns on whether Opus-written reports carry every needed value. Nothing run so far measures that.
- Time and cost at D1-Opus's pace (5.8 s and USD 0.021 per call, one call at a time): Q0 about 60 to 65 minutes and USD 13; S1 about 4 hours and USD 50. If the chain starts by 08:30Z, the gate is decided about 09:35Z and S1 would end about 13:30Z. The claim length should cover that.

## 3. Next run

- **If Q0 passes:** S1 starts in the same process. Nothing needed.
- **If Q0 fails on the reports-only gate:** the plan's fail branch expects ballots abstaining against their own claims and proposes a feasibility line per option before the vote. The D1-Opus breakdown points the other way: Opus did not abstain against its own claims once in 18 ballots; it abstained when the claims it could extract were incomplete. First check in the failed run: `choice_claim_incomplete` against `choice_claim_inconsistent` on the clean reports-only ballots, and whether each needed value appears in at least one of the three reports. If the reports are incomplete, the change to test is the report contract (each report must state every option's constraint values it saw), not the ballot contract. Either change needs fresh worlds and a new attempt.
- **If Q0 fails on execution (invalid, truncated, refused):** compare the ported request body with D1-Opus's, which ran 72 of 72 clean.
- **After S1:** the 24 confirmation worlds 30000-30023 stay closed. The S1 result decides whether a confirmation design is worth writing; that plan can be drafted during S1's four hours.

## 4. Design notes for later runs

- The frozen runner works world by world (`src/bench_v3/runner.py` lines 181-207: exposure order and arm order are shuffled inside each world). The gate therefore becomes certain only at the sixth world, about 65 minutes in, unless two clean misses arrive earlier: two misses in either clean gate make a pass impossible. The hub run reports `clean_accuracy` as it goes; I will read it during Q0 and say so as soon as the gate is decided either way. Putting the clean cases of all six worlds first would decide the gate in about 10 minutes, but that is a change to the frozen runner and belongs in a later version, not this attempt.
- Q0 and S1 run one call at a time. S1's 2,436 calls are 24 independent worlds; two or three workers on the same server would cut four hours to under two without changing any request. That is a launcher change and would need its own rehearsal.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 3, 4 and 7.
