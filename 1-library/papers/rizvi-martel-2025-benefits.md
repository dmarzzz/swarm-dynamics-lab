---
id: rizvi-martel-2025-benefits
type: paper
title: Benefits and Limitations of Communication in Multi-Agent Reasoning
authors:
- Michael Rizvi-Martel
- Satwik Bhattamishra
- Neil Rathi
- Guillaume Rabusseau
- Michael Hahn
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2510.13903
doi: null
arxiv: '2510.13903'
cite: Rizvi-Martel, M., Bhattamishra, S., Rathi, N., Rabusseau, G., & Hahn, M. (2025). Benefits and Limitations of Communication in Multi-Agent Reasoning. arXiv preprint arXiv:2510.13903 (revised July 2026).
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 0 (OpenAlex, 2026-10-03); 9 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A theoretical framework for the expressivity of multi-agent LLM systems that split long-context problems into shorter sub-problems. Applied to three algorithmic families (state tracking, recall and k-hop reasoning), it derives bounds on the number of agents needed to solve a task exactly, on the quantity and structure of inter-agent communication, and on achievable speedups as problem size and context grow. It identifies regimes where communication is provably beneficial, trade-offs between agent count and bandwidth, and intrinsic limits when either is constrained. Controlled synthetic experiments with pretrained LLMs confirm the predicted trade-offs.

## Contribution

One of the few formal (complexity-theoretic) results on how many agents and how much communication a task needs; complements empirical scaling work ([[kim-2025-towards]], [[bertalanic-2026-ringelmann]]).

## Key results

- Theory: bounds on agents required, communication volume/structure, and speedups for state tracking, recall and k-hop reasoning.
- Measured: synthetic-benchmark experiments agree with predicted trade-offs.

## Methods and models

Formal model of communicating transformer agents; synthetic tasks; pretrained LLM experiments. Specific bounds not checked.

## Limitations and open questions

Abstract-level read; algorithmic tasks, not open-ended coordination.

## Relevance to us

Offers a theory of agent-count vs bandwidth trade-off that a swarm experiment could probe. Related: [[tran-2026-single]], [[fukushima-2026-message]].
