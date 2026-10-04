# Experiment setup record: wild-halflife / saved-data analysis v1

This record is **retrospective**, created during continuation on 2026-10-04. It follows the headings of the [setup template](../../../toolkit/agent-experiments/templates/experiment-setup.md) and [setup runbook](../../../toolkit/agent-experiments/EXPERIMENT-SETUP.md). It is not launch authorization, independent review or retrospective preregistration.

## Ownership and question

- Owner/operator: shadow/sol-halflife. Design and arithmetic review: same author, not independent.
- Research status: human-directed exploratory observational analysis of existing local files and saved git history, not an accepted hypothesis or a controlled model experiment.
- Question/claim: time to reuse by another identity and association of reuse arrival rates with prior adopter count, in two fixed corpora only.
- Intended decision: determine whether exact-unit adoption curves are a useful cross-swarm instrument, without interpreting their slopes as causal copying effects.
- Prior work: [PLAN.md](PLAN.md), arXiv 2609.09150, kmad/agent-swarm-forensics. No claim that formal survey/hypothesis review gates were passed.
- Preceding results: [baseline summary](results/summary.json), [first post-hoc exclusion sensitivity](results/posthoc.json), [draft](FINDING.md). No original pre/post run review files were recovered; retained as a process gap.
- Continuation assessment: [supplement-pre.md](reviews/supplement-pre.md), written before supplemental execution.

## Gate evidence

| Gate | Status | Evidence / next action |
|---|---|---|
| G0 Question and applicable research gates | exploratory only | PLAN.md cites nearest sources. Formal hypothesis acceptance not claimed. |
| G1 Plan before implementation | documented | Plan commit 2cb859a5 precedes analysis-code commit a76306ae; supplement assessment committed at 4eff98d0 before supplemental execution. |
| G2 Instrument and offline checks | pass, same-author | Seven synthetic checks, including repeats, ties, censoring, known KM/rate arithmetic and visible-pages bootstrap. |
| G3 Original admission documentation | incomplete historical record | No original pre-run/public-preflight receipt recovered. Later hub publication is explicitly retrospective, not proof of admission. No calls/spend/allocation occurred. |
| G3 Supplement admission | saved-data checks only | supplement-pre.md freezes the post-hoc day exclusion and adds uncertainty, zero model/provider calls. |
| G4 Model qualification / scientific escalation | not applicable | No model execution, no escalation and no controlled-effect claim. Software checks do not establish model competence. |
| G5 Reconciliation and closeout | see post-mortem | [supplement-post.md](reviews/supplement-post.md); no claim of full protocol compliance. |

## Design and instrument index

- Original plan: [PLAN.md](PLAN.md), untouched; definitions frozen before baseline outcomes.
- Source snapshots: SHA256 of revisions.jsonl.gz and full frozen git SHA in summary.json. No raw source records committed.
- Units: exact normalized URLs, lines and hosts; wiki insertion hunks and git added lines. First adoption by each identity only.
- Independent units: **not established**. Two observed corpora. Bootstrap clusters are origin pages / commits, not random independent worlds; units within and across clusters can share dependencies.
- Precision: complete enumeration of the scoped artifacts, 1,000 cluster resamples, no power claim or optional stopping.
- No development/scientific split or sealed holdout. Post-hoc checks labeled as such.
- No agent prompts, provider credentials, effective model contexts or model configuration.
- Offline checks: [test_halflife.py](test_halflife.py); same-author reference recomputation in [verify_results.py](verify_results.py).
- Visualization mapping: supplement-pre.md. Static supported fallback; one figure with observed adoption curves and rates. No animation/live-model frame claimed.

## Current attempt admission

Explicitly manual saved-data workflow; shared experiment operations dispatch is unsupported and unnecessary here.

| Operation | Command or reason |
|---|---|
| Inspect / offline tests | `python3 5-experiments/studies/shadow/wild-halflife/test_halflife.py` |
| Dispatch model experiment | Unsupported; no model calls authorized or required |
| Resume | Existing baseline and first sensitivity retained in results; supplement is deterministic and repeatable |
| Analyze saved evidence | README.md reproduction commands, frozen git revision |
| Close | Preserve outputs, update report/status/task, lab.py check and push |

- Original baseline code and results predate this retrospective record. Do not treat missing historical checks as passed.
- Supplement parent: baseline saved-data report and draft commit 48bc8a76. Read prior evidence and wrote assessment before supplement.
- Public immutable plan: `https://github.com/dmarzzz/swarm-lab/blob/2cb859a5/researchers/shadow/notes/wild-halflife/PLAN.md`; no original network-verification receipt present.
- Calls/tokens/spend cap and observed: zero. No retry/provider ambiguity or model outcomes. Existing local data and a one-process nice-10 job, BLAS one thread, no provisioning.
- Runtime/software versions: supplement.json and requirements.txt.
- Credentials: none needed for analysis. Optional own-result hub publishing uses the existing configured client, never source data or secrets.

## Attempt and repair history

| Analysis | Outcomes | Disposition |
|---|---|---|
| Baseline | 12 source × identity × unit summaries; static figure | Retained unchanged |
| First post-hoc boilerplate exclusion | Six identity-A summaries; separate posthoc.json | Retained, exploratory sensitivity |
| Supplement | Visibility CIs, whole-June-18 exclusion, schema aggregates; expanded figure | Separate supplement.json, not pooled with baseline |

Documented corrections: the plan's phrase “remove selection” is not valid for conditioning on eventual popularity. FINDING.md corrects it without rewriting the original plan. “Deletions ignored” in the baseline visibility note means moderator page-deletion events, not URL removal within revision bodies. The supplement spells out that distinction.

## Closeout and successor handoff

Execution and outputs: see supplement-post.md. Scientific interpretation: exploratory descriptive finding with mechanism-identification limits. Process compliance: original documentation incomplete; no retrospective pass claimed. Actual cost: zero; no experimental workers, fleet claim, credentials or teardown. Next action if extended: predefine a source-paper-compatible task-engaged cohort, explicit content and deletion-event exposure reconstruction, and an independently reviewed analysis; do not change the present frozen cohort to seek a favorable contrast.
