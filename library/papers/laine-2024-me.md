---
id: laine-2024-me
type: paper
title: "Me, Myself, and AI: The Situational Awareness Dataset (SAD) for LLMs"
authors: [Rudolf Laine, Bilal Chughtai, Jan Betley, Kaivalya Hariharan, Jeremy Scheurer, Mikita Balesni, Marius Hobbhahn, Alexander Meinke, Owain Evans]
year: 2024
venue: arXiv preprint (NeurIPS 2024 Datasets and Benchmarks Track, per citing papers)
url: https://arxiv.org/abs/2407.04694
doi: null
arxiv: "2407.04694"
cite: "Laine, R., Chughtai, B., Betley, J., Hariharan, K., Scheurer, J., Balesni, M., Hobbhahn, M., Meinke, A., & Evans, O. (2024). Me, Myself, and AI: The Situational Awareness Dataset (SAD) for LLMs. arXiv preprint arXiv:2407.04694."
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

SAD is a benchmark of over 13,000 questions in 7 task categories testing LLM situational awareness: recognising their own text, predicting their own behaviour, telling internal evaluation from real deployment, and following instructions that depend on self-knowledge. Across 16 base and chat models, all beat chance, but the best (Claude 3 Opus) is still far from a human baseline on some tasks. SAD score is only partly predicted by general knowledge (MMLU). Chat models beat their base models on SAD but not on general knowledge.

## Contribution

The foundational benchmark that broke situational awareness into measurable sub-abilities, including the "stages" task (evaluation versus deployment) that later evaluation-awareness work extends.

## Key results

- 16 LLMs, 7 categories, more than 13k questions. All models score above chance and below the human baseline on some tasks.
- Chat fine-tuning raises SAD scores without raising MMLU.

## Methods and models

Question-answering and instruction-following tests. Code and results at situational-awareness-dataset.org (not opened).

## Limitations and open questions

Static questions with no agentic runs, and no measure of awareness changing during an interaction.

## Relevance to us

Seminal background for V5's measurement of "says it is being evaluated". [[needham-2025-large]] extends its stages task to 61 datasets, including agentic transcripts. Cited by [[krakovna-2026-realistic]] and [[li-2026-decomposing]].
