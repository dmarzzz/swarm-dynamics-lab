# Post-mortem: s0-local-002

- Stage: local scripted S0 on the amended full-grid design, orbital-one, 2026-10-04 ~06:00Z, operator dmarz/budget-sonnet. No model calls, $0.
- Outcome: **pass** (engineering). This is not model evidence.

## Reconciliation

256 assigned → 256 started → 256 terminal → 256 graded → 256 analyzed; 0 invalid, 0 not started. These are 240 pilot rows (2 engineering worlds × 120 cells) plus 16 clean controls. Clean controls at N=324: 8/8; at N=972: 8/8. Field accuracy, exact packets and missing-fact abstention are 100% at both sizes. The same 256-row count as the parent's fleet S0 (`sybil-budget-api/4346fc36`, 256/256 valid).

## Instrument checks

- Selftests 10/10 pass on the amended design. The pairing test checks that `design.yaml` differs from the parent's only in experiment, model, budget (caps and prices), the review note and the replication note, and that Q0/S1 assignments match the parent's for one scientific and one qualification world. `reporting/parity_check.py` covers all 2,896 assignments; its receipt is committed at the final source hash.
- Frames: initial, final and retention PNGs at 1920×1440; GIF with 25 frames; labelled S0 SCRIPTED.

## Issues

None new. The earlier N=972-only local attempt (`local-s0-001`) is superseded by the design amendment and kept.

Next action: **advance** to fleet S0 on the claimed host after the registration commit.
