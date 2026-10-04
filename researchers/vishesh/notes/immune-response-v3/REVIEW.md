# Immune-response assessment and repair ledger

Assessment of repository revision 951142a and preserved native v2 run `immune-response/4deeb0f2`, 2026-10-04 UTC. This is an owner-side engineering/design review, not independent hypothesis acceptance. All changes are prospective in v3; v1/v2 evidence remains unchanged.

## Overall finding

V2 is a useful oracle-controlled repair instrument, but not yet compelling evidence for autonomous swarm immunity. Its strongest feature is the branch-paired factorial comparison separating shared restoration from replay blocking. Its weaknesses are narrow fixture variation, a single native task, an invalid primary-control outcome, no visual artifacts, incomplete actor specifications, and ambiguous recovery when the clean reference fails. V3 repairs the instrument and exposes adverse boundary cases rather than tuning until every treatment looks successful.

| Review dimension | Evidence and issue | V3 response / acceptance |
|---|---|---|
| Design quality | Private repair is fixed in the primary Q11–Q10F contrast; v2 separates restoration and blocking. Controller still uses oracle labels. | Retain factorial controls and explicit oracle boundary; add selective repair Q11S to test collateral loss. |
| Measurement | Correct authorized deployment is well defined. Python booleans could satisfy integer equality; extra compatibility fields were tolerated. Relative recovery could be reported against a failing clean reference. | Strict integer/exact-key scoring; require four successful, error-free rounds in both branch and CLEAN for recovery. Retain all assigned outcomes and validity separately. |
| Visualization | Native v2 retained useful trajectories but shipped no frames/animation. State hashes alone cannot show private/shared contents. | Trace-backed PNG/GIF and interactive replay for historical outcomes; v3 adds per-round correct/wrong/missing counts. No fabricated historical states. |
| Specification | Timing and limitations are clear; the exact response schema and state-transition contract were scattered in code. | Versioned agent contract, explicit information boundary, response schema, memory behavior, source/checkpoint hashes and reproduction commands. |
| Plan quality | V2 was frozen before execution, but one task cannot measure population robustness. | Disjoint development/engineering/native/holdout IDs; bounded local robustness suite, then a small fresh native repair qualification with explicit gates. |
| Control evidence | Scripted incident strata all had identical results; target was always requested. | Variable target relevance/ownership, no-incident and no-replay controls, missing-lineage stress and benign-learning rollback stress. Distinguish task failure from execution failure. |
| Agent reproducibility | Pinned Haiku, temperature zero, immutable records, isolated stores. Replicate seed only randomized arm order; no provider seed. | Keep that limitation explicit; test deterministic scripted replay, hash prompt/schema/config/code. Keyed record choices make duplicate-key endorsement unrepresentable in the schema. |
| Scenario validity | A fictional version ledger gives objective truth but is not a general dependency solver or production incident. | Keep scenario claims bounded; measure transfer only after qualification. Do not present synthetic registry values as realistic operational validation. |
| Reliability / infrastructure | All 1,137 v2 API calls returned. One specialist response endorsed two versions of one key, causing one invalid outcome. Generic hub completion did not distinguish qualification success. | Typed choices, malformed-output regression, explicit execution/clean qualification metrics, durable round telemetry and visible failures. Dedicated machine required for a new model run. |

## Native v2 outcome review

Eight assigned and recorded outcomes; one invalid (Q10F). API failures: zero. Actual model usage cost: USD 1.98713, 1,137 calls, 1,616.676 seconds. Usage was reported for every call. The failure occurred at Q10F round 19, specialist A6: six endorsed record IDs were all supplied, but two referred to different versions of `version:service-3`. It was a response-contract error, not an invented ID, transport outage or evidence that the scenario itself was impossible.

| Arm | Useful completion (18 recovery requests) | Valid | Interpretation |
|---|---:|---|---|
| CLEAN | 18/18 | yes | Basic task competence in this task |
| Q01 | 18/18 | yes | Shared-only repair worked here; private restoration necessity is not established |
| Q11R | 13/18 | yes | Recovered, then relapsed after stale replay |
| Q11 | 18/18 | yes | Combined restoration and blocking worked in this task |
| N | 7/18 | yes | Persistent error until the later genuine update |
| Q00 | 7/18 | yes | Containment alone did not remove resident corruption |
| Q10F | 7/18 | no | Primary control had one specialist contract failure |
| Q10 | 7/18 | yes | Private-only repair did not remove resident corruption |

The primary all-assigned Q11–Q10F difference is 11/18 (+61.1 percentage points). Its complete-valid-pair count is zero. Do not turn this into a confirmed model effect or compute a population confidence interval. V2's native Q01 success differs from the scripted prediction: scripted behavior cannot stand in for LLM behavior. A new run cannot retroactively make the old invalid pair valid.

## Failure and repair ledger

| ID | Evidence / cause confidence | Repair | Verification and status |
|---|---|---|---|
| F1 | Observed duplicate fact key in one validly parsed model response; verified | One nullable record-ID enum per fact key; validate before mutating memory | Offline contract and state-atomicity tests pass; fresh native qualification required |
| F2 | Boolean/int equality and non-exact constraint-key acceptance; code review | Strict integer types and exact keys | Scorer regression tests |
| F3 | Recovery relative to a failing CLEAN could look successful; code review | Error-free clean and treatment four-round gate | Forced failure test leaves recovery censored |
| F4 | Identical scripted incident outcomes and fixed target relevance | Five distinct scenarios and varying target slots/ownership | Prospective 16-task engineering suite; report range, not just mean |
| F5 | No visual outputs; incomplete historic state telemetry | Build replay from existing trace; add state counts prospectively | Inspect timeline, event alignment, final summary and GIF playback; label unavailable historical state |
| F6 | Hub “done” can be mistaken for qualification passed | Publish execution_qualified and clean_qualified independently; keep invalid counts | Runner/analyzer tests and explicit post-mortem |
| F7 | Fleet availability changed during allocation | Atomic exclusive-claim checks correctly rejected collisions | No conflicting host used; wait for a dedicated allocation |

## Remaining evidence limits

No autonomous incident detection, calibrated suspicion, appeals, noisy or false-positive detector, adaptive attacker, tools outside the mock ledger, actual service deployment, larger swarm scaling, or independent replication is demonstrated. Correct-minority retention is only a limited sentinel check. The benign-learning control measures one specific rollback loss, not every collateral cost. Live provider nondeterminism and service drift remain even at temperature zero. A reliable implementation can still produce valid negative results; “no failures” is an engineering target, not a promise of favorable scientific outcomes.
