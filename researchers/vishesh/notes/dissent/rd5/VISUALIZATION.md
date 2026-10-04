# RD5 visualization mapping v1

Bindings: Q5-A1 interpretation pairs and H5-A1 six roots × B0/B1/B2 × epochs 0–3. Run IDs are prospective names; neither has started. Source and configuration hashes travel in the prepared packet. Rendering reads saved files only and consumes no experimental RNG.

The live fallback is the worker's JSON progress stream (`progress`, `assigned`, `stage`), accompanied by a saved `replay.html` refreshed after each terminal outcome. Serve/upload that saved page using the existing hub artifact workflow at deployment; no additional model or experimental worker is needed. The final same page includes a time slider and play control, so a video dependency is unnecessary for this bounded temporal pilot. Raw records remain downloadable. Q5 is a non-temporal paired table; animation adds no scientific information there.

| Signal | Source and units | Encoding |
| --- | --- | --- |
| Time | `tick`, simulated ticks 0/2/4/6 | Slider reveals assigned opportunities cumulatively; final position includes all. |
| Current decision | `action` | PROCEED green, HOLD amber, DEFER lavender; explicit words retain accessibility. |
| Historical decision | `historical_action` | Separate column; never shown as current authorization. |
| Supplied truth | evaluator-only `truth` | Separate reader column; absent from actor requests. |
| Capacity | `available_checks`, count 0–2 | Numeric column aligned with each decision. |
| Physical/inference distinction | `acquired`, `inference_attempted`, saved state receipt events | Separate booleans; a native failure does not erase acquisition. |
| Evidence/eligibility | `frontier`, `reason`, saved `state-*.json` source receipts | Reason column and full JSON provenance; aliases do not become new acquisitions. |
| Missing/failure | manifest status versus terminal row | UNSTARTED stays visible; failed interpretation is DEFER with failure reason, never a correct outcome. |

The [scripted preview](validation/scripted-preview/replay.html) renders an existing urgent-delay unit fixture and a deliberately missing display slot. Its four decisions are **SCRIPTED — NOT MODEL EVIDENCE**. The fifth display-control slot is not part of H5's design. Inspect initial, transition and final slider positions. Metrics come from records, not pixels or a plotted subset.

Before closeout verify displayed per-arm counts and every missing cell against the manifest/summary, save the final frame or screenshot and replay, upload/read back hashes, and record availability in the post-mortem. Rendering and uploads can be repaired from saved data without rerunning Jev.
