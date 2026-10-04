# Pre-run assessment: fleet-s1-001

sybil-specialists / dmarz/sybil-specialists / S1 / 2026-10-04 UTC. Parent: fleet-s0-001, whose post-mortem was read. Status: ready. S0 reconciled all 256 outcomes, passed 14 invariant checks, matched local metrics within floating-point rounding and verified live images plus playback.

## Design and assessment

Unchanged README, design.yaml and fleet-scripted-001-pre.md define the question, equal-check comparators, evaluator boundary and metrics. Twelve paired world clusters 200–211 cross two bridge levels, three attacker pass rates and budgets 2/4/8: 18 cells and 864 arm outcomes. Development only; reserved holdout remains inaccessible. Primary contrast is coverage minus degree rare accuracy at bridges 1, attacker pass 0.1, budget 4; report malicious admission alongside it. The fixture cannot establish general Sybil resistance or LLM behavior. An adverse tradeoff is valid and will not cause retuning.

## Changes and unresolved issues

No scientific code, assignments or design changes. The deployment wrapper repairs final-image ordering without changing pixels or records; the S0 acceptance check passed. Scientific limitations from the parent review remain. No unresolved material execution defect.

## Frozen execution plan

Run private agentops scripts/deploy-sybil-specialists.sh with source e3caaf3d77bc46474f2b02145799c5f534adf225 and stage S1. The assessment is committed separately from this frozen execution revision. Design digest b7d0aa0ab82b03c9ec5ae705ec90a990c5e29e98c9fe5aa3859c2efcbecb210d; runtime versions unchanged. Use sim-dmarz-4, reverify merged exclusive claim dmarz-sybil-specialists (expires 07:21:53Z). One worker, maximum 30 minutes, zero model calls and zero API spend. Stop on invalid outcomes, duplicate/missing assignment, source mismatch or artifact failure; preserve every original attempt. Analyze the saved JSONL after full reconciliation, with paired-world descriptive intervals and all parameter-cell tradeoffs.

## Visualization mapping

VISUALIZATION.md v1, first assigned world 200 in each cell, all four arms and steps 0–budget. Eighteen initial/final image pairs and eighteen GIFs (3/5/9 frames) from retained history. Verify final-image priority, metric agreement and supported browser playback. The overview metrics currently show the coverage arm; per-arm comparisons live in the four-panel replay and summary records. No evaluator truth reaches policies. S2 and API stages remain disabled.
