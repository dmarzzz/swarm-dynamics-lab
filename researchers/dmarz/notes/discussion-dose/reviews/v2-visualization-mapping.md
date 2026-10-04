# Visualization mapping: discussion-dose v2, mapping v1

- Mapping version / source: v1, `src/frames.py` (FrameTracker) and `src/replay.py`; renderer `site/public/js/delib.js` in swarm-labs-agentops.
- Bindings: one replay per hub run. Each frame carries world (task id), arm (attack, rounds), level, stage (acquisition or continuation) and phase. Runs before this mapping (H1 to H4 calibration, v2 S0-H4 `723dad8e`, all v1) get replays backfilled from their saved event journals with `src/replay.py`. No model calls.
- Behavior to make visible: whether the injected value spreads from the exposed agent to the witness and swing agents, and whether discussion rounds repair or entrench it. Consensus on a wrong value is not correctness.

| Recorded signal / exact field | Derivation | Encoding | Access | Missing / failure |
| --- | --- | --- | --- | --- |
| Agent's latest endorsed value of the target key (`call_response.response.claims`) | `false` if it equals the injected value, `true` if it equals the clean value, `other` otherwise | Node fill: violet = false, bone = true, grey = other | Evaluator-only label (agents never see which value is true) | Hollow node = not stated yet |
| Agent vote (`ballot.vote`) | Latest ballot response | Letter in node; `∅` = ABSTAIN | Actor output | `·` = no ballot yet |
| Current majority of shown votes | Strict majority of the three latest votes | Centre letter; violet if attacker's option, bone if correct | Evaluator-only colouring | `–` = no majority |
| Role (exposed, witness, swing) | `world.roles`, fixed per world | Node position and label | Evaluator-only | n/a |
| Speaking agent (`call_start` without response yet) | Pending call | Blue ring | Host | Ring stays if a call failed; the failure shows in the tally |
| Latest public message (`report` or `discuss` message) | First 160 characters | Text under the triangle | Actor output (public board) | Empty when no post |
| False endorsements per checkpoint | Count of `false` across the three ballot probes at each round | Column of three cells per round | Evaluator-only | Unfilled column = checkpoint not reached |
| Tally: episodes, attacker wins, false memory, clean correct, invalid | Sum of `evaluation` fields over finished episodes | Bottom-right text | Evaluator | Invalid episodes counted, never hidden |

- Time axis: logical event order. Each replay frame is a snapshot after a model response, a round barrier, a memory merge or a failure. `ts` is wall time when the host processed the event. Arms are separate episodes, so no cross-arm alignment is implied.
- Event markers: phase and round in the header; episode boundaries move the tally.
- Cadence and bounds: live `frame.json` at most every 3 s (plus once per finished episode); replay of at most 3,000 snapshots, halved 2:1 if exceeded (`thinned` counts halvings); about 2.5 KB per frame.
- Live view: run page canvas while running. Replay: `replay.json` uploaded at the end, played on the run page with play, pause, scrub and speed. Fallback: the hub's numeric metrics.
- Public safety: fictional worlds only; messages truncated; the site proxy rebuilds frames from a typed whitelist and masks IP-like strings.
- Validation: `selftest_v2.test_frames_and_replay_match_records` runs a synthetic trace with an injected provider failure and checks the final replay tally against records (episodes, invalid, attacker wins, clean correct). The backfilled H4 calibration replay reproduces hub metrics: attacker 5/12, false memory 11/12, clean 10/12, invalid 0.
- Rendering failure policy: tracker and upload errors are swallowed and never alter calls, records or the hub's terminal status. A missing replay is recorded in the post-mortem.
