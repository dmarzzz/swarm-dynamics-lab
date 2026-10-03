---
id: ju-2024-flooding
type: paper
title: Flooding Spread of Manipulated Knowledge in LLM-Based Multi-Agent Communities
authors:
- Tianjie Ju
- Yiting Wang
- Xinbei Ma
- Pengzhou Cheng
- Haodong Zhao
- Yulong Wang
- Lifeng Liu
- Jian Xie
- Zhuosheng Zhang
- Gongshen Liu
year: 2024
venue: arXiv preprint (Semantic Scholar lists Science China Information Sciences)
url: https://arxiv.org/abs/2407.07791
doi: null
arxiv: '2407.07791'
cite: 'Ju, T., Wang, Y., Ma, X., Cheng, P., Zhao, H., Wang, Y., Liu, L., Xie, J., Zhang, Z., & Liu, G. (2024). Flooding Spread of Manipulated Knowledge in LLM-Based Multi-Agent Communities. arXiv preprint arXiv:2407.07791.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 94 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Builds a threat model and simulation of a trusted multi-agent platform and a two-stage attack, Persuasiveness Injection followed by Manipulated Knowledge Injection, that makes agents spread counterfactual or toxic knowledge without explicit prompt manipulation and without degrading their general capabilities. The manipulated knowledge persists through retrieval-augmented generation when benign agents store and later retrieve the chat histories. The authors suggest guardian agents and fact-checking tools as defences.

## Contribution

Shows that a compromised agent can seed persistent misinformation in an agent community through ordinary conversation and shared memory.

## Key results

- Reported in abstract: attack induces spread of counterfactual and toxic knowledge without loss of foundational capability; persistence through RAG.

## Methods and models

Simulated multi-agent community on a trusted platform; two-stage injection; RAG memory.

## Limitations and open questions

Abstract only; the arXiv comment calls it work in progress, and the published version listed by Semantic Scholar was not checked.

## Relevance to us

Persistence through shared memory means a Sybil agent's influence outlives its session, and stored chat histories become apparent independent evidence later, the replication-as-corroboration failure in [[bara-2026-epistemic]]. [[hammond-2025-multi]] cites this paper when proposing immutable agent identifiers for detecting suspicious patterns. Related: [[lee-2024-prompt]], [[gu-2024-agent]].
