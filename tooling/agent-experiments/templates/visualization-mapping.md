# Visualization mapping: <run or attempt ID>

- Mapping version / source commit / parent mapping:
- Run ID(s), design/config version, task/seed/arm bindings:
- Behavior this view should make understandable:
- Live view, final frame, and animation/replay design:

| Recorded signal / exact field | Unit, denominator or derivation | Visual encoding / legend / scale | Actor-visible or evaluator-only | Missing/failure display |
|---|---|---|---|---|
| <field> | <definition> | <position, color, shape, axis or trace> | <access boundary> | <explicit state> |

- Time axis and origin: logical step / wall time; comparison alignment across arms:
- Important event markers and their recorded source:
- Snapshot/sampling cadence; upload throttle; maximum frames/points/bytes and rendering overhead:
- History/replay input artifact, ordering, stable entity IDs and downsampling policy:
- Live artifact/schema, final image, animation/replay format and embedding destination:
- Supported player controls, or labeled time cursor and static fallback:
- Why static-only/no animation is appropriate, if applicable; unsupported features and fallback:
- Public-safe fields, evaluator-truth separation, uncertainty and accessibility choices:
- Synthetic-trace validation: normal progress, event transition, missing data, injected failure:
- Acceptance checks for initial/event/final frames, metric agreement and actual playback:
- Rendering failure policy and post-run artifact owner:

Reference an unchanged experiment-level mapping by version if useful, but fill the run-specific bindings. This mapping describes planned instrumentation; it does not imply that rendering or dashboard integration already exists.
