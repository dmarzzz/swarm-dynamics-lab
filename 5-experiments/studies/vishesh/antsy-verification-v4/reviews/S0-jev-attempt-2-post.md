# Jev S0 attempt 2 post-mortem: rounding mismatch identified

The recovery replayed67 previously valid responses without network requests. Its first new response was rejected by our probability-sum check. Safe diagnostics now identify the cause: returned probabilities A0.17/B0.55/C0.04/STOP0.23 sum to0.99. The selected label B is the maximum; labels, model, provider and usage are valid. This response is consistent with rounding four probabilities to two decimal places. The adapter's0.001 sum tolerance was too strict for this observed representation.

This is an adapter rejection, not an OCR decision-quality failure. The first attempt's unrecorded validation reason remains unknown; rounding is plausible but not proven for that earlier event. Do not retroactively invent its response.

Repair: for a vector entirely on the observed0.01 grid, accept a sum within half a rounding unit per component (4*0.005 here); retain the stricter0.001 tolerance for other precision. Still require all labels, finite values in[0,1], the pinned route, valid usage and selected-label argmax consistency. Never renormalize probabilities or change the selected action. Record this representation rule and test acceptance/rejection boundaries.

The captured response can be revalidated locally under that documented rule. It becomes the68th reusable response with explicit schema-recovery provenance. No new request is needed for it. Preserve both failed attempts, then complete missing invocations in attempt3 under the unchanged task/policy and budget. Jev S1 remains blocked until that succeeds.
