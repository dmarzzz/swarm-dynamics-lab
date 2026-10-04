# Experiment evidence metadata

Every experiment entry should expose **evidence_confidence** and **sample_size_summary** near its title. These fields help readers judge what an experiment establishes without mistaking agents, messages or calls for independent samples. Use the same fields for exploratory studies in researcher notes and accepted experiments under `experiments/`.

The [evidence index](EVIDENCE.md) summarizes the current assessments. The editable source is [evidence-metadata.json](evidence-metadata.json); `python3 scripts/experiment_evidence.py --write` updates its marked document blocks and index. `--check` validates metadata, registration coverage and rendered consistency. The existing lab CI check runs the metadata validator and its offline tests, so a newly added registration or stale generated block is visible in review. These commands read documents and write metadata only; they do not launch experiments, change run configurations or update the external live hub.

## Confidence scale

This is an **ordinal editorial assessment of evidence for the explicitly stated claim**, not a probability that the claim is true, a confidence interval, an agent's self-reported certainty, a ranking of how interesting the idea is, or formal research-gate approval. The score has meaning only with its claim and rationale. Scores are not averaged across studies or combined across incompatible cohorts.

| Score | Label | Interpretation |
| --- | --- | --- |
| 0 | Untested | No observed evaluation of the stated claim in this scope. A proposal, unrun successor or software test alone does not establish an empirical effect. |
| 1 | Exploratory | Descriptive or diagnostic evidence only: tiny or dependent samples, scripted/proxy behavior, failed competence, incomplete outcomes, or major identification limits prevent a dependable effect claim. |
| 2 | Limited | An interpretable controlled comparison supports a narrow claim, with competent controls and accounted outcomes, but task/model diversity, precision or replication remains limited. |
| 3 | Moderate | The claim survives a prospectively specified evaluation with adequate independent task coverage and uncertainty, credible controls and relevant robustness checks. Material scope limits remain explicit. |
| 4 | Strong | The scoped finding is independently replicated across relevant tasks or implementations, with adequate precision, robust controls and consistent utility/safety evidence. This still does not imply universal generalization. |
| null | Unassessed | Available evidence has not been sufficiently assessed to assign a score. Unknown is not zero. Give the missing evidence and next review step. |

Assign the highest level whose requirements are supported, then explain the main limitation in one sentence. Do not infer a score from a paper count, call count, model brand, a successful process exit or a favorable effect. A valid null or adverse result can have high confidence. A failed qualification can establish a diagnostic failure while leaving the intended treatment claim unsupported; label that boundary in the claim and rationale. Scripted mechanism checks may earn exploratory confidence for their stated fixture, without earning confidence about model behavior.

Record the assessor, date, source commit and supporting paths. These are source-reported assessments unless an independent audit is explicitly linked. Reassess after a new cohort, model/measurement change or completed analysis; retain historical records in Git. An earlier assessment must not be silently treated as a live run status.

A study row may override `assessor` and `assessed_at` when its owner updates the evidence. Otherwise it inherits the registry defaults. The renderer shows each cohort's actual assessor and date, so a later operational assessment is not attributed to the original reviewer.

## Short sample-size field

Write one compact sentence, preferably under 300 characters and never over 500, in this order:

1. **Independent unit and count:** task roots, maps, documents, founder lineages or source corpora. If structural families are reused, say so. If independence or the count is unknown, state that explicitly.
2. **Execution denominator:** completed/analyzed versus assigned; failed, partial and unstarted counts where material. Keep qualification and main evaluation separate.
3. **Population and repeats when helpful:** agents per world, repeated executions, arms, rounds or calls. These describe exposure or cost, not additional independent samples.
4. **Planned versus observed:** label proposed counts as planned. An unrun design has zero observed outcomes even when its plan contains thousands of episodes.

Examples of the format, not additional empirical findings:

- `Observed: 24 paired task roots; 2,400/2,400 condition outcomes; 36–972 simulated identities feeding one synthesizer; one graph family.`
- `Observed: 3 reused source corpora; 180/180 assignments across placements and conditions; 200 curators; no new model calls.`
- `Observed: none. Planned: 6 world roots, 4 arms; two replacement waves with 3 agents. Counts are development allocation, not power.`

Do not pool shared control rows, duplicate documents, descendant branches, model conditions or repeated calls as independent observations. A cluster count is not necessarily a random sample from the intended real-world population. Report dependent outcome totals alongside the real experimental unit. Unknown outcomes remain unknown; an operational completion denominator is distinct from a bound on an unobserved scientific outcome.

## Cohorts and upkeep

One registry row represents a coherent version/cohort and claim. Use separate rows for a new model, redesigned task or endpoint when pooling would mislead; several rows may render on one document. Keep historical failed attempts in the sample summary or supporting source instead of erasing them. A successor must not inherit its predecessor's score or sample count.

Registration files and frozen run manifests remain unchanged. Map each existing registration path to its registry row; list additional implemented studies that register in code explicitly. Pure idea banks are not counted as executed experiments, and preference/novelty scores remain separate. Templates carry unassessed fields until the author fills the claim and observed/planned denominator.

After editing the registry, run:

```sh
python3 scripts/experiment_evidence.py --write
python3 scripts/experiment_evidence.py --check
python3 -m unittest discover -s scripts -p 'test_experiment_evidence.py'
python3 scripts/lab.py check
```

The first two commands synchronize metadata, not evidence. Read the supporting results and review the independent unit before increasing a score. Existing public-plan, qualification and research-review requirements still govern experimental execution.
