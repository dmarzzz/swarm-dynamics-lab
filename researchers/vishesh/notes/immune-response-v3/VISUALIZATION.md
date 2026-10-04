# Visualization mapping v3

Bindings: every design.json task × world × arm; logical rounds 1–24. Live/final mapping uses the same rendering functions as saved replay. The viewer should distinguish initial damage, apparent recovery, stale-induced relapse, and collateral loss of legitimate learning.

| Recorded signal | Encoding | Units / missing-state semantics |
|---|---|---|
| trajectory.utility | Request timeline: teal check / coral cross | One exact authorized deployment request; never interpolate |
| trajectory.failures | Gold exclamation overlay | Response-contract/provider failure, distinct from a scientifically wrong answer |
| cumulative recovery utility | Synchronized line chart | Correct requests / all recovery requests through the cursor, rounds 7–24 |
| private_status | Actor matrix of correct / wrong / missing | Counts out of twelve; evaluator-only, never actor input |
| shared_status | Shared store count display | Same evaluator-only categories |
| world / round | Event labels and cursor | Damage 4–6, repair before 7, replay 13 unless no_replay, true update 18; benign learning at 5 |

Stable arm identity and axis limits permit comparisons. Choose task/scenario/arm, scrub the timeline, or play once with pause. The interactive view starts at the final frame and moves only when requested. GIF preview loops with round indicators; use the static PNG or interactive manual scrub when reduced motion is desired. The GIF represents one labeled task/scenario; the interactive viewer includes every supplied outcome, including failed ones.

Artifacts: final_frame.png (1600×1000), replay.gif (24 measured-step frames), replay.html (self-contained, no network fetch), visualization-provenance.json. Existing public hub supports image/GIF artifacts; HTML stays a downloadable/local artifact unless a separate supported hosting integration is supplied. Do not invent frame.json spatial positions for this non-spatial ledger. The scientific source records are the JSONL outcomes/round events, not the animation.

Rendering reads retained telemetry only, makes no model calls and changes no policy state. Validate initial, damage, repair, replay and final frames against recorded events and numerical summaries. Historical v2 lacks private/shared counts: show its recorded affected IDs and explicitly mark fuller state unavailable. No historical state reconstruction from hashes. An interrupted trajectory shows missing/unknown cells. Empty/missing rows remain visibly incomplete rather than synthesized successes.
