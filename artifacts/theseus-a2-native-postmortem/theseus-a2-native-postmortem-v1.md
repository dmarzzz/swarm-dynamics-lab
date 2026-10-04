# A2 acquisition: valid negative result

A2 completed on the owner-approved OpenRouter route with 196 terminal calls, no provider errors and no retries. The withheld-policy acquisition gate failed: **6 of 12 policies qualified**. This is a six-fixed-root acquisition diagnostic, not evidence about swarm culture or turnover.

| Endpoint | Learned policy | True-policy ceiling |
|---|---:|---:|
| Assigned executor actions | 96 | 96 |
| Observed actions | 88 | 96 |
| Correct actions | 67 | 96 |
| Observed accuracy | 76.14% | 100% |
| Correct / assigned | 69.79% | 100% |
| False releases | 3 | 0 |
| False incident activations | 5 | 0 |
| Useful releases | 7 / 12 | 12 / 12 |

One learner returned an invalid same-source mapping, leaving eight dependent actions unstarted. Those are missing outcomes, not measured mistakes. Five other learners returned valid but incorrect mappings. All six failed policies contradict visible training evidence; the same histories uniquely identify the correct sources. The exact enumerator therefore supplies a strong simple acquisition baseline on these cases.

## What the traces establish

The owning agent reviewed all twelve learner outputs, the full visible histories for all six qualification misses, and all 21 incorrect executor outputs. Automated replay checked all 196 request/response pairs, provider translation and request hashes, scoring and cost. There were zero audit disagreements. **All 21 wrong actions agree with the supplied wrong learned policy.** No additional execution error was observed. We cannot infer hidden reasoning or why the model selected those sources.

This changes the useful next question: how should evidence authorize promotion of a learned policy into inherited memory? More polishing of this execution benchmark is unlikely to help. Faithful execution can propagate a wrong inference. A retrospective semantic gate would reject all six failed policies; that observation does not measure the service lost by a deployed abstention mechanism or prove a preservation benefit.

## Design critique and next decision

The oracle ceiling isolates execution capability, but has privileged knowledge and is not a fair practical comparator. The prospective [selective-preservation design](SELECTIVE-PRESERVATION.md) defines retain, revise, quarantine and provisional states, supporting and contradicting evidence, scoped updates, and an equal-information, equal-budget single-controller comparator. Its stable, changed-rule and conflicting-evidence cases remain development fixtures, not native results.

Before any preservation study, compare that evidence process with exact consistency checking where the rule space is enumerable. A worthwhile extension needs evidence that is incomplete or legitimately changes, useful work measured alongside false actions and abstentions, and an operational reason that the simple method is insufficient. Use separate held-out cases after offline development. Do not weaken the failed capability gate or rerun to seek a favorable result.

**FINISH / PARK this acquisition qualification lane.** No turnover run or A3 is launched. A material successor requires a concrete prospective plan and the corresponding owner decision. The existing approved A2 attempt is complete.

## Scope, process and costs

The independent design units are six fixed synthetic roots, with twelve nested learners and paired case/family actions. These counts support engineering diagnosis, not a precise population effect or novelty claim. The same intended Haiku 4.5 model was served via OpenRouter/Anthropic; the dated backend snapshot was not independently established. Do not pool this cohort with older direct-provider runs. Successful OpenRouter inference does not establish direct-Anthropic recovery.

The immutable A2 plan and route amendment were published and the public page verified before the first assigned call. Source was `b5484ca0d9c7f199bf70c5412dcd5d363a8aefd7`; 36 offline checks passed before dispatch. The first assigned learner also served as route qualification within the original 204-call envelope. Researcher review was not required by owner direction; this audit is not independent validation.

New measured model cost: **USD 0.156627**. Original cumulative lineage: USD 0.8122310437 estimated prior spend + USD 0.010452 unresolved A1 exposure + this A2 cost = **USD 0.9793100437 / USD 5**. No incremental infrastructure purchase. Unused A2 hold USD 2.443373 is released; remaining unallocated budget USD 4.0206899563 is not new-run authority. The original allocation and failed A1 records remain intact.

[Native summary](results/A2/summary.json), [trace audit](results/A2/TRACE-REVIEW.md), [structured scientific assessment](results/A2/scientific-post-mortem.json), [figure](results/A2/results.png), [completion-order replay](results/A2/replay.html).
