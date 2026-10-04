# Post-mortem: s1r-a1 and s1l-a1 (manifest m3, Claude Opus 5.5)

- Experiment / owner / stages / date: soc07-private-judgments / dmarz (operated by dmarz/orbital-orchestrator from orbital-one) / S1-R controlled replay and S1-L live teams / 2026-10-04 UTC.
- Pre-run assessment: [s1-pre.md](s1-pre.md), section "Manifest m3". Parent: [s1q2-post.md](s1q2-post.md) (S1-Q.2 passed 12 of 12).
- Revision `3bb554f518c30e7c1dded9d17ce8b4be7f6f0a97`, fingerprint `7237fa8a…`, host sim-dmarz-8, claim `dmarz-soc07-private`. Both stages were launched by the stage chain (`scripts/run-soc07-chain.py`, agentops `c4c8b41`, unit `soc07-chain-m3`), each only after the previous stage's software gate passed.
- Disposition: **both stages complete and every software gate passed; the comparison is null at ceiling.** Team success was 1.00 for every communicating arm in every regime, in both stages. **The ceiling was already visible in S1-R** (all arms 1.00 in all regimes); S1-L ran as launched and confirmed it. This says the task is too easy for this model with reasoning, not that delaying disclosure has no effect. The successor is a new design version, [soc07-private-judgments-v2](../../soc07-private-judgments-v2/README.md), with harder worlds and a futility rule.

## What ran (measured)

| Stage | Hub run | Episodes | Calls planned / valid | Failures, retries | Input / output tokens | Max input per call | USD | Time | Gate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S1-R | `soc07-private-judgments/807dfab8` | 192 / 192 | 672 / 672 | 0, 0 | 1,028,967 / 56,082 | 2,061 | 5.237508 | 32 min | passed: clean competence, parse validity, truncation per phase, budget/timeout, zero leaks, calls counted once, no crash |
| S1-L | `soc07-private-judgments/92e1c0d5` | 240 / 240 | 4,080 / 4,080 | 0, 0 | 6,513,472 / 327,304 | 2,297 | 32.599968 | 43 min | passed (same checks without clean competence) |

Study ledger after S1-L (sim-dmarz-8): 4,788 calls, **USD 37.933648**, of which m1 0.010669, m2 0.032043, m3 37.890936; 0 unknown-cost calls. The one-call m3 interface probe (USD 0.002408) is outside the ledger. Cap USD 500.

## Results (measured; exploratory)

Team success rate by arm and regime (16 episodes per cell), and episodes whose first answers were not unanimous:

| Arm | S1-R clean / correctable / informed | S1-L clean / correctable / informed | S1-L first-answer splits (clean / correctable / informed) |
| --- | --- | --- | --- |
| PRIVATE | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0 / 16 / 15 |
| PUBLIC | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0 / 16 / 15 |
| NEVER | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0 / 16 / 15 |
| PREPARE | 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0 / 0 / 0 |
| VOTE | not in S1-R | 1.00 / 1.00 / 0.00 | 0 / 16 / 15 |

- Primary contrast, PRIVATE minus PUBLIC: 0.000 in every regime in both stages, world-cluster bootstrap interval 0 to 0 (8 worlds per regime, 10,000 draws).
- VOTE fails the informed-minority regime by design: without discussion, four agents holding only superseded estimates outvote the one agent holding the audit.
- In S1-L the manipulation worked: first answers split in 31 of 32 minority-regime episodes per communicating arm, and discussion resolved every split to the correct answer in every arm. S1-R's analysis reports 0 first-answer splits in every cell; why is not checked here (inferred: in the controlled replay only one agent is a model and the counter is computed over the assigned agents' answers). Its 1.00 team success in every arm already showed that one round of discussion recovers the right answer.
- Interpretation (inferred, not measured): with adaptive reasoning, Opus agents treat a cited later audit as decisive whether or not first answers were published, so publication order has nothing left to change on this generator.

## Visualization review

- All five m3 runs on sim-dmarz-8 (S0 83013f20 and 00e03ba4, S1-Q.2 a80d0c73, S1-R 807dfab8, S1-L 92e1c0d5) were checked directly: every uploaded artifact's SHA-256 matches the server copy, `replay.gif` decodes at 1800 x 1200, and every journal hash chain reads (S1-R 1,106 records, S1-L 4,610).
- The final frames show the ceiling: every communicating arm's bar is full in every regime, and VOTE's informed-minority bar is empty.

## Experiment-quality assessment

- Execution quality was high: 4,752 m3 calls, all valid, no failures, retries, truncations or leaks; reasoning stayed far below the 4,096-token allowance (about 80 output tokens per call in S1-L).
- Scientific information was nil on the primary question, because every arm reached 1.00. The design's own "uninformative if" condition (team success at ceiling in every arm and regime) is met.
- Two deviations recorded in A6 apply: provider-default sampling instead of temperature 0.7, and the visible caps as a share of a larger `max_tokens`.
- The futility signal was available at S1-R; S1-L (USD 32.60) was spent confirming it. v2 adds a rule that S1-L does not start when S1-R is at ceiling.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
| --- | --- | --- | --- | --- | --- |
| S1L-1 / design | Team success 1.00 in every communicating arm and regime in S1-R and S1-L | Generator too easy for a reasoning model | New design version v2 (3 options, two audits incl. a superseding one, margins 1 to 9, deadline-boundary worlds) with a manipulation-check gate and a futility rule | v2 S1-R not at ceiling | open (v2) |
| S1L-2 / process | S1-L ran although S1-R was already at ceiling | No futility rule in v1 | v2 futility rule; chain launched in parts | Rule committed before v2 data (26c20dab) | closed for v2 |
| S1Q1-4 / tooling | Launcher `verify` walks runs whose files are on sim-dmarz-3 | Host move | Runs verified directly above | — | open, minor |

## Next run

- SOC-07 v1 is complete under m3. sim-dmarz-8's claim is released after this post-mortem; its checkout, results and the live v1 ledger stay on the host.
- Successor: soc07-private-judgments-v2 on sim-dmarz-3. Part A (S0) is running; Parts B (P0, S1-Q, S1-R) and C (S1-L, only if S1-R is not at ceiling) wait for dmarz's approval in his own words.
