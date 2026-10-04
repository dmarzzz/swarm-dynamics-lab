# 5-experiments: studies, evidence and toolkit

Phase 5 (experiment) of [Swarm Dynamics Lab](../README.md). This folder holds each study's plan, code,
records, results and post-mortems, and a study must commit its plan before the first run and carry a pre-run
assessment and a post-mortem for every attempt.

## What this is

The experiments folder is where the lab's questions get measured. A registered experiment
(`5-experiments/<id>/`) needs an accepted hypothesis. No hypothesis was accepted during the hackathon, so
there is no registered experiment here: every run so far is an exploratory study under `studies/`, labelled
exploratory. The evidence registry gives each cohort a 0 to 4 editorial score for one stated claim. The
score does not promote an exploratory study through the research gates.

## What is in here

| Path | What it holds |
|---|---|
| [`EVIDENCE.md`](EVIDENCE.md) | The evidence registry: 150 cohorts, each with an evidence score and a sample size. 48 score 0/4, 76 score 1/4, 25 score 2/4, one is unassessed and none scores higher. |
| [`EVIDENCE-METADATA.md`](EVIDENCE-METADATA.md) | The rubric for the score, and how to keep the registry current. |
| `evidence-metadata.json` | The registry in machine-readable form. |
| [`studies/`](studies/README.md) | 117 study folders, grouped by researcher. |
| [`toolkit/`](toolkit/README.md) | The shared setup runbook, templates and harnesses that studies follow. |

## How to add to it

1. Read the [experiment setup runbook](toolkit/agent-experiments/EXPERIMENT-SETUP.md) and copy its
   [setup record](toolkit/agent-experiments/templates/experiment-setup.md) into your study folder as
   `SETUP.md`.
2. Write and commit the plan before the first run. Before each attempt, read the previous post-mortem and
   complete the pre-run assessment.
3. Report every run, including failures, and write the post-mortem when the attempt ends.
4. Add or update the study's cohorts in the registry as [`EVIDENCE-METADATA.md`](EVIDENCE-METADATA.md)
   describes, then run `python3 scripts/experiment_evidence.py --check`.

Keep large outputs out of git (see `.gitignore`) and link them instead.

## Where it goes next

Experiments test the hypotheses in [`4-hypotheses/`](../4-hypotheses/README.md). Finished figures, films,
docs and datasets are filed in [`artifacts/`](../artifacts/) with their inputs and the script that made them.
