---
id: lin-2026-beyond
type: paper
title: 'Beyond Memory Majority: Latent-Source Reasoning for Multi-Agent Memory Arbitration'
authors:
- Chenchen Lin
- Wenhao Yuan
- Xuehe Wang
- Edith Cheuk Han Ngai
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2608.19701
doi: null
arxiv: '2608.19701'
cite: 'Lin, C., Yuan, W., Wang, X., & Ngai, E. C. H. (2026). Beyond Memory Majority: Latent-Source Reasoning for Multi-Agent Memory Arbitration. arXiv preprint arXiv:2608.19701.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

Long-running multi-agent systems accumulate memories written by different agents, and existing memory methods combine retrieved memories by voting or weighting as if they were independent evidence. Memories from different agents often inherit the same upstream source or bias, so correlated evidence is counted repeatedly and forms a false majority; the authors call this Memory Correlation Bias. CAMA (Correlation-Aware Memory Arbitration) groups retrieved memories, estimates the effective number of independent sources by combining neural dependency inference with provenance-based symbolic priors, and learns a sequential policy that retrieves alternative evidence or traces upstream sources before deciding. The abstract reports gains over state-of-the-art baselines in suppressing false majorities.

## Contribution

Names the failure of majority voting over agent memories that share a source, and proposes arbitration by effective number of independent sources rather than headcount.

## Key results

- Reported in abstract: CAMA beats baselines on several benchmarks and suppresses false majorities from correlated memories. No numbers in the abstract; not checked.

## Methods and models

Query-conditioned evidence groups, neural dependency inference, provenance priors, learned retrieval policy. Only the abstract was read.

## Limitations and open questions

Abstract-level reading; threat model (benign correlation versus adversarial injection) not checked.

## Relevance to us

Q2 and Q3, closely matched to the merge step. When sub-agents return and their memories are pooled into the parent, the parent faces exactly this arbitration problem. An attacker who corrupts one shared upstream source (a page, a tool output) can make several honest sub-agents write the same false memory, producing a manufactured majority with zero sub-agents compromised. Counting effective independent sources, with provenance carried through the fork, is the defence direction; it requires each sub-agent to record where each memory came from. Related: [[narang-2026-inference]], [[kim-2025-correlated]], [[bara-2026-epistemic]].
