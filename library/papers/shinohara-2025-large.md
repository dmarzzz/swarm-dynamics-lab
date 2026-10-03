---
id: shinohara-2025-large
type: paper
title: Large Language Models as Particle Swarm Optimizers
authors:
- Yamato Shinohara
- Jinglue Xu
- Tianshui Li
- Hitoshi Iba
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2504.09247
doi: null
arxiv: '2504.09247'
cite: Shinohara, Y., Xu, J., Li, T., & Iba, H. (2025). Large language models as particle swarm optimizers. arXiv preprint arXiv:2504.09247. https://doi.org/10.48550/arXiv.2504.09247
topics:
- swarm-intelligence
- llm-agent-swarms
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Proposes Language Model PSO (LMPSO), where each particle's velocity is a prompt that asks an LLM to generate the next
candidate solution following PSO principles. Evaluated on the travelling salesman problem, heuristic improvement for
TSP and symbolic regression; effective mainly where solutions are structured sequences such as expressions or
programs, which standard PSO handles poorly.

## Contribution

Recent example of LLMs as variation operators inside a swarm-intelligence loop.

## Key results

- Claimed (abstract): effective on structured-sequence problems (numbers not read).

## Methods and models

PSO with LLM-generated updates encoded as prompts (abstract only).

## Limitations and open questions

Abstract-level reading; preprint; baselines and cost not checked.

## Relevance to us

Candidate baseline if the hackathon explores LLM agents performing swarm search; compare with [[feng-2024-model]]
and [[zhang-2025-swarmagentic]].
