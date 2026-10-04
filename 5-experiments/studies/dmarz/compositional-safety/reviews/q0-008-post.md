# Post-mortem: q0-008

- Experiment / owner / stage / date: compositional-safety / dmarz (operated by dmarz/compositional-opus) / Q0, first stage of chain q0-008 → p1-002 / 2026-10-04 UTC.
- Pre-run assessment: [q0-008-pre.md](q0-008-pre.md) at source `d1c10d49d37eb18e6ca2706afb4e3f00192c3844` (design v9). Agentops run-queue 219.
- Records: [records/q0-008](../records/q0-008/) (manifest, dispatch log, compressed episodes and trace, receipt, four final frames).
- Disposition: **interrupted by the operator for an execution defect; no qualification result.** p1-002 never started. Next action: `repair-and-rerun` as [q0-009](q0-009-pre.md).

## What ran and what happened

- The chain started about 08:02 UTC on sim-dmarz-5 (the run-queue 219 record says 08:24Z; that time is wrong). It registered the q0-008 plan, passed admission and ran Q0.
- 8 of 24 episodes finished, all on root 257: 8 valid, 8 safely complete, 0 violations, 3 to 8 turns. A ninth (282 D1 risk S) was in progress. No qualification summary was written, and the 15 unfinished assignments have no outcome.
- 43 calls, **USD 0.378800 actual**, USD 5.104048 reserved. Hub: four 257 bundle runs done; the 282 D1 risk run was marked failed by the operator with its 5 calls and USD 0.043312. Study ledger on sim-dmarz-5: 2,185 calls, USD 59.813121 reserved, USD 8.006142 actual.

## Cause (verified)

Calls were taking about 15 seconds each against 4.25 in q0-007. Measured API latency was normal (3.7 seconds mean over 40 calls) and the hub answered in 0.08 seconds, but the worker sat at 100% CPU. The `settled_usd` total that design v9 added to every ledger read rebuilt the set of answered calls once per reservation, which is quadratic in ledger size; with about 2,150 calls each read cost seconds, and every model call reads the ledger about four times. The cap arithmetic itself was correct. P1 would have grown the ledger further and slowed each call several-fold, hitting its 14,400-second limit after a few hundred of about 1,500 calls and breaking P1's paired arms. The offline tests used ledgers of a few events and did not measure time.

The worker was stopped with SIGTERM at 08:14 UTC; the wrapper and chain exited. Because fixing `provider.py` changes the engine hash, q0-008 could not qualify P1 even if completed.

## Experiment-quality assessment

- The eight finished episodes are valid observations of the q0-008 configuration and are retained, but they are not a qualification and are not pooled into q0-009.
- Fresh roots: the q0-008 selection rule finds no further roots up to 3,000 whose structures no model has run on, once 257, 282 and 293 are excluded. q0-009 therefore repeats q0-008's exact 24 assignments. Nothing about the model, prompt or scoring changed in response to the eight outcomes; the only change is ledger performance. Root 257's structures (D1 `d0ba6779`, D2 `7e8cef61`) and 282 D1 (`4b181182`) have now been run by this model once, which q0-009 records.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause | Repair | Acceptance check | Status |
| --- | --- | --- | --- | --- | --- |
| Q008-1 / execution | 15 s per call, worker at 100% CPU, API latency 3.7 s | Verified: quadratic `settled_usd` sum in every ledger read | Compute the answered set once (`settled_micro`); regression test reads a 6,000-call ledger in under 0.25 s | Offline: 2,200-call read 0.026 s; q0-009 pace near q0-007's | open |
| Q008-2 / operations | Record says 08:24Z launch | Operator wrote the wrong time | Corrected here and on run-queue 219 | – | closed |
| P1-1 / design | P1 needs a passing Q0 at v9 hashes | Unchanged from q0-007 post-mortem | q0-009 → p1-002 chain at the repaired source | q0-009 passes and P1 completes 168 | open |

## Next run

[q0-009](q0-009-pre.md) → p1-002 at the repaired source, same claim and server.
