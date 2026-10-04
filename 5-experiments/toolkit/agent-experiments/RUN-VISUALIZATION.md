# Visualizing run progress

Owner preference, 2026-10-04 UTC: frames are a standard part of understanding a run. Prefer an embedded time-series animation or replay that reveals how behavior changes over time, alongside quantitative traces. Design a small **Visualization mapping** section for every run before launch. The process is standard; the visual design is specific to the experiment.

## Map the experiment to a view

Use [visualization-mapping.md](templates/visualization-mapping.md) within the run's pre-run assessment or as a linked versioned file. Each attempt binds it to its run ID, design/source version, task/seed and arm. A batch may share a versioned mapping, but each run must identify its own binding and time origin. Name:

- The behavior a viewer should understand: convergence, propagation, disagreement, containment, repair, relapse, or another mechanism.
- Exact recorded fields, units and denominators; derived formulas and whether a signal is actor-observable or evaluator-only.
- What position, color, shape, trails and chart axes mean; stable identities, legend and fixed scales for comparisons.
- Logical time versus wall time, sampling and upload cadence, event markers, and explicit missing/failed/pending states.
- Live view, final frame, retained history, animated/replay artifact, embedding destination and fallback.
- Rendering/resource bounds and validation checks. Keep rendering separate from the experiment's decision logic and random-number stream.

## Choose views that expose the mechanism

| Run type | Useful live frame | Time-series animation/replay | Event markers and cautions |
|---|---|---|---|
| Convergent solution | Current candidate/state, objective and residual or distance to a declared reference | Evolving candidate with synchronized objective/residual traces and convergence threshold | Initialization, updates, threshold crossing, stall; distinguish improvement from actual convergence and avoid undocumented smoothing |
| Damage and repair | Agent/private/shared-state panel with affected, contained, restored and unavailable states | Playback of damage propagation and repair alongside useful-completion and harm traces | Damage onset, containment, restoration, stale reintroduction, legitimate update, relapse; cumulative harm never resets after repair |
| Consensus | Distribution of opinions/votes, committed state and evidence-source relationships if measured | Agent-state evolution synchronized with agreement, correctness, confidence and decision latency | New evidence, dissent, vote/commit, reversal; agreement alone is not correctness and claimed independence is not measured independence |

For immune-response v2, an illustrative mapping uses round `t`, arm, per-round `utility`, `forbidden`, `affected`, and `failures`, marking incident rounds 4-6, intervention before 7, stale return at 13 and legitimate update at 18. These are a proposed view of already-recorded fields, not a claim that frames have been implemented. Store hashes alone cannot reconstruct full private/shared contents; record additional sanitized snapshots prospectively if the visualization needs those contents. Label oracle affected-state overlays as evaluator-only.

## Use supported display contracts

The private agentops `docs/REPORTING.md` defines the actual hub contract. At the time of this amendment, the public live site supports:

- Replacing `frame.json` approximately every 2-5 seconds for spatial point views with `{L, t, x, y, th}` (coordinates and headings in radians, at most 20,000 points). Use this only when its semantics fit the run, and validate array lengths, bounds and finite values. It is a latest-frame view, not a durable time-series archive.
- Public PNG/JPEG/WebP/GIF artifacts, including a final frame for the contact sheet. A bounded animated GIF is a supported publication candidate; verify actual playback in the intended surface. Image support does not guarantee that every surface animates it.
- Other artifacts are private to the team. Do not assume uploading arbitrary JSON, HTML, MP4 or a custom frame schema makes it publicly embeddable. A richer player requires a separate supported renderer/integration. Use a clearly labeled image/animated-GIF fallback until that exists; keep detailed history in the authorized artifact store.

For a non-spatial experiment, prefer an annotated progress image and an animated time-series image over arbitrary invented point coordinates. Choose a publication cadence that is useful and bounded; render on logical steps but throttle uploads. Never make additional model calls just to animate a trace. Preserve append-only history or sufficient events for deterministic replay even when the latest display frame is overwritten.

## Make time and comparisons honest

Use a visible step/time cursor, labels and event markers. Provide pause/scrub/speed controls if the supported player has them; otherwise include a readable timestamp/round indicator in the animation and a static fallback. Keep histories and scales comparable across arms, use stable layouts and redundant labels/shapes as well as color, and identify wall-clock versus logical-step alignment. Show uncertainty only when justified by the analysis unit; do not turn actors or frames into independent samples. Do not interpolate through missing outcomes as if observed or hide failed arms. Label downsampling and any decorative interpolation separately from measured transitions.

## Acceptance and reporting

Before launch, test the mapping on a synthetic trace containing both normal progress and an injected transition/failure. Verify signal-to-frame agreement, event timing, legibility, missing-data behavior and bounded rendering overhead. A renderer failure must be recorded and must not erase raw results or silently change the scientific run; freeze an appropriate reporting-failure policy.

After the run, verify initial, pre-event, post-event and final frames against the saved trace, check animation playback/embedding where supported, and reconcile the final visual with the numerical summary. Record mapping version, artifact links, sampled time range/cadence, omissions and rendering failures in the post-mortem. Derive a view from existing traces when possible without rerunning the experiment. If past telemetry is insufficient, document the gap and collect the needed fields in a new version; never fabricate historical states.
