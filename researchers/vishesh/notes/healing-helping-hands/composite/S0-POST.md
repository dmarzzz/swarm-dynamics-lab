# C1-S0 post-mortem

2026-10-04 UTC. Same-author assessment; source `66ec09017284892a59623c7e7a73d93651b4a686`, [prospective plan](PLAN.md), [pre-assessment](S0-PRE.md). Decision: **advance to separately admitted S1**.

All 60 assignments started, completed, graded and analyzed. 60 Qwen and 120 Jev calls; all 180 call starts have terminal records. Zero invalid, missing or transport-failed responses. Runtime 131.460 seconds. Same-author audit reproduced labels, exact payload hashes, confusion counts and paired contrasts. Jev usage USD 0.002331126; cumulative ledger USD 0.015335250, remaining USD 0.084664750 under the original USD 0.10 cap. Qwen CPU runtime is charged through the separately bounded VM.

Qwen-only scored 36/60 (60%): SUPPORT 16/20, REFUTE 0/20, UNCERTAIN 20/20. Jev-only and Qwen+Jev each scored 60/60 and 20/20 in every class, passing the prespecified 51/60 and 14/20 floors. The composite corrected 24 Qwen errors, damaged zero correct decisions and showed zero anchoring events. Composite minus Jev accuracy is zero; all 60 final labels agree. This does not demonstrate a useful contribution from Qwen. No prompt or threshold was changed after outcomes. Qwen's failure is retained as a measured control and does not block the qualified composite.

The confusion figure includes all assigned cases and missing-outcome columns. Finite repeated templates prevent an independent-generalization or certainty claim. The new dedicated machine and budget/source/registration checks worked; reporting acknowledged start and all six progress updates. Full observations, raw sanitized requests/responses, admission, manifest, reporting journal and audit are retained.

Next: S1's three fresh synthetic corpora and 270 dependent architecture worlds, under unchanged instrument hashes and the separate [S1 pre-assessment](S1-PRE.md). Preserve the ceiling result and strong central control; no tuning to manufacture composite or swarm superiority.
