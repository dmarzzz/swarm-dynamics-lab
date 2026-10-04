# Immune Response — output order improved consistency, not preservation

Owning scientific post-mortem, 2026-10-04. [Native run](https://swarm-live.pages.dev/#/r/immune-response-v3%2F1004-213504-24b1f5), [immutable C1 plan](https://github.com/dmarzzz/swarm-lab/blob/e6e4c5f0be5c532726ef69afb6f61102d8d0d719/researchers/vishesh/notes/immune-response-v3/controller-study/c1/PLAN.md), [reconciliation](c1-reconciliation.json), [complete manual review](c1-manual-review.json), [quality assessment](c1-quality.json), [animation](c1-replay.gif).

## Result

**Neither arm qualified.** Both repaired the runtime crash and configuration fault, but both unnecessarily intervened on an already-healthy service whose alarm was stale. Putting the brief observable justification before the action avoided one rejected store deployment and its action/explanation contradiction. It did not improve the fixed service-outcome or joint qualification counts on this four-world panel.

| Endpoint | Action first | Justification first |
|---|---:|---:|
| Service-outcome gates passed | 3 / 4 | 3 / 4 |
| Diagnosis + outcome gates passed | 2 / 4 | 2 / 4 |
| Fully correct categorical diagnoses | 6 / 8 ticks | 6 / 8 ticks |
| Healthy simulator ticks | 8 / 8 | 8 / 8 |
| Useful same-version crash restarts | 1 | 1 |
| Rejected deployments | 1 | 0 |
| Selected-action/explanation contradictions | 1 | 0 |
| Actual action outputs in assigned key order | 8 / 8 | 8 / 8 |

The paired difference in healthy ticks and outcome-gate attainment is zero for every root. This is not proof of equivalence or no population effect: there are four previously inspected authored roots, one rollout per arm/root, related generator ancestry and no same-condition fresh repeats. Alternating arm order balances first position over this small panel; it is not a large randomized replication. The comparison tests an output-order instruction/schema package, not hidden reasoning or the effect of changing model strength.

C1 completed all eight assigned trajectories and all 32 calls without provider, schema, usage, route or ordering failure. The one-hour watchdog was not reached. Q/A and the earlier holdouts were not collected. The scientific baseline remains **GAP**; trace replay and a completed discriminator do not establish stable native behavior on varied tasks.

## What each world shows

**Healthy service.** Both arms waited twice, with correct diagnoses and explanations. This establishes restraint on the straightforward current-evidence case only.

**Verified worker crash.** Both arms deployed the current worker binary and immediately restored health. Justification-first then inspected to verify the repair. Action-first instead refreshed the registry and claimed this would refresh liveness evidence. Its selected action agrees with the named tool in its explanation, so this is a false tool-effect claim rather than the counted action-selection contradiction. Registry refresh does not measure runtime liveness. The fixed service gate passes because the prior restart succeeded; broader operational readiness should still account for the verification defect.

**Stale false alarm.** Both first diagnoses falsely marked storage format incompatible, despite matching catalog and persisted formats. Action-first selected an incompatible store deployment while its later explanation acknowledged that this was wrong and concluded that the worker should be restarted. The simulator's existing persistent-format safety gate rejected that action. It then restarted the healthy worker based on stale telemetry. Justification-first correctly described the compatible configuration in its explanation and avoided the store deployment, but still restarted the healthy worker from a stale alarm before inspecting. A consistent explanation can accompany an unjustified action.

Both arms remained green on health because the service began healthy and the simulator rejected the unsafe store mutation. **Green health is not successful preservation:** unnecessary intervention, rejected action and missing timely evidence verification are retained by the fixed gates. The inherited simulator rejection is not a newly added controller guard or evidence of correct model judgment.

**Genuine configuration fault.** Both selected the correct worker upgrade and restored compatibility. The clearer `failed_service` definition was followed on the first tick; the process was live, so both returned `none` while reporting a configuration fault. On the second tick both incorrectly reported the cached RPC failure even though the currently deployed catalog was now compatible. Both appropriately inspected, but the exact diagnosis gate failed. Source freshness and the distinction between cached checks and current configuration remain the observable weaknesses.

All sixteen categorical diagnoses and sixteen executed action/explanation pairs were reviewed. The manual annotations distinguish selected-action contradictions, false tool-effect claims, unsupported current-liveness assertions and diagnosis errors. They do not claim access to hidden reasoning. All raw requests and provider responses remain retained privately; summaries and measured results are public.

## Comparator and case validity

A separate public-observation rule controller passes the four C1 roots and twelve constructed future-panel cases offline. It reads the same catalog, deployment and telemetry fields, inspects stale liveness, restarts an observed failed process and enumerates a single compatible deployment. It has no simulator/gold imports and no hidden case labels. Its competence boundary is declared: known catalogs, authored one-fault/two-tick tasks, not general planning, multi-fault recovery or sensor deception. This demonstrates feasibility and supplies a strong simple comparator; it does not turn scripted behavior into native agent evidence.

Absent advice is an LLM control condition, not the rule comparator. Correct/stale/incorrect advice remains prospective authored manipulation, not natural peer-swarm evidence. AI Village informs evidence/visibility methodology but supplies no adjudicated service-repair ground truth here. The twelve constructed worlds are publicly authored and operator-validated, native-unseen cases—not operator-uninspected or independently authored holdouts.

## Admission, reproducibility and closeout

The exact approved runtime was `e6e4c5f0be5c532726ef69afb6f61102d8d0d719`, with packet SHA256 `c1f7bd6b0894274687efb85ff4e0970001b875790e833b8e3e3d57d0e28e57cf` and plan SHA256 `840594740c71b064537172485a047a1b5fb7982cb19a533fa25b44aa2e510b08`. Eight immutable assignments and 80 source/config/plan hashes preceded native collection. All 7 C1, 9 parent-controller and 41 prior-freshness tests passed remotely on Python 3.12.3 with jsonschema 4.26.0, matplotlib 3.11.2, Pillow 12.3.0 and PyYAML 6.0.3; the pinned local Python 3.13.13 environment also passed. A separate default-Python dependency failure was not represented as a test pass.

Fresh public endpoint metadata confirmed Anthropic-only Opus 4.6 at USD5/25 per million input/output tokens, with strict outputs supported. Actual response receipts confirm the requested route. No fallback, retries or private operator context was used. Immutable public registration and page preflight passed before dispatch. The approved account, exclusive existing host, posted rate and original ledger were checked against actual records. The finite C1 envelope was appended to the same ledger without resetting historical calls or reservations.

All 32 request hashes, response bodies and usages reconcile; all 16 simulator transitions replay; all 16 actual action serializations match their assigned order. Seven indexed hub artifacts were fetched and hash-matched. Every assignment is complete; none is excluded. The saved-data animation shows actual native outcomes. Its inherited empty holdout panel is a display placeholder: C1 did not include or fund a holdout stage. Row PASS labels refer to service outcomes only, not full diagnosis/consistency qualification.

The model relay exited after its 32nd request. The exact SSH tunnel was closed and zero experiment workers were verified before allocation release. The original ledger and raw evidence were backed up; the stage envelope was closed with no successor. Claim 441 was shortened to 90 minutes by 444 and released by 446. Operational finalization is paired with this authored scientific assessment; collection completion is separate from failed qualification.

## Cost

| Arm | Input tokens | Output tokens | Actual model cost | Conservative request reservations |
|---|---:|---:|---:|---:|
| Action first | 25,702 | 1,475 | USD0.165385 | USD0.718405 |
| Justification first | 25,708 | 1,404 | USD0.163640 | USD0.717575 |
| Total | 51,410 | 2,879 | **USD0.329025** | **USD1.435980** |

The original v3 ledger now holds **517 calls / USD6.248035 reserved of USD8**, leaving USD1.751965 unreserved. USD0.335540 of the unused C1 model envelope was closed; existing per-request reservations were not refunded or erased. Known actual charges are not the same as reservation exposure. Historical v2 and earlier infrastructure remain in central project accounting.

The existing host's verified posted rate was USD0.07143/hour. The exclusive allocation lasted 425 seconds, giving an attributable compute estimate of **USD0.008432708**. This is not an observed invoice or an additional machine purchase. The admitted infrastructure hold was USD0.15, with a 90-minute compute bound of USD0.107145; ancillary/invoice reconciliation remains central. Count the host lifetime once, with this window as attribution, not another resource bill.

## Next scientific decision

Do not open Q/A automatically: the C1 candidate failed its prerequisite. Do not spend another cycle on minor output-order prompting or a stronger-model sweep. PI's subsequent guidance is incorporated in the [prospective paired verification study](../../../verification-study/PLAN.md), with an offline implementation and six passing tests; it has no native dispatcher or paid admission.

The new construction uses six incident roots (three service locations × two compatible data configurations), each with an identical older fault report followed by a fresh confirmation or contradiction. Compare the competent public-observation rule, the fixed unguarded agent and an explicitly labeled verification guard. The guard reads only public evidence, rejects unsupported deployments without substituting a repair, and consumes the tick. Measure attempted and executed unnecessary intervention, missed repair, an explicitly simulated service-opportunity cost and actual post-action inspection separately. Truthful fresh probes are an assumption; this does not erase C1's failed stale-only condition or establish natural-peer swarm behavior.

The proposed two fresh repeats across both branches and both native architectures require at most192calls, USD10.629120model reservation plus a separately verified infrastructure ceilingUSD0.15. This would require a named PI decision and v3model slice of at leastUSD16.877155, retaining all historical exposure inside theUSD200portfolio. The six paired roots are not twelve independently authored incidents; analysis must disclose family clustering and repeat variability. No native successor has been launched. This supersedes the earlier suggestion merely to run the unguarded controller twice on twelve worlds.

Guarded preservation partly follows from the declared precondition under truthful observations; do not call it emergent intelligence. The empirical issue is whether necessary repair and verification survive the guard's delays and feedback, compared with the competent rule controller. A reproducible adverse or null tradeoff can be useful. Judge the resulting scoped experiment on valid cases, controls, complete repeated execution and honest limits, not whether it yields a favorable effect.
