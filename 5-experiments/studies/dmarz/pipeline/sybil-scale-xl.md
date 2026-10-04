# sybil-scale-xl: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/scale-xl, server sim-dmarz, claim `dmarz-sybil-scale-xl` to 20:03Z. Amendment A1 (Opus 5.5, effort low, trimmed design). Not a review. Last updated 2026-10-04T10:14Z.

## 1. Results so far

- S0 `s0-a1` (run 4673b7bd): 72 of 72 valid, 0 model calls, 8 minutes, most of it preparing inputs at N=8,748.
- Q0 `q0-a1` (run a6b2a7b3): **passed**, 24 of 24 valid at all three sizes, 24 calls, USD 9.853, 59 seconds on the hub clock (07:53:00Z to 07:53:59Z).
- S1 `s1-a1` (run 7a32ec63) started 07:54:07Z from the tmux chain. It has made no model call yet: it is building the recorded inputs on the server's 4 cores (load 4.3). N=972 took about 3 minutes, N=2,916 about 10 minutes, and N=8,748 began at 08:07Z. 0 of 576 answers at 08:09Z.

### 08:21Z: A1's S1 stopped before any call; amendment A2 adds an overload retry

The operator stopped `s1-a1` during input preparation (hub status failed, KeyboardInterrupt, 0 calls, no cost) and committed amendment A2 (commit 4217f29b): a call that gets HTTP 429 or 529 is retried at most twice, after 20 s and 60 s; every other failure still stops dispatch. Nothing scientific changes. Because the source hash changes, the chain restarts as batch a2: S0 `s0-a2` (run b7e6407c) has been running since about 08:23Z, then Q0 `q0-a2` (about USD 10 more), then S1.

### 10:01Z to 10:10Z: S1 `s1-a2` ran and stopped at 481 of 576

The worker was paused from 09:37Z to 09:55Z (fleet monitor's decision, to keep it off scarcity's S1 under the 5M input-tokens-per-minute limit measured at 09:20Z). Input preparation then finished and the first call was at 10:01:39Z.

- 481 completed, 1 failed, 94 not started. USD 194.78, 48.53M input tokens, 537 seconds of calls. Hub status: failed.
- Throughput: 5.8M input tokens per minute for the first five and a half minutes (61 to 66 calls per minute, latency 3.5 s), then the first 429s at about 10:07:30Z. 8 calls drew a 429; all 8 cleared on the first 20-second retry; none reached the second. Average over the whole stage 5.42M per minute.
- **The stop was not the rate limit.** The failed call is `count_http_400` at 10:10:36Z (N=972, random, 4 checks, pass 0.9, world 6001). In the same two minutes discussion-v3-opus recorded 61 `provider_credit_balance_low` failures; a credit error is an HTTP 400. The account's credit ran out for a few minutes and one count_tokens request caught it. Amendment A2's retry covers 429 and 529 only.
- Missing: 26 calls at N=972 (plus the failed one), 34 at N=2,916, 34 at N=8,748. 1 of 24 cells has all 24 worlds; the worst has 17. Primary contrast cells (N=8,748, coverage, pass 0.1): 22 of 24 worlds with fixed checks, 20 of 24 with proportional checks.

## 2. Gate forecast

No stage is running. Nothing to forecast until the operator picks a repair.

## 3. Next run

- **Resume (cheapest):** dispatch only the 95 unfinished assignments at the same source hash. About USD 41 and two minutes of calls; the inputs are already built. The failed call was an account-level error, not a packet or instrument problem, so the resumed rows are the same measurement. It needs a dated note that the cohort was completed in two sittings, and the credit balance confirmed first.
- **New batch:** S0, Q0 (USD 10), about 70 minutes of input preparation and USD 236.
- **Close as is:** report the primary contrast on the complete pairs with the missing rows shown in the denominator.
- For any of them: the stage draws 5.8M tokens per minute, above the limit. From a full bucket that lasts about five minutes; the resume is short enough to fit, a full S1 is not, and every lane without a retry rule takes invalid calls while it runs (compositional-safety lost four episodes to `http_429` at 10:06Z to 10:07Z).

## 4. Design notes for later runs

- The chain S0 to Q0 to S1 under software gates worked: Q0 ended 07:53:59Z and S1 started 07:54:07Z, eight seconds of dead time. This is the pattern the other lanes should copy.
- The chain did not include a cost projection between Q0 and S1. Here it would have passed. A one-line gate (projected S1 cost from Q0 usage must be under the remaining cap) would make the chain safe when the estimate is closer to the cap.
- At N=972 the A1 cells pair with the Haiku parent. Two finished Sonnet replications tonight found the model swap moved the primary contrast by 1.4 pp (scale) and 2.8 pp (newcomer). If the Opus N=972 cells also match Haiku, the model is not the lever in this family and later sybil runs can use the cheapest qualified model.

- S1 spends its first 40 to 50 minutes building graphs and packets on four cores, with no model call. That work depends only on the frozen design, so it could run during S0 and Q0, or before the claim starts, and be read from disk by S1 (the run already writes `worlds.jsonl.gz`). On this run it roughly doubles the stage's wall time.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 1, 2 and 5.
