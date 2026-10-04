# Visualization mapping v1

Bound to sybil-budget-api S0/Q0/S1 and the runtime hash in every run. It shows how verification budget and attacker check-pass probability affect information recovery, attacker seats and honest specialist retention. The data are simulated identities plus one model synthesis per cell/world; no animation depicts autonomous identity conversations.

| Recorded signal | Definition | Encoding | Boundary | Missing/failure |
|---|---|---|---|---|
| evaluation.rare_accuracy | Correct specialist fields /3 | Main heatmap percent; fixed0–100% scale | Evaluator-only | Pending blank, failed count retained |
| evaluation.bad_seat_share | Attacker admitted /all admitted | Main heatmap percent; fixed0–100%, lower is greener | Evaluator-only | Same |
| evaluation.specialist_retention | Honest specialists admitted /all honest specialists | Companion retention heatmap; fixed0–100% | Evaluator-only | Same |
| checks; attacker_pass; n; arm | Frozen assignment | Columns, rows, panel title | Design labels | No interpolated cells |
| observed joint target | Mean accuracy≥90% and attacker seats≤5% with all24 worlds complete | Yellow cell outline | Evaluator-only | No outline for partial cells |
| completion_index; elapsed_seconds | Recorded response completion order and stage wall time | Replay frame count and header | Operational | Failed/not-started explicit totals |
| accounting | Actual and reserved model dollars | Footer | Operational | Missing usage stops dispatch |

Final `final_frame.png` is a 1920×1440 grid: random and coverage side by side; N324/N972 and accuracy/seats panels vertically. `retention.png` uses retention/accuracy panels. Q0 shows clean competence and missing-fact abstention separately. S0 is prominently labeled SCRIPTED. Live `progress.png` uploads at most once per20seconds plus final. Initial/final/replay use the same renderer; dimensions support the project figure floor.

The 25-frame GIF uses evenly spaced prefixes of actual recorded call completion order, at most24 transitions, 600ms each and2500ms final. Prefix cells have unequal counts and are preliminary; the replay is collection progress, not physical-time behavior or changing treatment effects. No observations are interpolated. Source histories are `episodes.jsonl.gz`, `assignments.jsonl.gz`, `worlds.jsonl.gz`; completion indices and elapsed seconds preserve replay order. The GIF has a visible completed/total cursor and static final fallback, but no built-in scrub control. Hub public image routes are the intended surface; raw histories remain in authorized storage. The coordinator/root operator verifies embedding/playback before closure.

The renderer never modifies experiment RNG or packet contents. Test empty, partially populated, injected failed, complete and Q0 states; check cell means and target flags against saved records; decode all frames and inspect a final image. Rendering failures enter `reporting_errors`; raw science stays intact and the post-mortem must repair/re-upload visuals from saved traces before closure. Palette runs muted red to teal with numeric percentages and clear labels, so color is not the sole encoding. Intervals stay in analysis tables; the image explicitly says means and does not imply simultaneous precision.
