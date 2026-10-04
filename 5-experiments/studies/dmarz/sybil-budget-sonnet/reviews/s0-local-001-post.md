# Post-mortem: s0-local-001

- Stage: local scripted S0 on orbital-one, 2026-10-04 ~05:45Z, operator dmarz/budget-sonnet. No model calls, $0.
- Outcome: **pass** (engineering). This is not model evidence.

## Reconciliation

128 assigned → 128 started → 128 terminal → 128 graded → 128 analyzed; 0 invalid, 0 not started. These are 120 pilot rows (2 engineering worlds × 60 cells at N=972) plus 8 clean controls. Clean controls: 8/8, field accuracy 100%, exact packets 100%, missing-fact abstention 100%.

## Instrument checks

- Selftests: 10/10 pass, including the new parent-pairing test (byte-identical sim/study/analyze; design differs only in experiment, model, sizes, budget, waiver and replication note; the budget block differs only in caps and prices; Q0/S1 assignment IDs, packet hashes and expected answers equal the parent's N=972 rows for one scientific and one qualification world).
- The full parity check over all 1,440 S1 and 8 Q0 assignments runs separately (`reporting/parity_check.py`); its receipt is committed as `reporting/parity-receipt.json`.
- Frames: initial, final and retention PNGs at 1920×1440; GIF with 25 frames. The final frame shows only the N=972 rows, labelled S0 SCRIPTED, with the lower half empty as the mapping states. The scripted plurality pattern (coverage 0% at 4–8 checks, random 50%) matches the parent's scripted behaviour at N=972 in kind. Not compared numerically here, since engineering worlds were not in the parent's S1.

## Issues

| Issue | Type | Resolution |
|---|---|---|
| The first selftest version recomputed the full parent S1 grid and exceeded a 10-minute limit | execution (test speed) | Selftest restricted to one world per stage; full check moved to `reporting/parity_check.py` |

Next action: **advance** to fleet S0 on the claimed host after the plan and registration commits.
