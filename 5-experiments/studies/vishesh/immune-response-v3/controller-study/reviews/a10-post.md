# Immune Response — stronger models repaired crashes but did not qualify

Retrospective owning-agent assessment, 2026-10-04. [Native run](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-203731-007831), [immutable prospective plan](https://github.com/dmarzzz/swarm-lab/blob/79a6907e3903c6afbfaeba4acabb5377976bc861/researchers/vishesh/notes/immune-response-v3/controller-study/PLAN.md), [reconciliation](a10-reconciliation.json), [quality review](a10-quality.json), [measured animation](a10-replay.gif).

## What we learned

Both Sonnet 4.6 and Opus 4.6 restarted the genuinely crashed worker without changing its binary. This improves on A9's observed failure to perform any useful restart, but the model, prompts, architecture and fixtures changed together; it does not isolate the effect of model strength. Neither controller passed the fixed development qualification. Sonnet failed the necessary configuration repair; Opus unnecessarily intervened on an already-healthy service with stale alarming telemetry.

| Model | Service-outcome gates | Full diagnosis + outcome gates | Fully correct diagnoses | Useful crash restarts |
|---|---:|---:|---:|---:|
| Sonnet 4.6 | 3 / 4 roots | 1 / 4 roots | 4 / 8 ticks | 1 |
| Opus 4.6 | 3 / 4 roots | 2 / 4 roots | 5 / 8 ticks | 1 |

All 32 calls returned schema-valid responses with complete usage. Eight development trajectories completed. The 20 other conditionally enumerated assignments remained unopened: both four-case holdout packets and twelve Sonnet controlled-advice trajectories. They are neither failures nor observed successes. Development roots are shared across models; these are four authored roots, not eight independent worlds or 32 independent samples. Do not advance to the larger swarm comparison.

## Trace-based diagnosis

Every effective request, returned categorical diagnosis, selected action and visible explanation was reviewed. All 16 state transitions and all 32 request/response/usage records replayed exactly from saved evidence.

Sonnet preserved the ordinary healthy service by waiting. In the crash case it selected the correct same-version worker deployment, restored health, then inspected. On the stale false alarm it inspected and then waited. Its uncertainty labels were sometimes `none` when the scorer required `unknown`, despite its action explanation recognizing the stale probe.

The configuration case is an unambiguous action failure. Sonnet selected a gateway downgrade. Its explanation noticed that this would remove the required feature and concluded that it should instead upgrade the worker. The engine correctly executed the gateway action actually returned. The second action changed the worker for a gateway version no longer deployed, leaving the service unhealthy. Both ticks were unhealthy.

Opus preserved the ordinary healthy case and repaired both the worker crash and the genuine configuration mismatch. After the crash, however, it selected registry refresh while its explanation concluded that runtime inspection was needed. The service-outcome gate still passed because the prior restart succeeded; this contradiction separately blocks broad readiness.

On the stale false alarm, Opus incorrectly diagnosed a storage-format mismatch even though the visible formats matched. It selected a store deployment, then explicitly acknowledged in its explanation that its selection was wrong and named a worker restart instead. The existing simulator persistent-format gate rejected the store action. It then restarted the healthy worker based on stale liveness. Health stayed green for both ticks, but **that is not successful preservation**: it attempted an unnecessary configuration change, received a rejection, unnecessarily restarted a healthy process, and never refreshed the stale probe. The existing simulator rejection is not a new controller safety mechanism or evidence of correct judgment.

There are at least three clear selected-action/explanation contradictions: Sonnet configuration tick 1, Opus crash tick 2 and Opus stale-alarm tick 1. All 16 action responses serialized `action_id` before `reason`. A later explanation cannot revise an earlier emitted action field. Ordering is therefore a plausible contributor worth testing, not a verified causal explanation.

## What the instrument itself needs

The diagnosis scorer interpreted `failed_service` exclusively as a currently observed non-live process. The prompt did not fully define that convention for configuration faults, so naming the incompatible component was penalized. Likewise, `fault=none` versus `unknown` needed explicit priority rules. Preserve the original exact-match scores, but do not interpret every such miss as proven inability to diagnose. This ambiguity does not explain away Sonnet's failed repair or Opus's unnecessary interventions.

The [prepared contract candidate](../next-contract/PLAN.md) makes those existing conventions explicit and proposes a paired action-first versus brief-justification-first comparison. It retains the same legal actions, observations and fixed service thresholds; no gold correction or new action filter is added. Both arms would share the clearer definitions. The offline candidate and two tests are prepared; no successor has launched. A model upgrade alone is not the demonstrated fix.

Controlled advice is implemented but untested natively because the prerequisite failed. The sealed holdouts remain unused and uninspected. Their common generator ancestry is disclosed; they are not independently authored real-world tasks. AI Village informed visibility, evidence linkage and correction discipline, not repair labels or demonstrated external competence. No raw Village text entered this experiment.

## Reporting, reproducibility and cost

Collection revision: `79a6907e3903c6afbfaeba4acabb5377976bc861`. Actual served model/provider receipts match Sonnet 4.6 and Opus 4.6 via Anthropic, without fallback. Two stateless requests per tick separate diagnosis from action; the action call receives the uncorrected model diagnosis. Seven new and 41 prior offline tests passed locally and remotely before admission. The original ledger hash and exclusive approved-account allocation were verified; immutable public registration preceded dispatch.

A post-collection renderer import collision selected an older study's renderer and caused worker exit 1 after successful collection. This was a reporting failure, not an invalid native cohort. The explicit renderer import and two reporting tests were repaired at `fc512b179d60d3ec821784efac7441ce84e62c49`; nine controller tests then passed. Saved-data repair made zero model calls. Corrected native figures, animation and interactive replay were uploaded to the same run. Nine indexed hub artifacts were retrieved and hash-matched. The original collection bundle remains preserved separately from repaired reporting.

New actual model charge: **USD0.267692**. New conservative reservations: **USD1.111111**. Cumulative ledger: **485 calls, USD4.812055 reserved of the original USD8**, including historical uncertainty; USD3.187945 remains unreserved. Actual charges and reservations are not interchangeable. No new machine was purchased; separate allocated shared-infrastructure cost is not measured here.

Workers stopped; the local relay and exact SSH tunnel were closed. Evidence, both original and corrected reports, and the unchanged-lineage ledger were backed up. Claim 421 was released through private operations PR 430. Operational finalization and this authored eleven-dimension assessment keep successful native collection, failed qualification, repaired reporting and accounting separate.

## Decision

**HOLD the larger experiment.** The useful gain is a controller that can perform basic runtime repair in these cases; reliable preservation and consistent action selection remain unqualified. The next discriminating test should examine the controller contract, not add more agents or repeat until a favorable result appears. A proposed bounded successor is documented, with unchanged thresholds and a cumulative-budget envelope; it needs its own approved execution contract and current admission before any collection.
