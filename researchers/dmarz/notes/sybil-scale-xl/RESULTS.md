# Results: Sybil resistance at 9x scale (Opus 5.5, amendment A2)

Exploratory S1, run sybil-scale-xl/1a20f29b, revision 4217f29b, claude-opus-5-5 at effort low. **Incomplete**: 576 assigned, 482 started, 481 valid, 1 failed, 94 not started. Dispatch stopped at 10:10:36 UTC when one token-count request returned HTTP 400. The record keeps only the category `count_http_400`; the adapter stores no error body. The cause is inferred, not recorded here: in the same 10:07–10:11 window discussion-v3-opus recorded 61 failures with reason `provider_credit_balance_low` (HTTP 400) on the shared account, and calls succeeded again afterwards (dmarz/fleet-monitor). The stop is therefore a billing outage unrelated to any outcome. Stage cost USD 194.78 (48.53M input, 32k output tokens). Study cost to date USD 214.49 including qualification, plus a USD 0.09 probe.

Every table below keeps missing rows in its denominator. Cell counts are valid/assigned worlds. Paired contrasts use complete world pairs, and a bound replaces each missing difference with its worst and best possible value (−1 and +1) over all 24 worlds.

## Primary contrast

Coverage, visible badges, attackers pass 10%, specialist accuracy, proportional (N/9) minus fixed (4) checks at N=8,748: **+100 points on all 18 complete pairs.** The proportional cell is 20/20 correct and the fixed cell 0/22. Bounded over 24 worlds with the 6 incomplete pairs at their extremes, the contrast lies between **+50 and +100 points**, above the predeclared 10-point useful difference in either case. Attacker seat share falls from 9.8% to 2.7%.

## Scaling, coverage and random checking

| N | Checks | Coverage accuracy | Random accuracy | Coverage attacker share | Plurality, coverage packet |
|---:|---:|---:|---:|---:|---:|
| 972 | 4 | 0.0% (21/24) | 58.0% (23/24) | 11.4% | 22.2% |
| 972 | 108 | 100% (19/24) | 100% (20/24) | 3.6% | 100% |
| 2,916 | 4 | 4.8% (21/24) | 50.0% (18/24) | 11.6% | 15.9% |
| 2,916 | 324 | 100% (20/24) | 100% (24/24) | 2.6% | 100% |
| 8,748 | 4 | 0.0% (22/24) | 31.4% (17/24) | 9.8% | 33.3% |
| 8,748 | 972 | 100% (20/24) | 100% (19/24) | 2.7% | 100% |

Informative checks, attackers pass 10%. With checks proportional to population, both selection rules stay at 100% specialist accuracy from 972 to 8,748 identities, and attacker seat share stays at 2.6–4.1%. The parent's proportional-check result (98.6% with Haiku at 972) therefore holds at 3× and 9× the population in this fixture.

With four fixed checks, coverage collapses at every size, as in the parent. Random selection degrades more gradually (58% → 50% → 31%, paired budget contrast at 8,748 +71 points on 15 complete pairs, bounded +7 to +82).

## Long packets did not degrade synthesis

At 8,748 identities each packet holds 4,374 reports (about 213k input tokens). In every proportional-check cell with informative checks, Opus matched same-packet plurality exactly (model minus plurality 0.0 at all three sizes, both selection rules). No long-context integration loss is visible at this packet length.

## Opus abstains where Haiku guessed

The largest difference from the parent is behavioural. With four coverage checks, Opus returned null for every specialist field at N=972 (63/63 fields, informative checks) where Haiku reached 47.2% on identical packets. Plurality reached 22% on these packets. Across fixed-check coverage cells Opus is 8–33 points below plurality, nearly all through abstention (for example N=8,748: 54 abstentions and 12 wrong non-null answers of 66 fields). The system prompt allows null "if evidence is missing or too ambiguous", and Opus takes that option when the admitted reports are dominated by one repeated fabricated value. This is measured behaviour, not a judgement that abstaining is wrong: the fixed-check packets contain few honest specialists.

The N=972 Opus-versus-Haiku comparison is paired by assignment, but this study's pairs are incomplete and the two models also differ in thinking. It is reported as descriptive only. A per-world paired table is deferred until the completion decision below.

## Uninformative checks (attackers pass 90%)

Proportional checking adds little and is not a security gain: coverage accuracy 15% → 26% → 40% at 972/2,916/8,748 with attacker share 21–22%, against fixed-check coverage at 0–6%. Opus is below plurality in these cells (−21 to −33 points for coverage), again mostly through abstention. Budget contrasts: coverage +13, +21 and +26 points (complete pairs 18, 14, 17), whose bounded intervals all include zero.

## Execution

- 8 calls drew HTTP 429 (first at about 10:07:30 UTC). All 8 succeeded on the first retry after 20 s; none reached a second retry. The amendment A2 retry rule worked as designed.
- Calling lasted about 9 minutes, after 89 minutes from launch that include input preparation and an 18-minute pause of the worker before its first call (09:37:35–09:55:03 UTC), made to avoid overlapping sybil-scarcity-opus at the 5M-input-token-per-minute workspace limit. Mean call latency 3.9 s, max 31.4 s.
- All 24 worlds have at least one missing row, because dispatch order is shuffled. The best cell has 24/24 worlds and the worst 17/24.
- The local reconciliation (reporting/build_report.py) recomputed every evaluation and the frozen analysis from the saved assignments and episodes and matched them. The launcher's `verify` covers all runs of the experiment and refuses because s1-a1 (stopped before any call) has no artifacts, so the hub artifact hash check for this run is still to be done.

## Files

[results-s1-a2/results-summary.json](results-s1-a2/results-summary.json), [results-s1-a2/results-cells.csv](results-s1-a2/results-cells.csv), [stage summary](results-s1-a2/summary.json), [post-mortem](reviews/s1-a2-post.md), [proposed completion amendment A3](AMENDMENT-A3-PROPOSED.md). The combined Haiku-plus-Opus figure is artifact `sybil-scale-xl-combined`. Live run view: https://swarm-live.pages.dev/#/r/sybil-scale-xl%2F1a20f29b
