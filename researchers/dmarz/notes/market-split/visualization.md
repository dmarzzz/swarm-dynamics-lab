# Visualization mapping market-split-v1

Bind every view to run ID, code/design hashes, policy, and first configured task/seed, selected before outcomes. The replay is one paired illustration, not a batch average.

- Policy rows contain stable firm IDs. Teal firms belong to the focal owner; gray firms belong to distinct rivals. Labeled segment boundaries separate firms. Two stacked bars show production of A/B in units. The ownership overlay is evaluator-only except for the published owner rule.
- `trace[t].firm_hhi` and `.owner_hhi` map to solid/dashed per-good traces on a fixed 0–1 axis; the dotted line is the threshold. Zero-output HHI is missing, not zero, and is never interpolated.
- `operation == register` marks registration events. `owner_profit`, `owner_fines` and `firm_count` display cumulative credits, cumulative credits and entity count. Actor inputs exclude evaluator counterfactuals.
- Time is completed simulated round, starting at 1; rows align by logical time. Every round is retained. Final PNG is 1800 × 1200; GIF is 1080 × 720, at most 24 measured frames, 350 ms each with a final hold. No smoothing.
- Upload `progress.png` at most every three seconds for the preselected episode. Upload `final_frame.png`, `replay.gif`, and complete `episodes.jsonl`. No custom JSON is misrepresented as the spatial `frame.json` contract.
- The public run UI embeds PNG/GIF. There is no pause/scrub control in the image viewer; the round cursor and final PNG are the fallback. Verify real image loading and GIF playback.
- Failed rows say INVALID, retain the last real round and show failure type; rows not yet run say PENDING. Never plot missing values as zeros or continue after failure. Hub metrics report all batch invalid episodes.
- Rendering does not touch simulator RNG or observations. Catch renderer failures, preserve/upload raw traces and `visualization-errors.json`, and fail qualification. Maximum replay size 12 MB, one worker.
- Synthetic tests cover registration and failure. Verify initial, pre-registration, post-registration and final frames against traces, dimensions and frame count. Artifact review owner: dmarz/market-split.
