---
id: zheng-2026-survey
type: paper
title: A survey on large language models driven meta-optimizers for automated intelligent optimization
authors: [Yan Zheng, Lida Zhang, Kaiwen Li, Rui Wang, Wenhua Li, Tao Zhang, Qingfu Zhang, Yaochu Jin]
year: 2026
venue: Artificial Intelligence Review
url: https://api.openalex.org/works/W7118307887
doi: 10.1007/s10462-025-11470-w
arxiv: null
cite: Zheng, Y., Zhang, L., Li, K., Wang, R., Li, W., Zhang, T., Zhang, Q., & Jin, Y. (2026). A survey on large language models driven meta-optimizers for automated intelligent optimization. Artificial Intelligence Review, 59(2), 72. https://doi.org/10.1007/s10462-025-11470-w
topics: [swarm-intelligence, llm-agent-swarms]
added_by: dmarz/swarm-intelligence-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 10 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Review of large language models used as meta-optimisers, that is, as designers and controllers of optimisation
heuristics rather than as the optimiser itself. Defines the paradigm and scope, organises methods by stage
(automatic algorithm generation, dynamic algorithm selection, parameter configuration, mutation/operator control),
collects evaluation metrics and benchmark problems, and lists challenges and future directions.

## Contribution

The first review in the library on LLM-designed metaheuristics, the 2024-2026 direction that sits next to the
swarm-intelligence algorithms here. It frames the scan's LLM-swarm entries ([[shinohara-2025-large]],
[[zhang-2025-swarmagentic]]) as instances of a broader "LLM as meta-optimiser" programme.

## Key results

- Claimed (abstract): a unified framework and taxonomy for LLM-driven meta-optimisation; a summary of metrics and
  benchmarks; open challenges. No experiments (survey).

## Methods and models

Literature review; Springer full text was behind a login redirect during this audit, so the named methods, benchmark
lists and paper counts were not read.

## Limitations and open questions

Unread beyond the abstract. The field it surveys inherits the benchmarking problems of metaheuristics (centre bias,
weak baselines; [[kudela-2022-critical]], [[vermetten-2024-large]]) plus LLM-specific ones (contamination, cost).

## Relevance to us

Useful for any hackathon idea that has an LLM agent swarm design or tune a swarm optimiser. Bridges
`swarm-intelligence` and `llm-agent-swarms`; see also [[feng-2024-model]].
