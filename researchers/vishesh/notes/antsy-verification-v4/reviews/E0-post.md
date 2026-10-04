# E0 post-mortem

Source e5d684e; exclusive sim-test-01. All100 receipts and 300 OCR calls completed, zero invalid outputs. Calibration inspected only IDs0–19; evaluation outcomes were not inspected during policy construction. Calibration results are retained in results/E0/calibration.json.

Observed calibration mean recall: A 0.3209, B 0.6023, C 0.5235. Per-receipt best configuration mean 0.6683;6.60 pp headroom over fixed B, above the predeclared1 pp relevance gate. Calibration winners A2/B13/C5; this is development evidence only. It establishes real routing opportunity, not agent competence or achievable gain from two checks.

No execution repair or outcome retry. One implementation-only change after E0 moved the pyarrow import into main so the scorer can be unit-tested without loading a dataset; scoring is unchanged. Ten scorer/policy tests pass, including spatial assignment, duplicate token accounting, evaluator blindness, paired stopping and hard budgets. Two actual PNG and two three-frame GIF smoke artifacts decoded successfully.

Reporting gap: E0 was executed under the committed pre-run plan, but its progress was checked through operational counters rather than streamed to the hub. The calibration summary is published retrospectively, labelled accordingly. S0/S1 report progress directly. This is a visibility defect, not evidence that OCR was rerun or that a live timeline existed.

Decision: proceed to S0 under c2dffda, then assess its interface/instrument qualification before S1. The immutable plan and condition TLDR were registered on the public experiment page before model launch; browser inspection verified the c2dffda README link. Jev is a separately authorized future condition, not a silent replacement of this Laya freeze.
