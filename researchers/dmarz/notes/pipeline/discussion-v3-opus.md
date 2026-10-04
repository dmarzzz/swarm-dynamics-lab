# discussion-v3-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/v3-q0-opus (orbital-one), server sim-dmarz-9, claim `dmarz-v3-q0-opus`. Not a review. Last updated 2026-10-04T08:58Z.

## 1. Results so far

- Plan, Opus request path and launch record committed 08:11Z (commit eb7a4d3a): attempt `v3o-a1`, one chain of probe, Q0 (6 fresh worlds 54001-54006, 96 cases, 636 calls), software gate, S1 (24 fresh worlds, 276 cases, 2,436 calls). Opus 5.5, adaptive thinking, effort high. Review waived by the owner.
- Server rehearsals (scripted, 0 model calls): Q0 rehearsal 636 of 636 done 08:17:51Z; S1 rehearsal 2,436 of 2,436 at 08:19:54Z. No model call yet.
- Input from the parent run D1-Opus: full-evidence decisions 6 of 6 reused and 12 of 12 fresh; saved-report quorum 4 of 6.

## 2. Gate forecast

**The Q0 gate's two clean conditions are already met.** Attempt `v3o-a2` (which replaced `v3o-a1`; a1 made one probe call only) dispatches the gate cases first and wrote an `early_gate` event to its journal (read on the server at 08:56Z, read-only): clean full-evidence 6 of 6, clean reports-only 6 of 6, 0 call failures, `passed: true`. Q0 started about 08:35Z; at 08:56Z it was at 175 of 636 calls and 20 of 96 cases, 0 invalid, USD 6.

- What remains for the gate is execution completeness over the other 461 calls. Forecast: pass.
- The reports-only question from D1-Opus is answered: with Opus-written reports, all six clean reports-only swarms reached the correct decision (D1-Opus on Haiku-written reports: 4 of 6).
- Timing: 7 to 9.5 calls per minute, so Q0 ends about 09:45Z to 10:00Z and S1 starts in the same process. Cost USD 0.033 per call: Q0 about USD 21, S1 about USD 80.
- S1 at this pace is 2,436 calls in 4.3 to 5.8 hours, ending about 14:30Z to 15:45Z. Check the claim's expiry against that.

Early descriptive reading from the clean worlds so far (3 of 6 worlds, not a result): the reports-only arm decided correctly in all six, while the independent, private-work and board arms abstained in 7 of the 8 clean cases finished so far. The hub's `clean_accuracy` (0.58 at 18 cases) reflects those abstentions, not the gate.

## 3. Next run

- **Q0 pass expected:** S1 starts in the same process. Nothing needed.
- **If Q0 fails on the reports-only gate:** the plan's fail branch expects ballots abstaining against their own claims and proposes a feasibility line per option before the vote. The D1-Opus breakdown points the other way: Opus did not abstain against its own claims once in 18 ballots; it abstained when the claims it could extract were incomplete. First check in the failed run: `choice_claim_incomplete` against `choice_claim_inconsistent` on the clean reports-only ballots, and whether each needed value appears in at least one of the three reports. If the reports are incomplete, the change to test is the report contract (each report must state every option's constraint values it saw), not the ballot contract. Either change needs fresh worlds and a new attempt.
- **If Q0 fails on execution (invalid, truncated, refused):** compare the ported request body with D1-Opus's, which ran 72 of 72 clean.
- **After S1:** the 24 confirmation worlds 30000-30023 stay closed. The S1 result decides whether a confirmation design is worth writing; that plan can be drafted during S1's four hours.

## 4. Design notes for later runs

- The frozen runner works world by world (`src/bench_v3/runner.py` lines 181-207: exposure order and arm order are shuffled inside each world). The gate therefore becomes certain only at the sixth world, about 65 minutes in, unless two clean misses arrive earlier: two misses in either clean gate make a pass impossible. The hub run reports `clean_accuracy` as it goes; I will read it during Q0 and say so as soon as the gate is decided either way. Putting the clean cases of all six worlds first would decide the gate in about 10 minutes, but that is a change to the frozen runner and belongs in a later version, not this attempt.
- Q0 and S1 run one call at a time. S1's 2,436 calls are 24 independent worlds; two or three workers on the same server would cut four hours to under two without changing any request. That is a launcher change and would need its own rehearsal.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 3, 4 and 7.
