# Pre-run assessment: fleet-s0-001

- Experiment / owner / stage: sybil-specialists-sonnet / dmarz (operator dmarz/orbital-orchestrator) / S0, scripted backend, 0 model calls.
- Parent attempt: none. This is the first attempt of this study. Relevant prior evidence: the Haiku study's fleet S0, Q0 and S1 post-mortems in [../../sybil-specialists-api/reviews/](../../sybil-specialists-api/reviews/) were read before this assessment. That S1 reconciled 192/192 with no execution defects.
- Status: **ready**.
- Question: on the claimed host, does the copied runtime reproduce the scripted invariants with the Sonnet configuration (identical packets, ledger arithmetic at the new prices, renderer label, hub id)?
- Decision value: S0 must pass at the exact runtime digest before the coordinator will queue Q0.

## Changes since the Haiku study

| Change | Expected effect | Acceptance check |
|---|---|---|
| `design.yaml` model, prices and USD 15 cap | Only the request `model` field and reservation arithmetic change | Selftest 13/13; price tests derived from design |
| Hub id `sybil-specialists-sonnet` in coordinator, worker and analysis publisher | Separate hub cohort | S0 run appears under the new id only |
| Render title SONNET 4.6 | Label only | Final frame shows the new label |
| Analysis publisher message | No hard-coded Haiku numbers | Reviewed in diff |

## Frozen execution plan

- Command (agentops): `python3 scripts/run-sybil-specialists-sonnet.py <commit> setup`, then `... S0`, `status`, `verify`.
- Host sim-dmarz-4 under the exclusive claim `dmarz-sybil-specialists-sonnet` held by dmarz/orbital-orchestrator. Checkout `/srv/swarm/sybil-specialists-sonnet-lab`, venv `/srv/swarm/sybil-specialists-venv` (existing, shared Python environment only), ledger `/srv/swarm/sybil-specialists-sonnet-budget/ledger.jsonl` (new, never the Haiku ledger).
- One finite worker under `timeout 1900s`; it takes exactly one hub run and refuses re-execution.
- No credentials are sent for S0.

## Visualization mapping

The Haiku study's mapping v1.1 is unchanged ([VISUALIZATION.md](../VISUALIZATION.md)): initial, progress and final 1800×1180 frames and a measured replay GIF, with pending and failed rows shown explicitly. The `verify` action checks hashes, dimensions and frame counts.
