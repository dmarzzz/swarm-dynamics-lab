# Pre-run assessment: fleet-s0-001

- Experiment / owner / stage: sybil-scale-xl / dmarz (operator dmarz/scale-xl) / S0, scripted backend, no model calls.
- Parent attempt: local-s0-001 (offline), interrupted with no rows when orbital-one ran out of memory ([post](local-s0-001-post.md)). This fleet run is therefore the first complete S0; it must record 216/216 valid rows and a passed scripted qualification.
- Status: ready once the plan commit is on main and the claim on sim-dmarz is merged and exclusive.
- Purpose: prove the pinned revision runs on the claimed server, that parallel world preparation fits its 4 vCPU / 8 GB, that hub registration, progress, artifact upload and verification work for this experiment id, and record the runtime source hash that Q0 and S1 must match.

## Design

2 engineering worlds (4900–4901) × 2 attacker pass rates × 7 checkpoints × 2 badge modes, plus 4 qualification worlds × 2 Q0 packets × 2 badge modes, per size N = 972, 2,916, 8,748: 216 scripted rows. Scripted plurality answers every packet; the stage passes only if every row is valid and every size meets the Q0 thresholds on the clean packets.

## Frozen execution plan

- Command: `python3 scripts/run-sybil-scale-xl.py <commit> setup`, then `… S0`, `status`, `publish`, `verify` (agentops).
- Expected time: preparation dominated by the four N=8,748 engineering worlds; minutes on 4 vCPU (pool capped at 4 processes). Record peak memory for S1 sizing; the server has 8 GB.
- Stop rules: any invalid row fails the stage and is preserved; no retries.

## Visualization mapping

Mapping v1: S0 frames labelled SCRIPTED, three-point log-N axis, initial/progress/final frames and a measured-prefix replay. Check that the 8,748 points render and that no pending cell is drawn as zero.
