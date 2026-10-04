---
id: fachada-2026-can
type: paper
title: "Can Large Language Models Implement Agent-Based Models? An ODD-based Replication Study"
authors: ["Nuno Fachada", "Daniel Fernandes", "Carlos M. Fernandes", "João P. Matos-Carvalho"]
year: 2026
venue: "Ecological Modelling"
url: https://arxiv.org/abs/2602.10140
doi: "10.1016/j.ecolmodel.2026.111624"
arxiv: '2602.10140'
cite: "Fachada, N., Fernandes, D., Fernandes, C. M., & Matos-Carvalho, J. P. (2026). Can large language models implement agent-based models? An ODD-based replication study. Ecological Modelling. https://doi.org/10.1016/j.ecolmodel.2026.111624"
topics: [meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "2 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Evaluates 17 LLMs on translating the full ODD specification of the PPHPC predator-prey model into self-contained Python. Each model got six generations under one fixed prompt; outputs went through staged checks (syntax, execution, output interface) and then model-independent statistical comparison against a validated NetLogo baseline under two parameter sets, plus runtime and static code-quality metrics.

## Contribution

First systematic ODD-to-code replication benchmark for LLMs with statistical output validation, separating executability from behavioural faithfulness.

## Key results

- GPT-4.1 was the only model to produce statistically valid implementations in all six trials; Claude 3.7 Sonnet in 4 of 6; Mistral Large, Grok 3, DeepSeek-R1 and DeepSeek-V3 only intermittently.
- No locally run open-weight model produced a statistically validated implementation, though several produced runnable code.
- Among valid implementations, runtime varied by orders of magnitude and code complexity varied widely, so correctness, efficiency and maintainability are distinct axes.

## Methods and models

PPHPC model (well-documented, replicated since 2015); 17 LLMs as of July 2025; temperature-sampled six trials per model; validation against NetLogo outputs; radon static metrics.

## Limitations and open questions

Authors note: one model only, possible training-data exposure to PPHPC descriptions, six trials, one prompt, two parameter sets, no expert Python baseline. Read discussion, limitations and conclusions, not the full tables.

## Relevance to us

Lesson for agent-built sims: code that runs is not code that reproduces the model; require statistical comparison against a reference (or invariants) before trusting an LLM-written simulator. Forward citation of [[grimm-2020-odd]]; complements [[he-2026-visa]] and [[blando-2026-towards]].
