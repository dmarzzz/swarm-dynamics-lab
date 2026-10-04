# Pre-run assessment: local-Q2

2026-10-04 UTC. Parent Q1; read Q0/Q1 post-mortems. Status: ready only after PLAN-v2.md public registration and repair tests. This is the single bounded schema-repair qualification, not a favorable retry. Plan written before implementation.

## Design and assessment

Question: does local1.7B satisfy the existing task once actor-visible output contracts are encoded? Six cases on three new domain roots task7204/seed31, clean/superior, targeted_check; exact truth evaluator. Original task/prompt/decision authority unchanged. Q1 supplies a failure diagnosis, not a paired causal comparator. Accept all six valid, at least five correct and one per domain; then only gated S1. Valid wrong choices finish as an adverse competence result. No holdout access or formal claim.

## Changes and unresolved issues

Candidate count and citation/choice enums plus numeric ranges are added to JSON grammar from actor-visible inputs only. Original semantic validator remains authoritative; duplicate candidates remain detectable. No values supplied by evaluator or fallback. Arithmetic and chair choice may still fail. Required tests: schema rejects disallowed IDs/ranges/cardinality, permits legitimate examples, does not leak numerical answers, truncation/deadline failures preserved. Freeze code/hash before run.

## Execution and visualization

Qwen3:1.7b pinned digest in PLAN-v2; four episode workers,1024 output,8K context,thinking off. At most90 calls/30minutes within cumulative990/60minute budget, zero API spend, local Mac explicitly authorized. No retries; all failures retained. Run python3 local-agents/run_local.py --stage Q2 --out local-agents/results/Q2 --bridge /path/to/private/bridge.py. Public receipt precedes all model calls. Reuse local-influence-v1 bound to these six assignments; save live metrics, all events, final image and logical replay; check recorded states and denominators.
