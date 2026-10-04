# D1-Opus deployment record

No IPs, credentials or private inventory here. Times UTC, 2026-10-04.

| Item | Value |
|---|---|
| Server | `sim-dmarz-9` (new one-run dmarz box, nyc3, expires 2026-10-05; fleet entry and targeted create recorded in agentops) |
| Claim | `dmarz-d1-opus`, by `dmarz/d1-opus`, exclusive, 8 h from ~07:45 (agentops PR #203) |
| Source | swarm-lab `573c4103bb411fec1b37f2288ef859737aafe839` |
| Frozen manifest | `d1o-a1.frozen.json`, sha256 `29f0c9ce20012f3ec4fd3c6f1c55b35341608cc337097d7db7f61e927115a921` (identical when rebuilt locally) |
| Inputs | retained Q0 `v3-q0-a1` files fetched from hub artifacts; all four match the published audit receipt |
| Operator | agentops `scripts/run-d1-opus.py` (claim check; key via SOPS → ssh stdin → process memory) |

## Attempts

| Attempt | Stage | Result | Calls | Cost |
|---|---|---|---|---|
| `d1o-a1-rehearsal` (first launch) | zero-model rehearsal | stopped before execution: the CLI child lacked the `swarm_report` import path; no ledger marker, zero calls. Launcher repaired (ce283c2 → next agentops commit) | 0 | $0 |
| `d1o-a1-rehearsal` | zero-model rehearsal, hub run `discussion-v3-d1-opus/d1o-a1-rehearsal` | 72/72 terminal, 0 physical calls, audit recomputed all 72, 7 artifacts uploaded and read back; scripted reader 12/12 fresh (gate correctly unpassed, not model evidence) | 0 | $0 |
| `d1o-p1` | one-call interface probe, dev world 10002 (not scheduled or scored), hub run `discussion-v3-d1-opus/d1o-p1` | valid parsed answer, `stop_reason` end_turn, returned model `claude-opus-5-5`, 4,052 input / 313 output tokens, 5.4 s | 1 | $0.022468 |
| `d1o-a1` | 72-call diagnostic | **not started**: waiting for dmarz's first-hand go-ahead and G0 review decision | 0 | $0 |

Expected `d1o-a1` cost from the probe's per-call usage: about $1–3; worst-case reservation $25.26 (cap $30).
