# soc07-private-judgments: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/orbital-orchestrator (orbital-one), run-queue 141, server sim-dmarz-8, claim `dmarz-soc07-private` to 11:50Z. Not a review. Last updated 2026-10-04T08:10Z.

## 1. Results so far

- Manifest m1, Haiku 4.5: S1-Q 7 of 12 correct (gate 10), 12 of 12 valid. Failed 05:03Z.
- Manifest m2, Sonnet 4.6, thinking off, temperature 0.7: S0 `s0-a3` 69 of 69 checks; S1-Q.1 (run 5f681258) **9 of 12 correct, 12 of 12 valid, gate failed** at 07:36:22Z. USD 0.032. All three misses are cost worlds (cost 3 of 6, feasibility 6 of 6).
- Manifest m3 (amendment A6, commit b2bc66a5, 07:55Z): Opus 5.5, adaptive thinking at effort medium, a 4,096-token reasoning allowance added on top of each phase cap (`src/protocol.py` line 85), no temperature, study cap USD 500 (375 public, 125 auxiliary), qualification set 2. S0 `s0-a4` under m3 (run 83013f20) passed at 08:06:15Z: 69 of 69 checks, 0 model calls, 6 min 40 s.

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

S0 is done. Next is the approval record for m3, then S1-Q.2 (12 calls, under a minute). Nothing is running as of 08:08Z. Gate 10 of 12 correct, 11 of 12 valid.

Forecast: more likely to pass than m2, because two of the three Sonnet misses are single-call override slips that reasoning addresses. Not safe: under the strict deadline reading the answer flips in 1 of the 12 set-2 worlds, so the model starts with one world that can go either way and a margin of two.

## 3. Next run

**Before S1-Q.2:** S0 `s0-a4` ran on the prompt without the clause (`src/prompts.py` line 6 is unchanged on main at 08:03Z). Adding it now means repeating S0 (7 minutes). Leaving it means one ambiguous world in S1-Q.2 and, even on a pass, 3 of 24 S1-R worlds and 4 of 24 S1-L worlds scored on an unstated rule. The fix: add one clause to the rule, for example "delivery at or before the deadline", and record it in amendment A6 as an instrument repair. It changes the prompts hash. After S1-Q.2 it would cost another S0, approval and S1-Q on a new world set, because `execution.json`, `design.json` and the prompt files are all in the fingerprint the approval is bound to (`src/config.py` lines 80-96, `src/launch.py` line 31) and a spent set's call ids cannot be reused (`src/budget.py` lines 69-70). Exposure if it is left: 1 of 12 worlds in set 2, 3 of 24 in S1-R, 4 of 24 in S1-L.

**If S1-Q.2 passes (at least 10 of 12):** S1-R (up to 672 calls) then S1-L (up to 4,080) are authorized stages with software gates (clean competence 13 of 16, parse-valid 95%, truncation at most 5% per phase). The post-mortem promised dmarz a cost estimate from S1-Q.2's tokens before S1-R; with the cap at USD 500 that is a report and need not be a wait. Chain S1-Q.2 into S1-R under the gate.

**If S1-Q.2 fails:**
- 9 of 12 with the miss on the equal-to-deadline world and the clause not added: instrument, not model. Add the clause and rerun on set 3.
- Misses on cost-audit worlds again with reasoning on: read the answer text first (it is in the journal). A third model swap is not the next step.
- `truncated` or `unexpected_content_blocks` failures: request shape. The adapter's adaptive path has only been exercised against a fake transport; the first real call is the test.

## 4. Design notes for later runs

- S1-Q is 12 calls and 40 seconds; each manifest costs a fresh S0 (7 minutes), an approval and a new world set. Two model swaps took about 2.5 hours of wall time for 24 model calls. Reading the answer text after the first failure would have cost less than the second manifest.
- A 10 of 12 gate is noisy: a solver that is right 90% of the time fails it about 11% of the time, and one that is right 85% of the time fails about 26% of the time.
- S0 replays 1,500 scripted episodes for every manifest. When an amendment touches only the manifest block and the adapter, a shorter S0 covering those paths would do.
- Deciding the budget and caps for the whole ladder before the qualification (as A6 did) is the right order; see LESSONS item 1.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 1, 3 and 6.
