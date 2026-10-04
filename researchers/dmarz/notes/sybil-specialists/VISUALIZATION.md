# Visualization mapping v1

This view explains where verification spends its budget, which identities receive admission, and what happens to specialist task completion. Every replay binds to run ID, source commit, design digest, stage, cell and first assigned world in replay_source.json. Each of the four panels follows one arm on the same world. The positions are fixed schematic community layouts, not physical coordinates or inferred communities. They never enter actor observations.

Signal mapping:
- world.public.adj: observed graph edges, thin gray lines.
- world.truth.honest: evaluator-only circle (honest) or triangle (adversarial), labeled as an overlay.
- trace[t].admitted: solid teal honest nodes or solid coral adversarial nodes; unadmitted nodes are hollow gray.
- public.trusted: square outline around initial seeds.
- trace[t].passed/failed: gold check ring / crossed-out node. The most recent event has a white outer ring.
- trace[t].metrics.rare_accuracy: correctly resolved rare skills / 3, displayed as 0–100%.
- trace[t].metrics.honest_rejection: honest excluded / honest population, 0–100%.
- trace[t].metrics.malicious_admission: admitted adversarial / adversarial population, 0–100%; clean worlds explicitly show N/A.
- trace[t].metrics.correct_skills: integer correct count / 6.

Time is logical verification step zero through the assigned check budget. The graph-only reference remains unchanged while other panels use checks. Frames record actual discrete states; no interpolation. One frame per step, maximum nine frames. Playback is 1.1 seconds per step with a 2.4-second final dwell. These delays are presentation pacing, not simulated work time. The GIF offers automatic playback; the final PNG is the static fallback. Zero-budget cells have static initial/final images because nothing changes.

All frames are 1800 by 1180. The worker uploads an initial image while running, then final PNG and replay GIF. Raw history is append-only episodes.jsonl; replay_source.json is sufficient to rebuild the selected replay. No additional API calls are made to produce visuals. Every cell uses its first preassigned seed even when it performs poorly. Full-batch summaries are separate from the single-world replay.

The public live site's supported image artifact contract is used; arbitrary graph JSON or HTML is not assumed embeddable. Detailed JSON artifacts remain authenticated. The image legend explicitly marks simulated data and evaluator truth. No IPs, credentials or private endpoint data enter artifacts.

Validation checks image dimensions, GIF frame count and unchanged source traces. Manual review checks initial/event/final readability and final numbers against the trace. Actual browser image loading and animation are verified after fleet deployment. Engine failure is retained as invalid and blocks completion; a missing render is an execution defect, never represented as a successful blank frame. Renderer failures preserve raw traces and require a new reporting repair with linked provenance before escalation.
