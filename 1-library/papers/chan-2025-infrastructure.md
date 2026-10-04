---
id: chan-2025-infrastructure
type: paper
title: Infrastructure for AI Agents
authors:
- Alan Chan
- Kevin Wei
- Sihao Huang
- Nitarshan Rajkumar
- Elija Perrier
- Seth Lazar
- Gillian K. Hadfield
- Markus Anderljung
year: 2025
venue: Transactions on Machine Learning Research (TMLR)
url: https://arxiv.org/abs/2501.10114
doi: null
arxiv: '2501.10114'
cite: 'Chan, A., Wei, K., Huang, S., Rajkumar, N., Perrier, E., Lazar, S., Hadfield, G. K., & Anderljung, M. (2025). Infrastructure for AI Agents. Transactions on Machine Learning Research. arXiv:2501.10114.'
topics:
- sybil-resistance
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 53 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proposes "agent infrastructure": technical systems and shared protocols external to agents that mediate their interactions with environments and each other, by analogy with HTTPS for the web. Identifies three functions: attributing actions and properties to specific agents, users or legal entities; shaping agent interactions (communication protocols, agreements); and detecting and remedying harmful actions. Gives an incomplete catalogue of research directions with use cases, adoption paths, relation to existing internet infrastructure, limits and open questions.

## Contribution

Generalises the identifier proposals of [[chan-2024-ids]] and [[chan-2024-visibility]] into a research agenda in which attribution is one of three infrastructure functions.

## Key results

- No empirical results (abstract-level read).

## Methods and models

Conceptual research agenda.

## Limitations and open questions

Abstract only; I did not check how deeply the catalogue treats Sybil identity creation.

## Relevance to us

Attribution infrastructure is the precondition for both reputation ([[xia-2026-when]]) and provenance-aware aggregation ([[bara-2026-epistemic]]) in agent collectives. [[hammond-2025-multi]] cites this paper as the frame for normative infrastructure among agents.
