# discussion-v3-d1-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/d1-opus (orbital-one), server sim-dmarz-9, claim `dmarz-d1-opus` to 15:44Z. Not a review. Last updated 2026-10-04T08:04Z.

## 1. Results so far

`d1o-a1` finished at 08:00:54Z and **passed the fresh gate**: hub metrics `fresh_justified: 12`, `qualification_passed: 1`.

- 72 of 72 calls terminal, 0 invalid, 0 missing usage, USD 1.47, 7 minutes (07:53:55Z to 08:00:54Z). About 5.8 s and USD 0.020 per call at effort high.
- Fresh gate: 12 of 12 evidence-justified choices on worlds 52001 to 52012 (gate 10 of 12). For comparison, on the six reused full-evidence worlds Haiku was 2 of 6 and Sonnet 3 of 6 in D1. The development comparison (Opus on the same six worlds and the saved-report quorums) is in the audit, which is not on main yet; I have only the hub summary.
- Before the run: rehearsal 72 of 72 scripted, probe `d1o-p1` valid, dmarz's waiver recorded 07:53Z (commit 9315f76a).
- Confidence: 12 of 12 on fresh worlds is a clear pass of this gate. It is 12 clean single-agent decisions, with thinking at effort high. It does not show how Opus behaves in the three-agent swarm arms or under attacked evidence.

## 2. Gate forecast

Done. Passed. sim-dmarz-9 is idle from 08:01Z; the claim `dmarz-d1-opus` runs to 15:44Z but is scoped to D1-Opus.

## 3. Next run

**The gate passed, so this is the live branch.** The plan says passing "makes Opus eligible for a separately planned fresh swarm qualification" and starts nothing. That successor does not exist yet. What it needs:

- A v3 swarm qualification on Opus 5.5 with the same shape as `v3-q0-a1` (6 fresh worlds, 4 communication arms, clean and attacked exposures: 96 cases, 636 calls). On Haiku that took about 34 minutes and USD 4.39. At tonight's Opus pace (6 s and USD 0.02 per call) it is about 65 minutes and USD 13, more if the swarm turns think longer.
- Fresh world IDs. 20001 to 20006 are used, 50001 to 50006 are reserved for Q1, 30000 to 30023 are the closed holdout, 52001 to 52012 are used by this run.
- An Opus request path in `bench_v3`. The pinned runner sends temperature 0 and a 2,000-token cap with no thinking handling. The D1-Opus adapter (no temperature, `thinking: adaptive`, `output_config.effort`, 16,000 cap, thinking blocks filtered, refusal category, fallbacks off) is the thing to port, with the F1 and F2 fixes from task `fix-bench-v3-review-f1-f2` pinned.
- A launch manifest, pre-run review and dmarz's waiver for that study. The server claim covers "D1-Opus only", so a new claim or an amended one.
- Open choice for that plan: effort. D1-Opus passed at effort high; the swarm arms multiply calls by about nine (636 against 72), so effort high costs about USD 13. That is small; keeping effort high keeps the qualification comparable with this result.

(The fail branch did not occur and is removed. D2 remains the diagnostic for why Haiku and Sonnet failed.)

## 4. Design notes for later runs

- 60 of the 72 calls are reused development requests and do not count toward the gate. The gate rests on 12 calls, about 75 seconds of this run. A fresh-only screen of 12 to 24 worlds would give the same decision at the same cost and a larger denominator.
- This run and D2 overlap on Opus. If the fresh gate passes, D2's Opus arm is expected to pass as well and D2 mainly explains the Haiku and Sonnet failures. If D2 has not launched by the time this audit lands, its operator should read the result first.
- Setup for this 8-minute run included a rehearsal, a probe, a preflight that expires in 30 minutes and a wait for a first-hand go. The probe and the run could be one command with the probe as a software gate.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 3 and 4.
