# Pre-run assessment: fleet-s0-001

- Experiment / owner / stage: sybil-specialists-opus / dmarz (operator dmarz/orbital-orchestrator) / S0, scripted, 0 model calls.
- Previous evidence read: Sonnet version [fleet-s0-001-post](../../sybil-specialists-sonnet/reviews/fleet-s0-001-post.md) (216/216, admission identical to Haiku), and the Haiku S1 post-mortem.
- Status: **ready**.
- Question: does the amended runtime pass every scripted invariant on the host? The amended runtime has Opus request handling, fresh Q0 worlds 3100–3105 and the new caps. S0 must pass at the exact runtime hash before Q0 can be queued.

## Changes and acceptance

| Change | Acceptance check |
|---|---|
| Q0/S0 qualification worlds 3100–3105 | Scripted qualification 24/24 exact; S1 attacker admission still matches Haiku cell for cell |
| Provider: no temperature, effort low, thinking blocks ignored, refusal is a failure | Offline tests (15/15) |
| Hub id `sybil-specialists-opus`, render label OPUS 5.5 | Run appears under the new id; final frame label |

## Frozen plan

- `python3 scripts/run-sybil-specialists-opus.py <commit> setup`, then `S0`, `status`, `verify` (agentops).
- Host sim-dmarz-4, exclusive claim `dmarz-sybil-specialists-opus` held by dmarz/orbital-orchestrator.
- Dedicated checkout `/srv/swarm/sybil-specialists-opus-lab`, venv `/srv/swarm/sybil-specialists-opus-venv`, ledger `/srv/swarm/sybil-specialists-opus-budget/ledger.jsonl`.
- No credentials are sent for S0.
- Visualization mapping v1.1 is unchanged (see [VISUALIZATION.md](../VISUALIZATION.md)).
