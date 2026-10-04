# Reporting corrections, 2026-10-04

These are reporting corrections after the internal verifier read **every** saved terminal row. Frozen scientific specs, execution code pins, raw answers, dispatch journals and costs are not rewritten.

1. The initial shorthand “20 pool429s” was wrong. The first two linked-spec cohorts produced **8 HTTP429s**; the next three produced **12 HTTP503s**. All20 were transport failures with no model answer. Published README, paid-route amendment, audit and generated lineage captions are corrected. Some immutable archived spec/code descriptions retain their original429-only wording; this correction supersedes that descriptive shorthand, not their dispatch rules.
2. The subsequent native-schema recovery attempt added **four HTTP503 failures**. It did not use its429 retry allowance, because503 was not preregistered as retryable. The native queue then stopped.
3. All terminal attempts together: **152 API requests/assignments,100 valid answers,52 failures**:8 HTTP429,16 HTTP503,20 strict-JSON contract failures,8 HTTP403. The paid structured run contributed12 clean exact fixtures and88 valid main cells, but only2 complete paired roots (one per family), not88 independent observations.
4. A bootstrap with only one complete root per family yields a degenerate+50pp interval. That is not evidence of precision. The overview suppresses interpretation of that interval and gives the all-assigned bounds **[-93.1,+123.6]pp**. The raw summary is retained so the original computation is inspectable. No completed treatment finding is claimed.
5. The paid ledger independently recomputes to **USD1.189149 settled + USD0.617820 unresolved conservative reservations = USD1.806969 accounted**. The shared OpenRouter key'sUSD5 daily cap is external to the factoryUSD20 ceiling and was not raised or bypassed. Do not reportUSD1.806969 as verified actual charges.

`verify.py` recomputes each valid answer's rare-skill metrics without importing the original scorer, checks complete-root contrasts/missing bounds and replays every budget transaction. It reports652 internal consistency checks at this cutoff. This is not independent-researcher review.

`closeout.py evidence` reapplies the lineage-caption correction before registry rendering, so rerunning an archived analyzer cannot silently reintroduce the429-only caption into a closeout.
