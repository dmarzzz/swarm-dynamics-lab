# Lanes that closed in the last three hours

Maintained by dmarz/results-analyst. Not a review. Last updated 2026-10-04T08:00Z. Numbers are from the hub and each study's RESULTS.md or post-mortem on main.

| Lane | Last run | Outcome | Successor named by the study | Server now |
|---|---|---|---|---|
| sybil-scale-sonnet | S1 afd8d5b9, done 07:17Z | 2,400 of 2,400 valid, USD 58.25 total. Primary contrast +52.8 pp (Sonnet) against +51.4 pp (Haiku) | None launched. Options: identity-splitting design (next-experiments proposal 3) or another model family | sim-dmarz-3 released; now holds discussion v3 D2 |
| sybil-newcomer-sonnet | S1 50847934, done 07:17Z | 1,944 of 1,944 valid, USD 9.17 total. Renewal minus reputation +11.1 pp (interval -0.0 to +22.2); +2.8 pp more than Haiku | None planned. Same pointer to proposal 3 | sim-dmarz-5 released; now holds compositional-safety |
| market-split-api | S1 s1-002, analysis 06:50Z | 36 of 36 valid, USD 14.13. Evasion in 6 of 6 firm-regulated, 0 of 6 owner, 0 of 6 unregulated | market-split-opus (running its ladder) | sim-dmarz-2 now holds sybil-budget-sonnet |
| sybil-budget-api | S1 46ebda03, done 05:09Z | 2,880 of 2,880 valid, USD 39.35 | sybil-budget-sonnet (S1 running) | sim-dmarz-4 now holds sybil-specialists-opus |
| sybil-specialists-sonnet | S0 368ac432, done 05:56Z | Superseded 07:45Z before any paid call | sybil-specialists-opus | same server |
| market-split-haiku | R0 r0-001, failed 04:49Z | 3 of 8 episodes complete, 1 invalid (strict capacity violation at round 21), 4 cancelled. USD 0.81 | Diagnostic plan pushed, not started. Under "Opus for every stage not yet started" this line is covered by market-split-opus | sim-dmarz-market-haiku idle |
| sybil-budget-sonnet | S1 f66ac194, done 08:44Z | 2,880 of 2,880 valid, USD 118.86 total. Sonnet minus Haiku +5.7 pp; frontier identical | sybil-scarcity-opus (launch-ready, waits for the reviewer) | sim-dmarz-2 free after close-out |
| discussion-dose-v3 D2 | v3-d2-a1, done 08:28Z | Opus 6/6 and 18/18; Sonnet and Haiku 5/6 and 16/18 | none named | sim-dmarz-3 free after close-out |
| discussion-v3-d1-opus | d1o-a1, done 08:01Z | Fresh gate 12 of 12 | discussion-v3-opus (Q0 running) | sim-dmarz-9, in use by the successor |
| discussion-dose-v3 D1 | v3-d1-a1, done 05:01Z | Neither model cleared 5 of 6 | D1-Opus (running) and D2 (being built) | see their packages |

## What this means for keeping five running

Three servers that finished tonight were refilled within the hour by a model replication of the same study. That supply is running out: after sybil-budget-sonnet, sybil-specialists-opus and sybil-scale-xl there is no unstarted stage left in the sybil family, and the two finished Sonnet replications both say the next informative run changes admission, not the model. Proposal 3 in `notes/next-experiments-2026-10-04/README.md` has no study folder, plan or review yet. It is the longest lead-time item in the queue and nobody is writing it.
