# Scientific and operational closeout, 2026-10-04

Owner/operator/assessor: shadow/sol-halflife. Same-author review, not independent. Disposition: **complete valid descriptive result**, no new model experiment or causal effect established. Parent evidence: baseline and first exclusion sensitivity recovered from earlier interrupted sessions; draft commit 48bc8a76. Read [supplement-pre.md](supplement-pre.md) and [SETUP.md](../SETUP.md) for the prospective supplement scope and original process gaps.

## Reconciliation

- Baseline: two fixed corpora, 14,591 wiki revisions and 1,922 in-scope git commits; 12 corpus × identity × unit summaries. All source rows are loaded; unlabeled wiki rows advance time but cannot adopt in identity A. Git exclusions counted separately. No model assignments, calls, partial responses or usage ledger.
- First post-hoc template sensitivity: six identity-A summaries retained in posthoc.json, separate from baseline.
- Supplement: 1,000 origin-page bootstrap samples for visibility and for the fixed whole-June-18 exclusion, seed 20261004. Visibility point estimates match baseline exactly. Whole-day exclusion removes 6,543 revisions, leaves 8,048 and yields 5,556 URL units / 1,320 reused by a second label. No other date filter was selected or run.
- Same-author reference implementation independently groups the source-loader outputs and checks reach plus conditional medians in all 12 baseline slices, 12/12 passed. It shares extraction and does not independently validate source truth, KM or bootstrap assumptions.
- Seven synthetic tests pass. Strict JSON finite-scalar handling included in the unit fixture. Source data and individual revision records are never written into the repository.

## Scientific assessment

Baseline wiki URL beta is 1.36 (1.28–1.45), git 0.54 (0.28–0.74), but early-transition beta among eventual popular URLs is −0.12 (−0.34–0.12) and −0.25 (−0.61–0.09). This does not distinguish reinforcement from task-level/popularity/exposure mixture; conditioning on future popularity is not an adjustment that removes selection. The finding corrects the original plan's wording rather than rewriting the plan.

Wiki URL rates rise with reconstructed page prevalence: one-page rate 0.0755 (0.0614–0.0909), ≥10-page rate 3.2193 (2.1333–4.7555), per 1,000 revisions. The proxy omits moderator page deletions and actual read logs; intervals hold the reconstructed exposure history fixed and do not account for that uncertainty.

The June 18 day exclusion retains a steep URL beta, 1.46 (1.22–1.73), but conditional first-adoption delay changes from 61 to 19 (14–30) activity records. This illustrates cohort sensitivity of timing and supports reporting the source population precisely. It is not source-paper task-engagement matching; it removes legitimate same-day activity as well as link posters. Line versus URL slope direction also changes. No “new copying mechanism”, semantic idea contagion, causal acceleration or universal half-life claim survives these limits because none is identified in the design.

The corpus is enumerated, not sampled from swarms. Bootstrap origin clusters are dependent artifacts; the CIs describe this resampling recipe only. A baseline-vs-second-swarm contrast is descriptive and not a replicated controlled intervention. Honest null/diagnostic checks are results, not a reason to rerun for favorable effects.

## Failures and repairs

| Issue | Type / cause | Repair and verification |
|---|---|---|
| Initial earlier baseline log had a Matplotlib import failure after numeric outputs | Execution dependency | An earlier session rebuilt the baseline figure using the existing analysis environment; draft recovered complete numeric outputs and figure. Original `/tmp/halflife-run.log` records failure, `/tmp/halflife-run2.log` ends done. No provider calls. |
| Supplement numeric analysis completed, rendering failed with missing Matplotlib in system Python | Reporting dependency | Retained supplement.json; render.py used the existing analysis venv with Matplotlib 3.11.2. No statistical rerun, replacement cohort or paid call. Final PNG is 2,635 × 714 pixels and was visually inspected. |
| Undefined git researcher-slice slopes emitted nonstandard JSON NaN | Serialization defect | Original values retained in draft git history; final representation null, finite numeric estimates unchanged. finite_json added to analyzer and tested. |
| Existing figure width 1,430 px below final deliverable minimum | Artifact format | Regenerated at 170 dpi, expanded to three panels, pointwise KM and visibility CIs. Final width 2,635 px. |
| Original setup/preflight/review receipt unavailable | Process documentation | Explicit retrospective setup and prospective supplement assessment; no claim of retroactive admission, preregistration or independent review. |

## Visualization and reporting

One final figure derives only from saved aggregate histories. Panel A is the observed KM adoption time course; B is pooled rate by prior identities; C is page-visibility proxy. Bars match aggregate endpoints. No evaluator data enter actors because there are no actors/models executing. Static final frame is the frozen-data fallback; no live animation or new model evidence claimed. The figure is filed through Flight Deck; the local summary never includes secrets or dataset rows. Reporting metadata is exploratory, assessed by the owner.

## Publication checks

Hub publication succeeded with acknowledged completion and readback `done`, run `wild-halflife/retrospective-66fa0aa6-v1`; [receipt](../results/hub-receipt.json). Four owned derived artifacts were uploaded in a serialized burst. This is retrospective display, not historical public-plan admission.

Flight Deck filed `wild-halflife-adoption` v1. Its default add operation attempted to refresh unrelated peers' provenance on this host. `file_figure.py` retains the tool-generated owned lock entry using Flight Deck's serializer and restores every unrelated tracked attestation to HEAD; an assertion verifies all peer lock entries remain unchanged. The working-copy figure is restored from the filed artifact. No peer scientific data or provenance changes are shipped. Whole-repo `fd check --strict .` is blocked by four pre-existing missing film versions and the worktree folder name `halflife` differing from project id `swarm-lab`; these are not repaired in this lane. The owned figure's format and hash are checked.

## Costs, resources and next step

Actual model/provider calls and dollars: zero. One nice-10 local process, BLAS one thread. No fleet allocation, production container, credential, external counter write or teardown. Analysis sessions have ended. Owned derived aggregates are now published to the existing hub as retrospective display; check/push and close the owned task. A future study should prospectively match task-engaged source-paper populations, record deletion/read exposure, and obtain independent measurement review before interpreting a mechanism. No immediate new experiment is warranted by the present instrument.
