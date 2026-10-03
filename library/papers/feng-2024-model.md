---
id: feng-2024-model
type: paper
title: 'Model Swarms: Collaborative Search to Adapt LLM Experts via Swarm Intelligence'
authors:
- Shangbin Feng
- Zifeng Wang
- Yike Wang
- Sayna Ebrahimi
- Hamid Palangi
- Lesly Miculicich
- Achin Kulshrestha
- Nathalie Rauschmayr
- Yejin Choi
- Yulia Tsvetkov
- Chen-Yu Lee
- Tomas Pfister
year: 2024
venue: International Conference on Machine Learning (ICML 2025)
url: https://arxiv.org/abs/2410.11163
doi: null
arxiv: '2410.11163'
cite: 'Feng, S., Wang, Z., Wang, Y., Ebrahimi, S., Palangi, H., Miculicich, L., Kulshrestha, A., Rauschmayr, N., Choi, Y., Tsvetkov, Y., et al. (2025). Model swarms: Collaborative search to adapt LLM experts via swarm intelligence. International Conference on Machine Learning (ICML 2025). arXiv:2410.11163.'
topics:
- llm-agent-swarms
- swarm-intelligence
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "2 (OpenAlex W4403573463, arXiv record, 2026-10-03); Semantic Scholar 34 same day"
code: []
---

## Summary

Model Swarms treats a pool of LLM expert checkpoints as particles that move collaboratively in weight space, guided by the best-found checkpoints (a particle-swarm-optimisation-style search), to optimise a utility function for adaptation. It is tuning-free, works with as few as 200 examples, and improves over 12 model-composition baselines by up to 21.0% across single tasks, multi-task domains, reward models and human interests; experts can discover capabilities absent from the initial checkpoints (weak-to-strong transitions).

## Contribution

Uses swarm intelligence (PSO) on LLM weights rather than LLM agents in a swarm, an inversion worth distinguishing.

## Key results

- Up to 21.0% over 12 baselines (abstract).
- Works with about 200 examples (abstract).

## Methods and models

PSO-like velocity updates over model parameter vectors with personal-best and global-best guidance. Code not checked.

## Limitations and open questions

Requires same-architecture checkpoints; compute for weight-space search. Abstract-level read.

## Relevance to us

Relevant to topic swarm-intelligence as an application of PSO to LLMs; not about agent interaction dynamics.
