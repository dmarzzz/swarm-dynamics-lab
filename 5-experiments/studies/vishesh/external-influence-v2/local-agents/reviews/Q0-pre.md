# Pre-run assessment: local-Q0

Experiment: external-influence-v2; owner vishesh/codex-local-agents; exploratory local competence screen. Status: ready only after public registration and offline tests. Parent: historical S0/S1, reviewed in ../../reviews/quality-post.md. Read before implementation; known arithmetic and chair-integration weaknesses intentionally preserved for backend comparison.

## Design and assessment

Question: can 0.6B local agents execute the same task competently? Strongest comparator: exact fixture truth for qualification; archived Haiku decisions only in S1. Six assignments across three domain/task roots, clean and superior paired within each domain. Each uses nine roles and 15 call slots. Complete assignments, not actors, are the scored denominator. Hidden truth is confined to evaluation. No directional quality prediction. Qualification failure is informative about usability, not attack resistance. No confirmatory research claim or untouched holdout access.

## Changes and unresolved issues

Only backend/model changes; original prompts, environment and scoring remain. Native JSON schema supplies shape, never scripted numerical values. Known arithmetic and final-check application failures remain measured. Acceptance: all six valid, at least five correct and at least one correct per domain. Invalid output, truncation and context overflow remain failures rather than silent retries. Local model suitability is unknown.

## Frozen execution plan

See ../PLAN.md for exact assignments, model and settings. Source/config hashes and full checkpoint digest are written to manifest before dispatch. Command: python3 local-agents/run_local.py --stage Q0 --out local-agents/results/Q0. Maximum 90 calls, 30 minutes, four episode workers, zero API spend. The owner explicitly requested this local Mac; fleet-machine requirement is overridden only for this local variant. No credentials enter inference. Reporting uses the established credential-consuming bridge with allowlisted output. Offline regression tests must pass and the public receipt must precede inference. Failure advances only to declared Q1 qualification or bounded diagnostic, never unrestricted S1.

## Visualization mapping

Use local-influence-v1 from ../PLAN.md, bound to Q0/task7200/seed23 and its six conditions. Calls and phases update live progress, events retain order/timestamps, final SVG and HTML replay show pending/invalid/correct states. Logical order is labeled and evaluator truth never enters prompts. Validate replay count and initial/middle/final/failure frames against journals. Public metrics are the fallback if the hub cannot embed richer files.

Offline acceptance completed before inference: 6 local adapter/gate/replay tests and 11 unchanged parent protocol tests passed. All six scripted qualification fixtures are valid/correct. protocol.py, environment.py, common.py and provider.py byte-match historical model-source commit b107b1636c852b946ecf7e7e7383cec8810d0eda. Public browser inspection verified the new TLDR and immutable parent README link on Swarm Live. Local source provenance and preflight are enforced by the runner.
