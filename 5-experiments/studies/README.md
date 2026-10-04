# 5-experiments/studies: exploratory studies

The studies of phase 5 of [Swarm Dynamics Lab](../../README.md). This folder holds one folder per researcher
and, inside it, one folder per study. No study here has passed the hypothesis gate, so each is labelled
exploratory and scored in the [evidence registry](../EVIDENCE.md).

## What this is

A study is one researcher's work on one question: the plan, the code, the records and the results. The
[evidence registry](../EVIDENCE.md) records the evidence score and sample size of each implemented cohort,
and the [rubric](../EVIDENCE-METADATA.md) defines the score. Start from the registry to find a study, then
read that study's own README and results file for the caveats.

## What is in here

The folder held 117 study folders on 4 October 2026.

| Folder | Contents |
|---|---|
| [`dmarz/`](dmarz/) | 51 study folders and 10 loose notes. Includes the sybil series (`sybil-*`), the market-split series (`market-split*`), `discussion-dose/`, `compositional-safety/` and `question-atlas/`. |
| [`shadow/`](shadow/) | 17 study folders and 5 loose files. Includes the experiment factory ([`factory/`](shadow/factory/README.md)), `qa/`, `capture-memory/`, `landscape-map/` and the hackathon submission packet (`submission/`). |
| [`vishesh/`](vishesh/) | 49 study folders and 7 loose files. Start with its [README](vishesh/README.md), which indexes the project briefs, readings and studies. |

A study folder normally contains:

| File | What it is |
|---|---|
| `README.md` | The question, the status and, for a registered cohort, the evidence block generated from the registry. |
| `SETUP.md` | The setup record from the toolkit runbook, with the evidence for each gate. |
| `preregistration.md`, `design.yaml`, `experiment.yaml` | The plan, the conditions and the parameters, committed before the first run. |
| `src/` | The code that ran. |
| `RUN.md` | How the study was run, with the exact commands. |
| `results/` or `records/` | Saved outputs that the results are recomputed from. |
| `RESULTS.md` | The results, with their caveats. |
| `reviews/` | The pre-run assessment and the post-mortem for each attempt. |

Not every folder has every file. Some studies are a single Markdown file for a hunch or a note.

## How to add to it

Only the owning researcher's agents write to a researcher's folder (see [AGENTS.md](../../AGENTS.md)). Create
`5-experiments/studies/<you>/<study>/` and follow the steps in [`../README.md`](../README.md). The matching
coordination folder (directives, inbox, agent status files, logs) is `lab/researchers/<name>/`.

## Where it goes next

The shared methods, runbooks and templates these studies follow are in
[`../toolkit/`](../toolkit/README.md). A study's shipped figures, films and docs are filed in
[`artifacts/`](../../artifacts/).
