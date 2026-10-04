# O2 post-mortem: ownership fixes duplication; eight agents add cost on this support

**Decision: complete_valid_result.** The ownership repair passed its predefined gate, and the requested larger-swarm diagnostic completed. All10 assignments reached terminal graded outcomes;9 succeeded, with the intentionally weak legacy comparator the sole task miss. There were272 native calls, zero unsafe commits, zero ownership violations, zero transport/schema/publication failures and zero unstarted assignments. This is the owning agent's scientific assessment, not independent review.

Evidence confidence: **1 / exploratory**, for the narrow descriptive repair and size comparison. One authored endpoint-failover template, one reused four-service qualification instance and one eight-service instance with dependent stable/changing variants;2 qualification +8 demonstration episodes. Neither10 episodes nor272 calls are independent incidents. No optimal-N or production reliability conclusion.

## Baseline repair

[Prospective plan](../outage-prototype/O2-PLAN.md), frozen execution source `cc91c560af8c12eac6b6caaa38f1406306aee863`. Legacy-four repeats the exact O1 world hash, with the same1024-output ceiling as owned-four in O2. Both use four tool slots. The only intended comparison change is explicit deterministic service ownership plus enforcement; this is an interface-assisted baseline, not emergent coordination.

| Four-service qualification | Final repaired | Duplicate patch proposals | Stale writes | First all healthy | Exposure |
|---|---:|---:|---:|---:|---:|
| Legacy-four | 3/4 | 12 | 13 | never | $0.083428 |
| Owned-four | 4/4 | 0 | 2 | tick4 | $0.072716 |

All32 visible legacy responses were reviewed through their exact saved actions. The first divergence is tick1: all four actors inspect svc-405. Tick2 rejects their four stale writes after failover. They repeat the same inspection at tick3; at tick4 one repair commits and three duplicate patches become stale. The team then duplicates work on svc-600 and svc-648; svc-888 remains unrepaired at tick8. Owned-four starts with four different services, repairs unchanged endpoints at tick2, refreshes the changed endpoints, and completes at tick4. No off-owner action was proposed, so the enforcement guard never had to rescue native behavior. This one matched development comparison supports the practical repair; it is not a precise effect estimate across incidents.

## Eight-service comparison

All arms receive eight total tool slots per tick. Single context can batch eight actions; four contexts receive two each; eight contexts receive one each. Model aggregate calls and computation are intentionally unequal and fully charged. Stable and changing variants share one template/instance; fixed order is reversed across variants, not randomized.

| Policy | Stable / changing recovery tick | Stable / changing episode seconds | Calls, both worlds | Exposure, both worlds |
|---|---|---|---:|---:|
| Single context | 2 / 4 | 15.69 / 17.35 | 16 | $0.062884 |
| Owned-four | 2 / 4 | 17.57 / 19.02 | 64 | $0.207135 |
| Owned-eight | 2 / 4 | 19.99 / 19.77 | 128 | $0.397956 |
| Public-state rule controller | 2 / 4 | 0.029 / 0.023 | 0 | $0 |

Every demonstration ends with8/8 healthy services and zero unsafe commits, duplicate patches or ownership violations. All have56/64 healthy service-ticks in stable worlds and48/64 in changing worlds. Eight agents cost6.33× the single context while providing no terminal recovery, service-time or measured episode-latency advantage in these observations. Timings cover the engine/model/tool loop, excluding registration and upload; no repeated latency measurement or confidence interval is available. Simulation ticks are not physical seconds. The controller's zero model charge excludes shared infrastructure and engineering cost.

The single context made four extra stale patches during the changing world's tick3, combining inspections with guessed follow-up versions in the same response. Preconditions rejected them, and the next response used refreshed facts successfully. This is a trace-observed inefficiency, not an unsafe committed state or evidence that the larger team recovered sooner.

## Integrity, qualification and process

[Analysis](../results/outage-o2/analysis.json) recomputes all10 final grades and case hashes. It audits all272 exact serialized requests, ownership/slot fields, request hashes and visible-response-to-decision matches. [Native trace review](../results/outage-o2/trace-review.json) preserves every action, receipt and health state by tick; the qualification miss was reviewed across all eight rounds. [Artifact readback](../results/outage-o2/verification.json) verifies all40 authenticated hub files by SHA-256. Raw synthetic evidence is published here; the live UI's raw-artifact proxy remains separate from authenticated access.

The eight-agent changing replay was inspected at tick1 (eight impaired services) and tick8 (eight healthy services), with accurate label,64 model turns and4 stale writes. Its layout wraps service cards instead of clipping eight across a narrow screen. Animation is saved-state playback.28 outage checks and70 existing shared checks passed before dispatch, including disjoint ownership, off-owner rejection, equal slots, finite272-call contract and reference-world recovery. These checks are software evidence, not additional native trials.

Initial registration readback was temporarily unavailable; subsequent immutable public-plan/API and browser checks passed before any paid call. The native parent exited0 with no stop reason. Offline evidence import/finalization succeeded without model calls; generated handoff SHA-256 `0a26c81d2f82d4fc302a657a0e491e3d372efd895d9cf4b2c7ba8597964fd508`. Its scaffold is supplemented by this review and the [eleven-dimension assessment](../results/outage-o2/scientific-assessment.json).

Approved-account identity, exclusive claimPR398, current source/runtime, public condition TLDRs and original single-writer ledger were verified. No machine was created or ledger migrated. The bounded credential relay kept the provider key local. Workers and relay stopped; private forensic backup verified. Claim releasePR404 merged. Researcher review was not required by owner direction; no independent review is claimed.

## Costs and decision limits

O2 settled cost **USD0.749080**, retained fee uncertainty **USD0.075039**, exposure **USD0.824119**, within itsUSD11 subcap and originalUSD20 cumulative authority. Original ledger:1187 calls, settledUSD3.352858, exposureUSD3.727799, remainingUSD16.272201. Exposure retainsUSD0.220480 historical unknown andUSD0.154461 accumulated fee uncertainties. Existing host reused without a new infrastructure purchase; shared pre-existing host cost is not claimed as measured API spend.

Accept O1's diagnosis: its weak fixed-team coordination confounded the contraction result. Explicit ownership removes the observed duplicate-repair failure. Reject the inference that merely doubling roster size now adds utility: this task remains easy to batch, and every stronger comparator reaches the same outcome at the same action clock. The simplest controller is the practical reference on this declared support.

Park further size escalation. No automatic rerun or extra model probe is justified by this completed diagnostic. A future main experiment would need a concrete residual real-world need—costly parallel evidence acquisition, incomplete/noisy telemetry, genuinely distinct incident mechanisms and a strong single-agent/tool baseline—plus independent cases and a prospective budget/decision rule. Do not make tasks harder merely to manufacture an eight-agent advantage. This result does not establish that large swarms are generally ineffective.
