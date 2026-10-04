---
id: nisan-2026-domination-avoiding
type: paper
title: "Domination-Avoiding Learning Agents Cannot Collude"
authors: ["Noam Nisan", "Emmanuel Zerah"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.01275
doi: null
arxiv: "2606.01275"
cite: "Nisan, N., & Zerah, E. (2026). Domination-Avoiding Learning Agents Cannot Collude. arXiv preprint arXiv:2606.01275."
topics: [agent-budgets, marl-emergence]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

A theory paper responding to [[calvano-2020-artificial]] and [[fish-2024-algorithmic]]. It proves that external-regret-minimising agents can collude in a natural pricing market, then defines Domination-Avoiding agents (including all mean-based agents, internal-regret minimisers and multiplicative-weights agents with variable learning rate) and proves they cannot collude there. In any game, such agents jointly learn to almost never play strategies removed by iterated elimination of strictly dominated strategies.

## Contribution

A sharp theoretical line between learning rules that can and cannot collude.

## Key results

- Proved (abstract): external-regret minimisers can collude; Domination-Avoiding agents provably do not.

## Methods and models

Theory; abstract read only.

## Limitations and open questions

Applies to formal learning algorithms; LLM agents are not obviously in either class. Abstract only.

## Relevance to us

Gives a principled non-colluding baseline firm for the swarm factory (e.g. an internal-regret learner), useful as a control against which LLM firm behaviour is compared.
