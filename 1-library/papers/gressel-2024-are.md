---
id: gressel-2024-are
type: paper
title: "Are You Human? An Adversarial Benchmark to Expose LLMs"
authors: ["Gilad Gressel", "Rahul Pankajakshan", "Yisroel Mirsky"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2410.09569
doi: null
arxiv: "2410.09569"
cite: "Gressel, G., Pankajakshan, R., & Mirsky, Y. (2024). Are You Human? An Adversarial Benchmark to Expose LLMs. arXiv:2410.09569."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Releases a benchmark of text challenges to expose LLM impostors in real-time conversation. Implicit challenges exploit instruction following to cause role deviation; explicit challenges are simple tasks easy for humans and hard for LLMs. Across 9 leading LMSYS models, explicit challenges detected LLMs in 78.4% of cases and implicit ones in 22.9%; in user studies humans passed explicit challenges 78% of the time versus 22% for LLMs. The study also caught participants using LLMs.

## Contribution

Quantified reverse-Turing challenge benchmark with human baselines.

## Key results

- Explicit challenges detect LLMs in 78.4% of cases; implicit challenges 22.9% (abstract).
- Humans succeed on explicit challenges 78% vs LLMs 22% (abstract).
- Many study participants were found using LLMs to complete tasks (abstract).

## Methods and models

Challenge benchmark over 9 LMSYS models plus user studies.

## Limitations and open questions

Abstract-only reading; frontier-model capability drift will erode explicit challenges.

## Relevance to us

Usable as an interactive probe for suspected swarm accounts in DMs; the role-deviation (implicit) family overlaps with prompt-injection honeypots ([[reworr-2024-llm]]). Same group: [[chocron-2026-who]]. Predecessor: [[wang-2023-bot]].
