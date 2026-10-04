# Visualization mapping v1

Bound to every run through source_hash, stage, batch, task, arm, attacker_pass and visibility. S0 labels SCRIPTED, Q0/S1 labels HAIKU 4.5. The graphic shows cumulative measured accuracy, with separate visibility × attacker-pass panels for S1; Q0 panels instead show full/common-only × badge mode. The plotted denominator is the valid completed rows in each cell, displayed alongside planned/completed/invalid/not-started counts.

| Recorded signal | Encoding | Access | Missing state |
|---|---|---|---|
| evaluation.rare_accuracy (S1), qualification_accuracy (Q0) | Blue horizontal bars on fixed 0–100% axes; printed value and n | Evaluator-only | Pending text, no zero imputation |
| scripted_evaluation same metric | Gray thin reference bar, same rows | Evaluator-only | No estimate until call completes |
| evaluation.malicious_admission | Printed red percentage, fixed underlying admission policy | Evaluator-only | Not applicable for clean tasks |
| validity, status | Footer assigned/completed/failed/not-started | Operator | Explicit counts |
| completion_index, elapsed_seconds | Cursor of recorded call completions, elapsed-time label | Operator | Not an LLM reasoning trajectory |
| accounting.actual_usd/reserved_usd | Printed spend and conservative reserve | Operator | Uncertain spend retains full reservation |

Time is call completion order, not simulated verification steps. Save a JSONL row after every terminal result and fsync. Render an initial image, live update at most every four calls, and final image. Retain snapshots every eight completions plus any failure/final, at most 30 frames, 1800×1180. GIF playback labels frame/call cursor; static final image is fallback. A GIF loops and provides no scrubbing; raw records reproduce exact timestamps and fine-grained progression. Upload final image before replay and refresh the initial image metadata so the contact sheet leads with final.

No graph-truth overlay enters prompts. Public frames contain only synthetic aggregates, public experiment/run labels and model identity. Color is redundant with text and numeric values. Every replay frame is rendered from a prefix of saved records; no interpolation. Offline tests check pending/failure rendering, dimensions, frame count, first/last data consistency and packet blindness. Post-run verification checks hashes, image decoding and actual browser playback. Rendering/upload failure stops promotion and keeps the server claim through repair.

## Reporting amendment v1.1 — 2026-10-04 UTC

During S1 inspection, the run's generic hub usage series was found to mix cumulative study values during progress with stage-only totals at completion. This does not affect the API budget ledger, saved per-call usage, terminal stage totals, model outputs or accuracy figures. Original traces are retained. The worker now reports stage usage consistently and omits the non-applicable Q0 rare-accuracy placeholder. A new offline regression begins with an already-spent ledger and verifies first/last stage usage and carried study totals.

The initial frame previously defaulted to zero spend even when Q0 had already incurred cost. The analysis replay now binds its initial accounting to the completed Q0 ledger snapshot and all subsequent frames to the saved S1 study_accounting field. It replays the same 192 model observations, makes zero new requests, and records a separate analysis commit. Original experiment artifacts remain available unchanged. Final values and scientific comparisons are identical. The corrected worker has a new runtime hash, so any future paid batch must qualify that hash first; this is not a retroactive claim that it generated the completed pilot.
