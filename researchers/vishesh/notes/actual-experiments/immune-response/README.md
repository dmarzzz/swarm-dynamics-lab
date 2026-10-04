# Immune response: separate restoration from stale-record rejection

## TLDR

After a bad record contaminates a swarm, is repairing private memories enough, or must the shared store also be repaired? Compare Q11 with Q10F, holding private repair and stale-record blocking fixed. Eight actors face returning stale data and a later genuine update; measure correct mock-deployment, recovery and relapse. Oracle incident labels make this a repair-mechanism test, not autonomous detection.

Exploratory v2 instrument, not a confirmed LLM finding. [Frozen protocol](preregistration.md), [assignments](design.yaml), [instrument](../src/immune_v2.py). Historical [v1 protocol](preregistration-v1.md) and runs remain separate.

The primary comparison is Q11 minus Q10F: both restore affected private state and block known stale records; only Q11 restores the shared store. Q10, Q10F, Q11R and Q11 form a two-by-two mechanism comparison. N, Q00, Q01 and CLEAN provide diagnostic baselines. A no-incident stratum measures unnecessary intervention. All actions concern fictional deployment plans, with deterministic truth and scoring.

Eight actors execute 24 rounds. A bounded incident precedes a paired checkpoint fork; a stale descendant returns at round 13, and a genuine update arrives at 18. Useful completion now requires a correct plan and an authorized mock-deploy action. Persistent failure and relapse after recovery are reported separately. The controller still has oracle labels; this does not test autonomous detection, real operational safety or collateral loss from novel benign learning.

## Question and prediction

Does shared-store restoration reduce persistent failure and relapse when private repair and stale-record blocking are already applied? The primary contrast is Q11 minus Q10F; it does not test autonomous detection.

## Setup

Eight actors maintain fictional deployment plans for 24 rounds. The controller supplies known incident labels and scores correct plans plus authorized mock deployments.

## Protocol

Fork paired conditions around an incident. Cross shared restoration with stale-record blocking while holding private repair fixed; compare diagnostic baselines and a no-incident stratum. A stale descendant returns at round 13 and a genuine update at 18. Historical v1 runs use the linked v1 protocol, not this revised contrast.

## Metrics

Measure useful correct completion, persistent failure, time to recovery, relapse and unnecessary intervention. Report backend, invalid outcomes and compute; scripted qualification does not establish an LLM repair benefit.

## Assessment and follow-up

The v2 native run `4deeb0f2` completed with eight outcomes and one response-contract failure in Q10F. [Full assessment](../../immune-response-v3/REVIEW.md) preserves the failure and explains why the single native task does not establish population robustness. [V3](../../immune-response-v3/README.md) adds strict agent contracts, no-replay/missing-lineage/benign-learning controls, selective repair, and recorded-data visualizations. Its 720-outcome engineering qualification passed; fresh native repair qualification awaits a dedicated machine.
