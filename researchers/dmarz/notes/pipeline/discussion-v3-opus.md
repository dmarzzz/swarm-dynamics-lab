# discussion-v3-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/v3-q0-opus (orbital-one), server sim-dmarz-9, claim `dmarz-v3-q0-opus`. Not a review. Last updated 2026-10-04T10:19Z.

## 1. Results so far

- Plan, Opus request path and launch record committed 08:11Z (commit eb7a4d3a): attempt `v3o-a1`, one chain of probe, Q0 (6 fresh worlds 54001-54006, 96 cases, 636 calls), software gate, S1 (24 fresh worlds, 276 cases, 2,436 calls). Opus 5.5, adaptive thinking, effort high. Review waived by the owner.
- Server rehearsals (scripted, 0 model calls): Q0 rehearsal 636 of 636 done 08:17:51Z; S1 rehearsal 2,436 of 2,436 at 08:19:54Z. No model call yet.
- Input from the parent run D1-Opus: full-evidence decisions 6 of 6 reused and 12 of 12 fresh; saved-report quorum 4 of 6.

## 2. Gate forecast

**Q0 passed at 09:50:35Z**: 636 of 636 calls, 96 of 96 cases, 0 invalid, replay-audited, clean full-evidence 6 of 6, clean reports-only 6 of 6, USD 22.68, 76 minutes. S1 `v3o-a2-s1` started in the same process: 7 of 2,436 calls at 09:51:22Z.

- S1 has no gate. 2,436 calls at Q0's pace (8.4 calls per minute, 6,743 input and 550 output tokens per call, USD 0.036 per call): about 4.8 hours, ending about 14:40Z, about USD 87. Input rate about 0.06M tokens per minute, negligible against the 5M limit.
- The early gate was decided at 08:44Z from the journal, 66 minutes before the hub showed the pass. The reports-only question from D1-Opus is answered: with Opus-written reports all six clean reports-only swarms reached the correct decision (4 of 6 on Haiku-written reports).
- Descriptive, from Q0's hub metrics: `clean_accuracy` 0.375 over all clean arms, 11 parent-unsupported cases, 0 parent inherited errors. The reports-only arm is at 6 of 6 while the other clean arms mostly abstain, so S1 has spread between arms and is not at ceiling.

**About 10:10:30Z to 10:10:48Z: 61 calls failed with `provider_credit_balance_low`.** The S1 journal has 61 consecutive `provider_failure` events with that reason, starting at the 206th call and touching 7 of the 24 worlds (54101, 54119 to 54124); the calls after the burst succeeded. The run does not retry or restart, so the cases those calls belong to are incomplete in this attempt. At 10:12Z S1 was at 279 of 2,436 calls with `invalid_calls` 61. **The operator stopped S1 at 10:14:26Z** (291 calls dispatched, USD 6.81) and will relaunch it as a new dated attempt on fresh worlds. Reported to dmarz/fleet-monitor at 10:14Z with the choice: stop and restart S1 on fresh worlds now (about USD 6 and 20 minutes lost) or let it run with a block of invalid cases among the first of 24 worlds.

## 3. Next run

- **S1 is running.** Nothing needed until about 14:40Z. A provider failure is recorded and the run continues; 429 and 529 are retried twice.
- **If Q0 fails on the reports-only gate:** the plan's fail branch expects ballots abstaining against their own claims and proposes a feasibility line per option before the vote. The D1-Opus breakdown points the other way: Opus did not abstain against its own claims once in 18 ballots; it abstained when the claims it could extract were incomplete. First check in the failed run: `choice_claim_incomplete` against `choice_claim_inconsistent` on the clean reports-only ballots, and whether each needed value appears in at least one of the three reports. If the reports are incomplete, the change to test is the report contract (each report must state every option's constraint values it saw), not the ballot contract. Either change needs fresh worlds and a new attempt.
- **If Q0 fails on execution (invalid, truncated, refused):** compare the ported request body with D1-Opus's, which ran 72 of 72 clean.
- **After S1:** the 24 confirmation worlds 30000-30023 stay closed. The S1 result decides whether a confirmation design is worth writing; that plan can be drafted during S1's four hours.

## 4. Design notes for later runs

- The frozen runner works world by world (`src/bench_v3/runner.py` lines 181-207: exposure order and arm order are shuffled inside each world). The gate therefore becomes certain only at the sixth world, about 65 minutes in, unless two clean misses arrive earlier: two misses in either clean gate make a pass impossible. The hub run reports `clean_accuracy` as it goes; I will read it during Q0 and say so as soon as the gate is decided either way. Putting the clean cases of all six worlds first would decide the gate in about 10 minutes, but that is a change to the frozen runner and belongs in a later version, not this attempt.
- Q0 and S1 run one call at a time. S1's 2,436 calls are 24 independent worlds; two or three workers on the same server would cut four hours to under two without changing any request. That is a launcher change and would need its own rehearsal.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 3, 4 and 7.
