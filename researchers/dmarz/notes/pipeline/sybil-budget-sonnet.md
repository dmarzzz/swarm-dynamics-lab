# sybil-budget-sonnet: decision package

Maintained by dmarz/results-analyst. Operator: dmarz/budget-sonnet (orbital-one), server sim-dmarz-2, claim `dmarz-sybil-budget-sonnet` to 15:17Z. Not a review. Last updated 2026-10-04T07:58Z.

## 1. Results so far

- S0 (ef4b32a6) 256 of 256 valid; Q0 (35565940) 16 of 16 valid, passed, USD 0.97.
- S1 `s1-001` (f66ac194, Sonnet 4.6, 2,880 calls) started 07:27:39Z. At 07:55:34Z: 722 of 2,880 answers, 0 invalid, USD 29.12. Cost per call is steady at USD 0.040.
- The hub reports only counts and cost during S1. Accuracy (`rare_accuracy`) appears when the stage closes, so there is no partial read on the Sonnet-minus-Haiku contrast yet.

## 2. Gate forecast

- No pass gate; the stage ends at 2,880 terminal calls.
- Pace: 345 calls in the first 20.7 minutes (17 per minute), then 377 in the next 7.2 minutes (52 per minute). At the recent pace the stage ends about 08:37Z; at the early pace about 10:05Z. I do not know why the pace changed.
- Cost: about USD 116 for S1 at USD 0.040 per call, inside the plan's USD 100 to 140 estimate and the USD 400 reservation cap.

## 3. Next run

S1 is the last stage. What follows depends on the declared primary comparison (Sonnet minus Haiku specialist accuracy per cell on identical packets; a useful difference is at least 10 pp):

- **If the difference is under 10 pp overall and at the middle budgets:** this is the third sybil study in which swapping the synthesizer changes little (scale: +52.8 pp against +51.4 pp; newcomer: +2.8 pp difference). An Opus rerun of the 2,880-call grid would cost about USD 150 or more and is unlikely to move the frontier. The next run for this server is then a design that changes admission: proposal 3 in `notes/next-experiments-2026-10-04/README.md`. It needs a study folder, plan and pre-run review, which can be written while S1 runs.
- **If the difference is 10 pp or more in some region:** an Opus replication restricted to the cells where the models differ (the plan predicts middle budgets with weak checks) instead of the full grid. The Opus request rules in [LESSONS.md](LESSONS.md) item 3 apply; this study's `provider.py` is byte-identical to sybil-scale-api's and sends temperature.

## 4. Design notes for later runs

- 2,880 calls is two sizes x six budgets x five pass rates x two policies x 24 worlds. The Haiku parent already has every cell. If the Sonnet result matches Haiku, later model replications can sample the grid (for example three budgets x three pass rates) and still test the model question.
- The study cannot show partial accuracy while running. A running per-cell accuracy metric on the hub would let the successor decision be made at 25% of the run instead of at the end.

## 5. Cross-lane

See [LESSONS.md](LESSONS.md) item 5.
