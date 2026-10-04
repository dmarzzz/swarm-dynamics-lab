# Pre-run assessment: fleet-s0-001

- Experiment / owner / stage: sybil-scale-sonnet / dmarz (operator dmarz/scale-sonnet) / S0 fleet, scripted backend.
- Parent attempt and previous post-mortem: [local-s0-001-post.md](local-s0-001-post.md), read. The Haiku study's [fleet-s0-001-post](../../sybil-scale-api/reviews/fleet-s0-001-post.md) is the engineering precedent.
- Status: ready, conditional on the exclusive claim and the exact pinned revision.
- Question: does the copied runtime execute end to end on a dedicated host, register under the new hub id, upload all artifacts and pass scripted qualification at all four sizes, so that Q0 and S1 can be pinned to the same runtime?
- Uninformative if: the host is shared, the revision differs from the committed plan, or uploads are not acknowledged.

## Design and assessment

Identical design to the Haiku study (see [README](../README.md)): 264 scripted rows (64 clean qualification fixtures 5000–5003 + engineering worlds 4900–4901 across all arms, sizes, budgets, attacker pass rates and badge modes), zero model calls. Units are worlds; no S1 world (6000–6023) or holdout (10000–19999) is opened by S0. Graph truth and ownership never enter actor packets; the blind-packet and principal-blind selftests cover this.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| New hub id, ledger cap, model label | Copied runtime with id/model/price/cap edits only | Same scripted outcomes as Haiku S0 | 264/264 valid; per-size qualification 1.0; same counts as local-s0-001 | dmarz/scale-sonnet |
| New host and paths | Separate checkout/venv/ledger under /srv/swarm/sybil-scale-sonnet-* | No interference with any other study | Claim verified exclusive; no other worker on host | dmarz/scale-sonnet |

## Frozen execution plan

- Runtime: source hash computed by the worker at the pinned public commit (expected to equal the local hash `a1a619f7…` if no study file changes before the commit); Python 3.12 venv with pinned requirements.
- Command: `python3 scripts/run-sybil-scale-sonnet.py <commit> setup`, then `… S0`, then `status`, `publish`, `verify` (agentops, private launcher).
- Max calls 0; wall time ≤ 4 h stage timeout; one scripted worker; no retries; failures stop dispatch and preserve not-started rows.
- Server: sim-dmarz-3 under exclusive claim `dmarz-sybil-scale-sonnet`; no credentials needed for S0.
- If it fails: post-mortem, repair under a new attempt id; no Q0 until a fleet S0 passes at the runtime Q0 uses.

## Visualization mapping

[Mapping v1](../VISUALIZATION.md), bound to `sybil-scale-sonnet/<run>` with stage/batch/source_hash/code params. Initial, progress and final 1800×1200 PNGs, hidden-badge image, ≤33-frame measured-prefix replay GIF, raw assignments/episodes/worlds. S0 frames are labelled SCRIPTED. Verified with the launcher's `verify` action (artifact hashes, dimensions, frame decode, evaluator and analysis recomputation).
