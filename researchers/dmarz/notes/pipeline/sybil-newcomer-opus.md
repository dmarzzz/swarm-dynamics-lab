# sybil-newcomer-opus: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/newcomer-opus (orbital-one), server sim-dmarz-13. Not a review. Last updated 2026-10-04T08:20Z.

## 1. Results so far

- Plan committed 07:59Z as one chain: fleet S0 (198 scripted), one-call probe, Q0 (36 calls), S1 (1,944 calls). Opus 5.5 at effort low, 4,000-token cap, two requests in flight.
- Q0 `q0-001` (run 39421582): **passed**, 36 of 36 valid, USD 0.205, finished 08:15:02Z.
- S1 `s1-001` (run 14ea6e6b) started from the chain: 32 of 1,944 answers at 08:16:07Z, USD 0.24 (USD 0.0074 per call).
- Earlier cohorts on the same 1,944 packets: Haiku and Sonnet agree. Primary contrast (renewal minus reputation, sixteen identities, sleeper, round eight) is +8.3 pp for Haiku and +11.1 pp for Sonnet, interval on the difference -2.8 to +8.3 pp.

## 2. Gate forecast

- Q0 gate: 36 of 36 valid, per shape at least 95% field accuracy, at least 90% exact packets, 100% abstention on absent fields. Haiku and Sonnet both passed 36 of 36. Forecast: pass.
- Q0 is done and passed. S1: 1,944 calls, about USD 14 at USD 0.0074 per call. Sonnet took 79 minutes with its settings; expect 1 to 1.5 hours (about 09:20Z to 09:50Z). Pace will be measurable at the next reading.

## 3. Next run

- **If Q0 passes:** S1 starts from the chain. Nothing needed.
- **If Q0 fails abstention or accuracy at effort low:** a new batch at effort medium. The prompt stays as the two earlier cohorts used it.
- **If S1 stops on one failed call:** see [LESSONS.md](LESSONS.md) item 8. The stage has no retry and stops new dispatch on the first failure.
- **After S1:** the plan predicts the pattern replicates (primary contrast under +10 pp, per-policy accuracy within 10 pp of Sonnet). If so, this is the third cohort saying the newcomer result is about admission. The study has no further stage; the server's next run is whichever admission-side study is ready (sybil-scarcity-opus is being built as a launch-ready package).

## 4. Design notes for later runs

- This cohort spends 1,944 calls on a prediction of no model effect. The primary cell is 3 policies x 24 worlds = 72 calls; a cut grid of the primary cell plus the one-identity comparison would test the same prediction in under 300 calls. At USD 11 the full grid is cheap in dollars; its cost is an hour of a server.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) items 5 and 8.
