# sybil-newcomer-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/newcomer-opus (orbital-one), server sim-dmarz-13. Not a review. Last updated 2026-10-04T09:02Z.

## 1. Results so far

- Plan committed 07:59Z as one chain: fleet S0 (198 scripted), one-call probe, Q0 (36 calls), S1 (1,944 calls). Opus 5.5 at effort low, 4,000-token cap, two requests in flight.
- Q0 `q0-001` (run 39421582): **passed**, 36 of 36 valid, USD 0.205, finished 08:15:02Z.
- S1 `s1-001` (run 14ea6e6b) started from the chain: 32 of 1,944 answers at 08:16:07Z, USD 0.24 (USD 0.0074 per call).
- Earlier cohorts on the same 1,944 packets: Haiku and Sonnet agree. Primary contrast (renewal minus reputation, sixteen identities, sleeper, round eight) is +8.3 pp for Haiku and +11.1 pp for Sonnet, interval on the difference -2.8 to +8.3 pp.

**S1 finished at 09:00:12Z: 1,944 of 1,944 valid, USD 14.48, 45 minutes.** Hub specialist accuracy over all cells: Opus 45.1%, against Haiku 44.4% and Sonnet 43.6% on the same packets. The primary contrast and per-cell comparison come from the study's own analysis, not from the hub number; I have not read the records.

## 2. Gate forecast

Done. Overall accuracy within 1.5 points across three models is what the plan predicted ("the pattern replicates").

## 3. Next run

- No further stage. sim-dmarz-13 is free after close-out and no successor is named for it.
- Candidates: sybil-split-opus (identity splitting at fixed attacker resources; plan and frozen design on main, no code yet) or sybil-scarcity-opus if it is not already placed on sim-dmarz-2.
- This is the fourth model cohort across the sybil studies that leaves the result where it was. See [LESSONS.md](LESSONS.md) item 5.

## 4. Design notes for later runs

- This cohort spends 1,944 calls on a prediction of no model effect. The primary cell is 3 policies x 24 worlds = 72 calls; a cut grid of the primary cell plus the one-identity comparison would test the same prediction in under 300 calls. At USD 11 the full grid is cheap in dollars; its cost is an hour of a server.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 5 and 8.
