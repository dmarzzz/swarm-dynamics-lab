# Post-mortem: s0-fleet-002

Experiment market-split-api, dmarz/market-split, S0, 2026-10-04 UTC. Parent q0-001-post.md; pre-run s0-fleet-002-pre.md. Disposition: advance to q0-002.

Six planned/started/terminal/graded/analyzed bundles; 12/12 valid episodes; 96 mock requests; zero paid calls or additional dollars. All six competence and visualization gates pass. All 11 network-blocked tests pass including overlong-note rejection and raw-response retention. Source 0e2d833a6369ec1a62c79a005a9477ed84dc3b5c; engine f8f1cd9695d37e40a12de76cca812404885a6b55bd230b096d8a5d976bcd9290; design 1958c4850b7572b92e35d35030058e5272d2bf3126dcc7a93f2f9596934916f6. Reproduction uses coordinator.py stage S0 --attempt s0-fleet-002 and finite worker max-runs6, with new IDs for any future attempt.

## Visualization review

Mapping market-split-api-v1 delivered six progress PNGs, final1800×1200 PNGs and1080×720 eight-frame replays, no errors. All42 uploaded hashes match remote and recovered local files. Browser opened bb54db606803 and shows the measured mock trajectories and event markers. Full traces retained with each run. Worker exited0.

## Quality and failures

This tests revised interface plumbing, not model compliance or natural strategy discovery. It does not close the real-model note-length or production-competence issue until fresh Q0 passes. No simulation failures, missing or duplicate observations. The previous failed/cancelled Q0 remains on the hub. Its administrative cancellation initially used an unsupported report event kind; corrected to supported log/status=cancelled and read back, with zero additional model calls. A verification probe reached the final run while still running; repeated after worker exit and all hashes passed.

## Next run

q0-002: tasks22/23 seed31, no regulator, both arms/eight rounds; four episodes32calls. Same model, revised neutral prompt, unchanged100%-valid/positive-profit/75%-reference floor. Ledger still4 attempted/4priced calls and $0.004958. Max1,100 aggregate calls and shared$500 directive remain; no new cap. Stop/retain any failure, diagnose with fresh fixtures if needed. S1 blocked until this Q0 passes; S2 disabled.
