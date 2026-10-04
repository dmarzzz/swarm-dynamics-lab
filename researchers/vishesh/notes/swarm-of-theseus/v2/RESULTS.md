# Swarm of Theseus v2 — execution and qualification results

**Ran the new design and its one planned repair. Both completed, but the joint competence gate failed. No turnover pilot ran, so this iteration does not answer whether useful culture survives replacement.** Sixteen software checks pass; 48 model calls produced valid outputs with no provider failures or scoring discrepancies. Schema reliability did not imply correct behavior.

The strongest practical revision remains selective correction: keep the valid precaution while retiring an obsolete one, across two complete crew replacements. The third setting changes console commands while holding task truth stable. These mechanisms are implemented and prospectively documented, but their comparative effects are unmeasured.

## Measured qualification

Each entry has12 case decisions, clustered in two worlds. Small denominators and different fresh worlds preclude treating initial-versus-repair differences as a causal formatting effect.

| Scenario / attempt | Explicit-rule stable | Explicit-rule changed/interface | Historical learner stable | Gate |
|---|---:|---:|---:|---|
| Release / initial | 10/12 | 6/12 | 7/12 | Fail |
| Release / repair | 9/12 | 11/12 | 8/12 | Fail |
| Incident / initial | 9/12 | 11/12 | 7/12 | Fail |
| Incident / repair | 11/12 | 11/12 | 12/12 | Pass for this scenario |
| Migration / initial | 12/12 | 10/12 | 9/12 | Fail |
| Migration / repair | 8/12 | 9/12 | 9/12 | Fail |

The frozen joint gate required >=90% in every explicit-rule scenario/checkpoint and >=75% stable learner accuracy in every scenario, plus valid schemas. The incident component passes after repair, but selecting it after seeing results would not satisfy the original all-scenario gate. The planned612-call pilot was therefore not dispatched. No favorable reruns or threshold changes followed.

## What failed—and what was fixed

The first attempt sometimes misread evidence values, overcomplicated learned rules or added requirements despite an explicit rule. The repair made the same observations tabular, removed obsolete history from the clean ceiling and specified the rule family while withholding the mapping from learners. Wrong decisions persisted. One repaired release output acknowledges that its governing evidence is YES/YES, then holds anyway. This is a task-application failure before any replacement, not a demonstrated failure of cultural preservation.

Process repairs succeeded: exact immutable public plan/review checks, exclusive host and separate quota, saved provider failure categories, fixed majority/missingness handling, two-generation lineage tests, and public failure preservation. The previous artifact metadata enum defect was fixed using the provenance writer with artifact bytes and ingredient hashes preserved; full schema validation now runs rather than silently omitting jsonschema.

Remaining candidate explanations are row/column binding, conjunction application and interference between decisions and note-writing. They are hypotheses, not verified causes. A stronger model or deterministic executor may help, but neither has been tested here. Giving actors the answer or lowering the gate would make the culture comparison less credible.

## Practical decision

Do not scale this three-scenario instrument on the current model/prompt. The incident setting is the best qualified candidate for a separately planned successor. First separate acquisition from action application with atomic/batched and decision-only/note-writing controls. Then either qualify all tasks on a suitable model or preregister an explicitly narrower incident-only study. Keep the single-controller baseline and cross-model comparison open; this study has not established a swarm advantage or novelty.

## Execution and cost

| Attempt | Calls | Complete runs | Audit disagreements | Estimated actual API cost | Conservative reservation |
|---|---:|---:|---:|---:|---:|
| S0 | 24 | 12/12 | 0 | USD 0.103255 | USD 0.357357 |
| S0-repair | 24 | 12/12 | 0 | USD 0.061956 | USD 0.210741 |
| Total | 48 | 24/24 | 0 | **USD 0.165211** | **USD 0.568098** |

Actual API cost is calculated from returned token usage and the verified USD 1/M input, USD 5/M output pricing; it is not an invoice. The approved ceiling was USD 15/660 calls; unused call capacity was not consumed after the stop rule. No machine purchase. Public runs show execution completion; this report and experiment description distinguish failed qualification.

## Evidence and reproduction

- [Initial post-mortem](reviews/S0-post.md) and [repair post-mortem](reviews/S0-repair-post.md).
- [Initial manifest/summary](results/S0/summary.json) and [repair manifest/summary](results/S0-repair/summary.json).
- [Prospective plan](PLAN.md), [deployment record](DEPLOYMENT.md), and blocked [pilot assessment](reviews/S1-pre.md).
- Public page: https://swarm-live.pages.dev/#/x/swarm-of-theseus-v2 . Original immutable run-specific receipts remain in each manifest even after the experiment description is updated.

Full local evidence folders preserve all48 raw calls, exact repaired user text,48 event records,24 terminal outcomes and process receipts. Use `src/analyze.py` on a downloaded attempt to recompute scores; raw observations remain unchanged. The final qualification viewer compares attempts, scenarios, worlds, controls and checkpoints using measured decisions only. It does not depict an unexecuted turnover experiment.
