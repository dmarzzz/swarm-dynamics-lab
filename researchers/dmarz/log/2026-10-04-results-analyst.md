# 2026-10-04 dmarz/results-analyst

- 07:48Z-08:02Z first full pass over every dmarz lane with a run in the last three hours. Wrote `notes/pipeline/` (INDEX, LESSONS, eight lane files).
- Found: compositional-safety P1 cannot run from q0-007 (nonrefundable ledger cap, and the cap is inside the hashed design); SOC-07's prompt never states that delivery equal to the deadline qualifies (one of Sonnet's three misses; 1 of 12 worlds in set 2 affected).
- Surprised by: how short the paid stages are next to the waits around them (Q0 stages of 1 to 13 minutes; idle gaps of 5 to 20 minutes waiting for a go or a waiver).
- Next: keep packages current as runs report; D1-Opus audit, sybil-scale-xl S1 pace, sybil-budget-sonnet S1 result.
- 08:02Z-10:20Z cycles. Packages for 13 lanes, 12 lessons. Things found from records while runs were going: compositional P1 could not run from q0-007 (ledger cap inside the hashed design); SOC-07 prompt lacked the deadline-boundary rule; budget-sonnet paired read at 44% forecast the final +5.7 pp; SOC-07 at ceiling at S1-R; compositional P1 would overrun its stage limit and the placebo arm hit the byte limit; scale-xl S1 measured at 5.8M input tokens/min against a 5M limit; the 10:10Z credit outage (HTTP 400) behind the scale-xl stop and 61 failed v3-opus calls.
- Got wrong: reported the v3 swarm plan missing from a stale checkout (08:17Z); reported market-split idle during a 30 s hand-over (09:02Z); read a clean small-request canary as "safe" two minutes before a different failure cause arrived (10:06Z-10:08Z); undercounted spend by USD 32 by not reading `model_cost_usd`.
- Surprised by: how many stops tonight were limits written into hashed designs or account-level limits, not model behaviour. Every completed Opus qualification passed.
