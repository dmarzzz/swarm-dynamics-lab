# D0 post-mortem

2026-10-04 UTC; source b9cc1f919344a9f557713e1ff141b62573b4a528. Execution complete: 70 reused receipts, 2,940 condition rows, 13.30 seconds excluding upload overhead, zero model calls. Original choices/qualities reproduced across both seven-arm histories; input purchases matched stored truth. Independent reconstruction of repaired choices and numeric scores passed. Output assignment is complete and unique.

Null-neutral changes Laya committee recall from 56.30% to 57.78% (+1.48 points), harmful switches 4→3; Jev 55.72%→56.47% (+0.74), harmful switches 5→2. Global-empty gives 56.44%/55.89%, with 6/4 harms. These are estimator interventions under fixed past purchases, not observed behavior of a newly prompted agent. The different outcomes justify preserving the global-empty sensitivity rather than silently treating all missing data as equivalent.

Cause confidence: null deletion changes rankings mechanically; regression fixture and recorded-case replay verify this. The null-neutral contract eliminates that mechanism exactly. Residual harmful changes from real regional evidence remain: the coarse estimator is still not a calibrated whole-receipt model. The old evaluation receipts are development data now; no independent win is claimed.

Visual mapping: comparison PNG and eight GIFs (first three IDs plus each backend's worst original loss) generated from saved events, with truth only at final frame. PNG/GIF dimensions and decoding are verified after retrieval. Worst-case additions are explicitly post-hoc diagnostic examples. The run is short, so start/done progress plus retained trace replaces streaming live frames.

Next action: D1 bounded cost-aware baseline diagnostic, not a paid-model sweep. Evaluate stop/continue and utility sensitivity while retaining ideal QA and equal-region limitations. New practical field-level evaluation remains gated on measured checker behavior, actual review costs and fresh document families.
