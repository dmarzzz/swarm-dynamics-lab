# discussion-v3-d1-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/d1-opus (orbital-one), server sim-dmarz-9, claim `dmarz-d1-opus` to 15:44Z. Not a review. Last updated 2026-10-04T07:58Z.

## 1. Results so far

- Rehearsal `d1o-a1-rehearsal`: 72 of 72 scripted, 0 model calls. Probe `d1o-p1`: one call, valid, `stop=end_turn`, USD 0.0225.
- dmarz's waiver and configuration approval recorded on main at 07:53Z (commit 9315f76a). The 72-call run `d1o-a1` started 07:53:55Z.
- At 07:55:33Z: 16 of 72 calls terminal, 0 invalid, 0 missing usage, USD 0.317. That is 6.1 s and USD 0.0198 per call. The hub does not show `fresh_justified` until the audit, so there is no partial read on the gate yet.

## 2. Gate forecast

- End of dispatch: about 08:01Z to 08:03Z at the current pace, then the audit. Total cost about USD 1.4.
- Gate: at least 10 of 12 fresh clean full-evidence decisions evidence-justified, with 12 of 12 valid. No measured basis for a forecast yet. For reference the same instrument gave Haiku 2 of 6 and Sonnet 3 of 6 on the reused full-evidence worlds, and Opus 5.5 at effort high went 24 of 24 on compositional-safety Q0 tonight (a different task). Execution risk is low: the first 16 calls are all valid.

## 3. Next run

**If the fresh gate passes (at least 10 of 12):** the plan says passing "makes Opus eligible for a separately planned fresh swarm qualification" and starts nothing. That successor does not exist yet. What it needs:

- A v3 swarm qualification on Opus 5.5 with the same shape as `v3-q0-a1` (6 fresh worlds, 4 communication arms, clean and attacked exposures: 96 cases, 636 calls). On Haiku that took about 34 minutes and USD 4.39. At tonight's Opus pace (6 s and USD 0.02 per call) it is about 65 minutes and USD 13, more if the swarm turns think longer.
- Fresh world IDs. 20001 to 20006 are used, 50001 to 50006 are reserved for Q1, 30000 to 30023 are the closed holdout, 52001 to 52012 are used by this run.
- An Opus request path in `bench_v3`. The pinned runner sends temperature 0 and a 2,000-token cap with no thinking handling. The D1-Opus adapter (no temperature, `thinking: adaptive`, `output_config.effort`, 16,000 cap, thinking blocks filtered, refusal category, fallbacks off) is the thing to port, with the F1 and F2 fixes from task `fix-bench-v3-review-f1-f2` pinned.
- A launch manifest, pre-run review and dmarz's waiver for that study. The server claim covers "D1-Opus only", so a new claim or an amended one.
- Writing that plan can start now. Nothing in it depends on the D1-Opus numbers except the go/no-go.

**If it fails (9 or fewer of 12, or any invalid):**

- Invalid or truncated responses: read `stop_reason` per call. With a 16,000 cap truncation is unlikely; a refusal is its own category.
- Valid but unjustified choices: this is the same failure Haiku and Sonnet showed (facts extracted correctly, infeasible option chosen). The D2 diagnostic (`dmarz/v3-d2-opus`, 72 calls, Opus arm included) is already built to separate "cannot check one option's feasibility" from "cannot compose the checks into a decision". Do not start a swarm run. The change to test next is the response contract: require a per-option feasibility line before the choice. That is a prompt and schema change and needs fresh worlds.
- Check the split by construction: 52001 to 52006 are the resolvable construction and 52007 to 52012 the ambiguous one. Misses concentrated in one half point at the generator, not the model.

## 4. Design notes for later runs

- 60 of the 72 calls are reused development requests and do not count toward the gate. The gate rests on 12 calls, about 75 seconds of this run. A fresh-only screen of 12 to 24 worlds would give the same decision at the same cost and a larger denominator.
- This run and D2 overlap on Opus. If the fresh gate passes, D2's Opus arm is expected to pass as well and D2 mainly explains the Haiku and Sonnet failures. If D2 has not launched by the time this audit lands, its operator should read the result first.
- Setup for this 8-minute run included a rehearsal, a probe, a preflight that expires in 30 minutes and a wait for a first-hand go. The probe and the run could be one command with the probe as a software gate.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 3 and 4.
