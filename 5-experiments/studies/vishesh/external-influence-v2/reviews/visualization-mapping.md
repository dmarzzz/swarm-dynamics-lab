# Visualization mapping: influence-replay-v1

Retrospective mapping, 2026-10-04; original run external-influence-v2/38908910, source b107b1636c852b946ecf7e7e7383cec8810d0eda. Bindings are assignment index plus domain/task/seed/world/arm from manifest.json. This analysis does not change the experiment or consume model calls.

| Recorded signal | Units and derivation | Encoding | Access boundary | Missing state |
|---|---|---|---|---|
| Ordered initial/revision response estimates | Apply original public rubric to each observed report | Six stable analyst positions; selected candidate label | Agent-visible estimates; truth-based color is evaluator-only | Gray pending node until response |
| Checker result and package | Scope commercial to cost, technical to quality/latency/requirements | Two cards display exact recorded values | Tool observation; no evaluator reveal | Pending/unavailable label |
| Chair response choice/confidence | Exact response | Final chair card | Agent output | No final choice until observed |
| Episode correctness/harmful_target | Original scorer | All-case matrix green/coral/gold/gray plus text | Evaluator-only | Invalid explicitly distinct from other errors |
| Reapplied rubric on recorded reports/checks | Deterministic retrospective counterfactual; no truth in choice | Separately labeled audit card and score table | Analyst/check data; truth used only for assessment | Not a measured repaired-run outcome |

Logical time is ordered model response index 0–15, not wall-clock duration or simultaneous asynchronous events. Every recorded response is retained. The GIF has 16 frames (initial pending plus 15 responses), with a longer final pause. No interpolation or smoothing. The browser player supports pause, scrub, speed, selecting all 50 cases and inspecting the verified scorecard. Actor IDs are recovered from the v2 fixed phase/call order; future runs record them directly.

The supported public surface receives final_frame.png and measured_replay.gif; interactive HTML is a separate self-contained artifact because arbitrary HTML is not embedded by the live site. GIF playback and a static final frame are the fallback. Raw history remains in hub artifacts; the derived audit records SHA-256 of all input files. Renderer failure cannot change a historical decision or cause a model retry.

Acceptance: reconcile 50 assignments; verify six initial and revised choices against episodes.jsonl, two check responses, final choice and 15 responses per complete case; assert every matrix label matches the original evaluation; inspect initial/final PNGs, GIF frame count and playback, and browser controls. No secrets are in data: every candidate and price is a fictional fixture. Color is redundant with text; no actor/frame is treated as an independent sample.
