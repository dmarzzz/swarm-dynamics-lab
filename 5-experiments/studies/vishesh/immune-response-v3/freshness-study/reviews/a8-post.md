# Immune Response — A8 native qualification

Retrospective owning-agent assessment,2026-10-04. [Run](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-200352-e49401). Frozen runtime `9bf9815aae5fc6ed65e1f6a9ecfdc4763ed03698`; [prospective plan](../QUALIFICATION-A8.md), [reconciliation](a8-reconciliation.json), [rubric](a8-quality.json), [native frame](a8-final.png), [animation](a8-replay.gif).

## Outcome

**Execution and hosted action-ID interface passed; native capability failed.** All18requests returned complete usable responses and usage; all6episodes and12simulator actions completed. No400, invalid action, retry, missing response or silent decoding repair. Raw action IDs decode exactly to retained simulator actions, and all states/scores replay. Only1of6prespecified capability gates passed. This is a valid adverse qualification result, not another infrastructure failure.

| Case | Raw healthy ticks /2 | Checked healthy ticks /2 | Capability |
|---|---:|---:|---|
| Healthy current evidence | 2 | 0 | Raw passes; checked damages healthy service |
| Fresh worker crash | 0 | 0 | Neither arm restarts worker |
| Stale false alarm | 0 | 1 | Both arms eventually damage healthy service |

Across12action ticks,3were healthy; no useful restart occurred. Three of four initially healthy episodes lost health. These are descriptive counts over three familiar constructed worlds, not independent12-sample or population estimates. A8 has a new response contract and is not pooled with A5/A6 to estimate a treatment effect.

## Full native trace review

All six advisor answers and twelve controller answers were inspected against their exact visible requests and subsequent simulator outcomes. Every advisor made a verifiable catalog error. In healthy and crash cases, both advisors recommended gateway1 despite gateway2/worker2 sharing rpc-batch; the suggestion also removed required bulk_checkout. In the stale-alarm case, both advisors misrepresented worker2 as unable to read legacy data although the catalog explicitly lists both schemas. The configuration advisor incorrectly described worker1 as compatible with the gateway2 RPC requirement. The runtime advisor treated stale worker-down evidence as current.

Healthy/raw inspected and refreshed while preserving health. Its second explanation falsely suggested refresh avoided a tick cost and preserved a future action, despite being the final tick; all actions consume a tick. Healthy/checked immediately downgraded gateway1, repeating an invented configuration incompatibility, then inspected the damage. The freshness labels therefore did not guarantee correct factual interpretation.

Fresh-crash/checked inspected then refreshed, leaving the failed worker down. Fresh-crash/raw incorrectly called current epoch7 evidence stale, inspected, then downgraded the healthy gateway instead of restarting the failed worker. Both had an available same-version worker2 restart and fresh liveness evidence; the reference controller passes the unchanged gate. More allotted time might alter behavior but would be a different protocol, not a retrospective rescue.

Stale-alarm/raw immediately downgraded worker1 based on obsolete liveness and incorrect schema claims, then inspected. Checked first refreshed the stale probe correctly and observed all checks true, but its second action still downgraded worker1 and claimed it was down. This is evidence that refreshing metadata alone is insufficient when the decision ignores refreshed content. The controller explanations often repeat advisor errors, but shared model/context may produce the same errors independently: these traces do not causally isolate harmful advice.

All twelve structured actions match the action expressed in their visible justification at the action-type level; no explicit prose-versus-action reversal like A5 was observed. That narrow consistency does not validate the factual claims. Invalid-response count is0 while wrong or ineffective decisions remain substantive outcomes.

## Instrument, evidence and costs

The repaired two-field enum contract is now natively accepted for all12controller requests on the declared Anthropic-only OpenRouter route. Six advisor requests retain their prior contract.34offline/remote tests preceded dispatch. Strict decoding preserves the same ten legal choices; no simulator rule, success threshold or scientific outcome was changed to accommodate answers.

All18request/response/usage hashes reconcile; raw responses, decoded actions, original observations and complete trajectories are retained locally. Nine compressed hub artifacts were fetched and SHA256-matched; full transport remains local and is not misrepresented as public raw evidence. Native frame/GIF reflect the six recorded trajectories with three time frames, color-separated arms and action markers; no scripted trajectory is substituted. Interactive replay is uploaded with the run. Two-tick animation illustrates this deliberately short qualification, not long-run resilience.

Known actual new API costUSD0.030345; new reservationsUSD0.140146. Original ledger429calls/USD3.492196reserved ofUSD8; historical uncertain usage remains preserved. No extra budget or new machine. Existing shared-machine allocated cost is not separately measured. The exclusive researcher allocation was released after workers stopped, relay exited on18requests and the exact tunnel closed. Offline finalize completed with execution outcome completed; its zero model_calls describes finalization only. Capability status remains failed and this authored review supplies the scientific assessment.

## Decision

Do not advance to the larger freshness comparison. The infrastructure/schema defect is repaired for this observed cohort; the advisory/controller architecture cannot yet demonstrate the required simple repair and restraint. Preserve this negative result. Do not add agents, raise budget, weaken gates or silently give a longer horizon to obtain a pass.

The next useful offline design work should isolate factual evidence interpretation from advisory influence: explicit compatibility/liveness checks derived from visible fields, a controller-only comparator under the same decision budget, and a prospective test of whether correct evidence can override incorrect advice. Evaluate whether a deterministic verifier should reject factual claims rather than letting free-form advice masquerade as validated evidence. Such changes alter the scientific/execution contract and need a concrete prospective plan before any new native attempt. This diagnostic supports investigating those mechanisms; it does not prove advice causality or a general disadvantage of freshness annotations.
