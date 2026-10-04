# R1-01: larger robustness screen — did not pass

**FINISH the stopped attempt; HOLD native expansion.** R1 passed all ten qualification calls, then stopped after 25 of 40 evaluation calls: 24 valid, one unknown/value contract failure, 15 unstarted. All 24 scored decisions were correct, but one concealed a source-value error; 23/24 scored packets were fully exact. New API cost USD0.458142. The larger test did not establish robustness; original failures and missing cases remain intact.

[Immutable prospective plan](https://github.com/dmarzzz/swarm-lab/blob/29bddcb26f8d8dcb6ec7870db989b24b372459a2/researchers/vishesh/notes/decision-models/quorum-of-mirrors/packet-study/robustness-v1/PLAN.md), [native summary](../results/QM-R1-01/summary.json), [all-assignment replay](../results/QM-R1-01/traces.html), [audit](../results/QM-R1-01/audit.json), [cost and retained uncertainty](../results/QM-R1-01/closeout.json).

## What it tested and why it is useful

Can the model extract what a report claims separately from what its source establishes, despite corrections, irrelevant times/entities, decimal unit conversions, plans and uncertainty? Each scenario was presented with one and three copies of its changed-value report. The source evidence was held fixed. After extraction, ordinary code compares facts and counts independent sources.

The practical result is that correct final decisions do not establish faithful extraction: normalized values also need checking against their evidence. Report agreement is not extra evidence. This run tests whether repetition disrupts extraction; deterministic source counting itself is immune by construction. It does not establish that committees or debate improve decisions. For the exact controlled grammar, the simple parser solves every case without a model, so prefer that parser when the input contract permits it.

## Results against the frozen criteria

| Measure | Qualification | Evaluation |
|---|---:|---:|
| Assigned / started / valid | 10 / 10 / 10 | 40 / 25 / 24 |
| Exact completed pairs | 5/5 | 8/9 completed (20 assigned) |
| Correct decisions among valid responses | 10/10 | 24/24 (40 assigned) |
| Correct source facts among valid responses | 30/30 | 71/72 |
| Correct report facts including mode, valid responses | 70/70 | 170/170 |
| Exact classification vectors among valid responses | 10/10 | 24/24 |
| Grounded quote checks among valid responses | 10/10 | 23/24 |
| Paired common-report invariance | 5/5 | 9/9 complete (20 assigned) |
| Unstarted | 0 | 15 |

The evaluation acceptance rule was at least 19/20 exact roots, at least 39/40 decisions, no false support for NOT_ESTABLISHED claims and no false contradiction of supported claims. It was not established because evaluation stopped early. Eight roots were exact on both variants, one complete pair had a source-fact error, and eleven pairs were incomplete or invalid. The 15 unstarted calls are neither correct nor observed failures. Qualification was not pooled into evaluation. Paired outcome changes, complete confusion counts and all failures are in the summary and audit. Stop reason: local `ValueError` enforcing unknown-status/null-value consistency, reproduced from saved output. No HTTP error occurred. No retry or provider fallback.

## Observed failures and offline repair

- **QM-R1-01-032:** source s1 says and is quoted as “was operating,” but the model emits running=0. The correct value is1. Source s0 and s2 are stopped, so the final ZERO remains correct and report classifications are unaffected. The component/grounded-quote check catches what decision accuracy would miss. The one-copy partner was exact; one differing pair cannot establish a causal repetition effect.
- **QM-R1-01-034:** the model correctly marks a plan-only source unknown but emits value0 instead of null. Its JSON is syntactically valid and matches the provider field schema, but violates the local cross-field contract. The fail-closed rule stopped dispatch; the charge and full response were retained. This was not HTTP400 or an accounting failure.
- **Saved-data replay:** runtime summarized pairs by iterating an unordered set. With a nonzero delta, array order differed across processes. The offline analyzer now checks delta multisets and reconstructs root-keyed pairs. Original runtime and summary remain unchanged; future runtime should sort root IDs.

A [prospective offline repair note](../packet-study/r1-repair/PLAN.md) preceded a controlled-grammar guard. It independently parses actor-visible text and rejects mismatched facts, inconsistent unknown values and mismatched quotes without using gold or rewriting outputs. It catches both observed failures and accepts the other33 saved responses. Three regression tests pass. This is retrospective software validation; no repaired native run was launched and neither failure is relabeled a pass. The perfect grammar parser remains the simpler alternative where its input contract applies.

## Traces, controls and interpretation

All 50 assignments are represented, including 15 unstarted; actual requests are hash-checked against the frozen manifest and every valid response is rescored from saved content. The owning operator manually inspected all ten qualification input/output traces before signing the source- and receipt-bound evaluation admission. Evaluation manual coverage is seven actual responses: available variants of the first lexicographic root per family plus both failures; selected but unstarted cases have no trace to inspect; [coverage record](../results/QM-R1-01/manual-trace-coverage.json). Full automated replay covers the entire cohort. These are visible response traces, not hidden chain-of-thought.

Five authored families and twenty evaluation roots are the relevant breadth; 280 report occurrences are not independent events. Half the evaluation roots intentionally lack the decisive observation. HEDGE/PLAN values remain represented without being promoted to observations. Copy treatment also changes length and report order; it cannot isolate a pure copy-identity effect. A grammar parser agrees with typed construction labels on the sealed cohort. Same-author generator/parser/evaluator agreement is useful validation, not independent annotation.

No field generalization follows. Even 20/20 IID successes would have a two-sided exact 95% lower bound of about 0.832; these authored roots share only five mechanisms and do not meet the population sampling premise. A perfect result here would identify the next measurement boundary, not justify thousands more aliases of the same grammar.

## Plan clarifications and remaining gaps

The frozen plan overstates that IDs, times and values are all disjoint across splits: fresh split seeds/root IDs were used, but Boolean values, source control values, grammar and potentially times recur. The claim is new authored instances, not semantic holdout novelty. Qualification covered ONE and DEFER rather than all three final outcomes; earlier PQ-04 covered ZERO and the frozen evaluation explicitly balances direction and missing evidence within each family. These limitations are retained, not retrospectively rewritten.

The initial 1,000 software stress packets came from one seed, whereas the plan said across seeds. A separate 1,000-packet/ten-seed consistency check passed after qualification, without changing native inputs/runtime. It is supplemental software validation, not prospective native evidence. The original plan and source remain immutable. No independent research sign-off was required; no such review is claimed.

## Costs, process and resource closeout

New API charge: USD0.458142; maximum new reservation USD2.40. Owner added USD5, yielding cumulative USD8 API + USD1 infrastructure. Cumulative known API charges: USD0.93200496; unresolved historical exposure remains USD0.061344. Effective API exposure is USD0.99334896, leaving USD7.00665104 of API authority. Original reservation amounts and all 107 previous call rows were preserved bit-for-bit in the row digest; final known costs now have append-only settlement receipts. Both historical uncertain calls remain fully reserved. This corrects earlier overly conservative full-reservation headroom without erasing history or resetting funds.

The new USD5 authority was recorded exactly once alongside the prior USD2 addition. Approved account/inventory, exclusive claim/workload, immutable public registration, deployed hashes and live provider/prices passed before calls. The same existing host and sole canonical ledger were reused; no provisioning or ledger copy. Worker exit, remote artifact hashes and hub terminal failed status were verified before release. This claim lasted 407 seconds, estimated infrastructure USD0.008076; this is allocated-time accounting, not an invoice.

Execution, qualification, scientific interpretation, reporting and costs are retained separately in [scientific review](../results/QM-R1-01/scientific-review.json). The shared offline finalize hook supplies operational metadata only; this authored assessment supplies the scientific review.

## Next action

**FINISH this attempt; HOLD native expansion pending a concrete repaired run design.** The checked-in guard and saved-data regression resolve the immediate offline detection gap, but do not prove a model repair. A useful successor would balance positive/negative/unknown qualification in every family and compare direct exact parsing against model-selected evidence spans with deterministic normalization, preserving null versus asserted-value distinctions. Remove redundant unchecked status/value predictions and retain quote consistency checks. Use fresh cases and explicit stopping rules; do not resume these 15 cases as if the instrument had not changed.

Only after that interface is reliable does an independently annotated free-form incident corpus justify broader collection. Extra budget remains available; there was no automatic retry to obtain a favorable result.
