# Immune response: separate restoration from stale-record rejection

Exploratory v2 instrument, not a confirmed LLM finding. [Frozen protocol](preregistration.md), [assignments](design.yaml), [instrument](../src/immune_v2.py). Historical [v1 protocol](preregistration-v1.md) and runs remain separate.

The primary comparison is Q11 minus Q10F: both restore affected private state and block known stale records; only Q11 restores the shared store. Q10, Q10F, Q11R and Q11 form a two-by-two mechanism comparison. N, Q00, Q01 and CLEAN provide diagnostic baselines. A no-incident stratum measures unnecessary intervention. All actions concern fictional deployment plans, with deterministic truth and scoring.

Eight actors execute 24 rounds. A bounded incident precedes a paired checkpoint fork; a stale descendant returns at round 13, and a genuine update arrives at 18. Useful completion now requires a correct plan and an authorized mock-deploy action. Persistent failure and relapse after recovery are reported separately. The controller still has oracle labels; this does not test autonomous detection, real operational safety or collateral loss from novel benign learning.
