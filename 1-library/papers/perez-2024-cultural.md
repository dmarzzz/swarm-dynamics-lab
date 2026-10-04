---
id: perez-2024-cultural
type: paper
title: "Cultural evolution in populations of Large Language Models"
authors:
- "Jérémy Perez"
- "Corentin Léger"
- "Marcela Ovando-Tellez"
- "Chris Foulon"
- "Joan Dussauld"
- "Pierre-Yves Oudeyer"
- "Clément Moulin-Frier"
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2403.08882
doi: null
arxiv: "2403.08882"
cite: "Perez, J., Léger, C., Ovando-Tellez, M., Foulon, C., Dussauld, J., Oudeyer, P.-Y., & Moulin-Frier, C. (2024). Cultural evolution in populations of large language models. arXiv preprint arXiv:2403.08882."
topics:
- llm-agent-swarms
- meta
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "2 (OpenAlex W4392866898, arXiv record, 2026-10-03)"
code: []
---

## Summary

Presents an open-source framework for simulating cultural evolution with populations of LLM agents, where the experimenter controls network structure, agent personality and how social information is aggregated and transformed at each transmission step. The motivation is to capture transformation biases of human cognition that formal cultural-evolution models handle poorly, and to study machine-generated culture for its own sake.

## Contribution

Brings the cultural-evolution toolkit (transmission chains, population structure, attractors) to LLM populations; a methods paper, with the follow-up telephone-game study (Perez et al. 2024, arXiv 2407.04503, not opened here) supplying the empirical results.

## Key results

- Framework paper; no headline quantitative result in the abstract.

## Methods and models

Multi-agent LLM transmission simulations over configurable networks, with a user interface. Code linked from the arXiv page.

## Limitations and open questions

No validation against human transmission-chain data in the abstract. Results will depend on model and prompt.

## Relevance to us

A ready simulation framework for information cascades and drift on networks, complementing [[tanaka-2026-when]] (memetic drift) and [[vallinder-2024-cultural]] (cultural evolution of cooperation).
