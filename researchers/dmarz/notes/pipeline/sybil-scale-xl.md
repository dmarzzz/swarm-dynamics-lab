# sybil-scale-xl: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/scale-xl, server sim-dmarz, claim `dmarz-sybil-scale-xl` to 20:03Z. Amendment A1 (Opus 5.5, effort low, trimmed design). Not a review. Last updated 2026-10-04T08:20Z.

## 1. Results so far

- S0 `s0-a1` (run 4673b7bd): 72 of 72 valid, 0 model calls, 8 minutes, most of it preparing inputs at N=8,748.
- Q0 `q0-a1` (run a6b2a7b3): **passed**, 24 of 24 valid at all three sizes, 24 calls, USD 9.853, 59 seconds on the hub clock (07:53:00Z to 07:53:59Z).
- S1 `s1-a1` (run 7a32ec63) started 07:54:07Z from the tmux chain. It has made no model call yet: it is building the recorded inputs on the server's 4 cores (load 4.3). N=972 took about 3 minutes, N=2,916 about 10 minutes, and N=8,748 began at 08:07Z. 0 of 576 answers at 08:09Z.

## 2. Gate forecast

- S1 has no pass gate; it ends when 576 calls are terminal or the ledger stops dispatch at USD 330.
- Cost: Q0's USD 9.85 is at the top of the amendment's USD 7 to 10 estimate. Scaling the amendment's S1 estimate the same way gives about USD 235 to 245 for S1 and about USD 250 in total, under the USD 330 cap. This is my projection from one number, not a measurement; the per-size cost will be visible once S1 reports.
- Time: input preparation is the long pole so far. If N=8,748 scales as the first two sizes did (about three times longer per step), the first model call is around 08:35Z to 08:45Z. Model time after that is unknown until answers land. Q0's 24 calls finishing inside a minute means calls run concurrently; if S1 keeps that pace the model part is well under an hour, unless the provider's input-token rate limit throttles the 4,374-report packets.

## 3. Next run

**If S1 completes (576 of 576):** close-out is analysis and post-mortem; the study has no further stage. Nothing follows on this server unless a successor is planned now. Candidates already written down: proposal 3 (fixed attacker resources, identity splitting) in `notes/next-experiments-2026-10-04/README.md`, which both finished Sonnet replications name as the informative next step.

**If S1 stops early on the USD 330 cap:** the cap is in `design.yaml`, which is part of `source_hash` (`src/study.py` line 22), so raising it means a new batch with fresh S0 and Q0. Check which cells are missing before deciding: the primary contrast is at N=8,748 and those are the most expensive calls.

**If S1 stops on a failure:** one failed call stops new dispatch (`src/worker.py` line 59) and there are no retries, so a single HTTP 429 or 529 ends the stage with the remaining assignments not started. Four requests are in flight and the largest packets are about 200,000 tokens, so a rate limit on input tokens per minute is the likeliest cause; Q0 ran 24 such calls in a minute without one. Other declared categories: `nonterminal_output` (thinking used the 8,000-token room) and `refusal`. For a rate-limit stop the repair is lower concurrency or a retry on 429 and 529 ([LESSONS.md](LESSONS.md) item 8); either is a new batch with fresh S0 and Q0 and another 45 minutes of input preparation unless the built inputs are reused. Decide now whether a resume of the not-started assignments at the same source hash is acceptable, because that is the only repair that does not repeat the paid calls.

## 4. Design notes for later runs

- The chain S0 to Q0 to S1 under software gates worked: Q0 ended 07:53:59Z and S1 started 07:54:07Z, eight seconds of dead time. This is the pattern the other lanes should copy.
- The chain did not include a cost projection between Q0 and S1. Here it would have passed. A one-line gate (projected S1 cost from Q0 usage must be under the remaining cap) would make the chain safe when the estimate is closer to the cap.
- At N=972 the A1 cells pair with the Haiku parent. Two finished Sonnet replications tonight found the model swap moved the primary contrast by 1.4 pp (scale) and 2.8 pp (newcomer). If the Opus N=972 cells also match Haiku, the model is not the lever in this family and later sybil runs can use the cheapest qualified model.

- S1 spends its first 40 to 50 minutes building graphs and packets on four cores, with no model call. That work depends only on the frozen design, so it could run during S0 and Q0, or before the claim starts, and be read from disk by S1 (the run already writes `worlds.jsonl.gz`). On this run it roughly doubles the stage's wall time.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 1, 2 and 5.
