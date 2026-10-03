---
id: veselovsky-2023-artificial
type: paper
title: 'Artificial Artificial Artificial Intelligence: Crowd Workers Widely Use Large Language Models for Text Production Tasks'
authors:
- Veniamin Veselovsky
- Manoel Horta Ribeiro
- Robert West
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2306.07899
doi: null
arxiv: '2306.07899'
cite: 'Veselovsky, V., Ribeiro, M. H., & West, R. (2023). Artificial Artificial Artificial Intelligence: Crowd Workers Widely Use Large Language Models for Text Production Tasks. arXiv:2306.07899.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 187 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Reruns an abstract-summarisation task on Amazon Mechanical Turk and combines keystroke logging (for example, pasting rather than typing) with a synthetic-text classifier to estimate how many crowd workers used LLMs. Estimates that 33-46% of workers used LLMs on the task, which threatens crowdsourced "human" data. Code and data at github.com/epfl-dlab/GPTurk.

## Contribution

Early measured base rate of LLM use in a paid human-data pipeline, and a detection design that pairs a behavioural signal (keystrokes) with a text classifier.

## Key results

- Measured (abstract): 33-46% of MTurk workers used LLMs for the summarisation task.

## Methods and models

Task replication on MTurk; keystroke detection plus synthetic-text classification. Abstract read only.

## Limitations and open questions

One LLM-friendly task; the authors say generalisation to other tasks is unclear. Abstract depth.

## Relevance to us

Behavioural telemetry (copy-paste, typing cadence) catches what text detectors miss, a lesson for agent detection on any platform that can instrument input. Follow-up with agents in mind: [[xu-2026-penny]].
