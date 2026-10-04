# soc07-private-judgments: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/orbital-orchestrator (orbital-one), run-queue 141, server sim-dmarz-8, claim `dmarz-soc07-private` to 11:50Z. Not a review. Last updated 2026-10-04T09:41Z.

## 1. Results so far

- Manifest m1, Haiku 4.5: S1-Q 7 of 12 correct (gate 10), 12 of 12 valid. Failed 05:03Z.
- Manifest m2, Sonnet 4.6, thinking off, temperature 0.7: S0 `s0-a3` 69 of 69 checks; S1-Q.1 (run 5f681258) **9 of 12 correct, 12 of 12 valid, gate failed** at 07:36:22Z. USD 0.032. All three misses are cost worlds (cost 3 of 6, feasibility 6 of 6).
- Manifest m3 (amendment A6, commit b2bc66a5, 07:55Z): Opus 5.5, adaptive thinking at effort medium, a 4,096-token reasoning allowance added on top of each phase cap (`src/protocol.py` line 85), no temperature, study cap USD 500 (375 public, 125 auxiliary), qualification set 2. S0 `s0-a4` under m3 (run 83013f20) passed at 08:06:15Z: 69 of 69 checks, 0 model calls, 6 min 40 s. The operator then committed the instrument repair below (commit 71717def: the rule now ends "An option meets the deadline if its delivery is at or before the deadline.") and S0 `s0-a5` (run 00e03ba4) started about 08:10:47Z on the repaired prompt.

### Why Sonnet missed (offline check, no model calls)

A sub-agent of this lane regenerated both qualification sets from the study's generator at the approved source hash (`475140d4…`; ids, kinds, regimes and correct labels all match the post-mortem tables) and worked the Sonnet cost worlds by hand from the rendered prompts. I spot-checked the cited lines; I did not rerun the regeneration myself. The answer texts are on the server (`journal-s1q.1.jsonl`) and have not been read, so the causes below are consistent with the records, not confirmed by them.

| World | Result | Superseding audit | Latest values | Correct | Margin |
|---|---|---|---|---|---|
| w0000 | miss (B) | A delivery 10 to 5 (deadline 5) | A cost 82, B cost 84, B delivery 3 | A | 2 |
| w0001 | miss (B) | B cost 57 to 99 | A cost 95, both 3 days | A | 4 |
| w0008 | miss (A) | A cost 52 to 96 | B cost 95 | B | 1 |
| w0002 | correct | A delivery 6 to 3 | A 45, B 58 | A | 13 |
| w0006 | correct | A delivery 7 to 5 | A 57, B 51 | B either way | 6 |
| w0007 | correct | A delivery 9 to 2 | A 32, B 52 | A | 20 |

- w0001 and w0008 are well posed. The only reading that gives the model's answer is using the superseded estimate. They are the only two worlds in the set where the audit changes a cost, and both end with a narrow margin.
- **w0000 depends on a rule the prompt does not state.** The rule text is "choose the lowest-cost option among those that meet the delivery deadline" (`src/prompts.py` line 6). The generator and scorer treat delivery equal to the deadline as meeting it (`src/generate.py` line 48, `src/score.py` line 29, both `<=`). Read strictly (delivery must be under the deadline), the answer is B, which is what the model gave. Against this: Sonnet answered w0009 correctly, and that world needs the `<=` reading.
- Post-hoc pattern with no mechanism: in 7 of the 8 misses across both failed sets the superseding audit was record `e04`, against 3 of 16 correct answers.
- The output schema puts `choice` first and `justification` after (`src/prompts.py` lines 33-34), so without reasoning the model commits before it can work the numbers. m3's adaptive thinking removes that constraint.

## 2. Gate forecast

**S1-Q.2 passed at 08:24:02Z: 12 of 12 correct, 12 of 12 valid** (run a80d0c73, Opus 5.5 at effort medium, repaired prompt, qualification set 2). USD 0.053, about USD 0.0045 per call. S0 `s0-a5` had passed at 08:17:19Z and dmarz's go for S1-Q.2, S1-R and S1-L was recorded at 08:17Z. S1-R (`s1r-a1`, run 807dfab8) started at 08:24:25Z, 23 seconds after the gate.

Three cohorts on this gate: Haiku 7 of 12, Sonnet 9 of 12 (both without reasoning, on the unrepaired prompt), Opus 12 of 12 (with reasoning, on the repaired prompt). Model, reasoning and the prompt clause all changed between the second and third, so the improvement cannot be assigned to one of them.

**S1-R passed at 08:56:43Z** (run 807dfab8): 192 of 192 episodes, 672 calls, 0 failures, valid rate 1.0, USD 5.24, 32 minutes. Team success 1.00 in the private arm and 1.00 in the public arm; private minus public +0.000. S1-L (`s1l-a1`, run 92e1c0d5) started from the chain at about 08:57Z: 425 calls and 25 episodes by 09:01Z, 0 failures, about 110 calls per minute.

**S1-L finished at 09:39:32Z** (run 92e1c0d5): 240 of 240 episodes, 4,080 calls, 0 failures, valid rate 1.0, USD 32.60, 42 minutes. Team success 1.00 private, 1.00 public; private minus public +0.000. All software gates passed.

**The result is at ceiling and carries no information about the question.** Every team was correct in both arms in S1-R and again in S1-L, so the difference could not have been anything but zero. Report it as "at ceiling on Opus 5.5 with reasoning", not as "publication of first answers makes no difference". Study total: 4,788 Opus calls, USD 37.9, plus USD 0.04 on the two failed qualifications.

## 3. Next run

The successor exists: **soc07-private-judgments-v2** (commit 1649757f, 09:31Z, prepared and not launched). It changes the task, not the model: three options, eleven records, two audits (one pattern where the first audit alone points to a wrong option), cost margins 1-2 / 3-5 / 6-9, a deadline-boundary world in every third world, a manipulation check on first-answer disagreement, a one-call probe stage, all stages chained under software gates. Its paid stages are held until sybil-scale-xl's S1 has finished, because of the shared rate limit. See the v2 row in [INDEX.md](INDEX.md).

One gap in v2 as prepared (sent to dmarz/fleet-monitor at 09:42Z): the only new stop, `s1_informative`, is evaluated inside S1-L after its 4,080 calls, and it measures first-answer disagreement, which the minority regimes produce by construction. It does not catch what happened here. A gate at the end of S1-R (if team success is 1.00 in both arms in every regime, S1-L does not start) would have saved 42 minutes and USD 33 in v1 and costs nothing to add before launch.

## 4. Design notes for later runs

- S1-Q is 12 calls and 40 seconds; each manifest costs a fresh S0 (7 minutes), an approval and a new world set. Two model swaps took about 2.5 hours of wall time for 24 model calls. Reading the answer text after the first failure would have cost less than the second manifest.
- A 10 of 12 gate is noisy: a solver that is right 90% of the time fails it about 11% of the time, and one that is right 85% of the time fails about 26% of the time.
- S0 replays 1,500 scripted episodes for every manifest. When an amendment touches only the manifest block and the adapter, a shorter S0 covering those paths would do.
- Deciding the budget and caps for the whole ladder before the qualification (as A6 did) is the right order; see LESSONS item 1.

- The qualification only has a floor. Haiku and Sonnet failed it from below; Opus with reasoning passes it at 12 of 12 and then sits at 100% in the team stage. A gate with a ceiling as well as a floor would have flagged this before S1-R and S1-L.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 1, 3, 6 and 9.
