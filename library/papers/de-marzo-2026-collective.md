---
id: de-marzo-2026-collective
type: paper
title: 'Collective Behavior of AI Agents: the Case of Moltbook'
authors:
- Giordano De Marzo
- David Garcia
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2602.09270
doi: null
arxiv: '2602.09270'
cite: 'De Marzo, G., & Garcia, D. (2026). Collective behavior of AI agents: The case of Moltbook. arXiv preprint arXiv:2602.09270.'
topics:
- llm-agent-swarms
- criticality-measurement
- swarm-detection
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex W7128614415, arXiv record, 2026-10-03); Semantic Scholar 14 same day
code: []
---

## Summary

Large-scale data analysis of Moltbook, a Reddit-style platform populated only by AI agents: over 369,000 posts and 3.0 million comments from about 46,000 active agents. AI collective behaviour shows statistical regularities familiar from human online communities: heavy-tailed activity distributions, power-law scaling of popularity metrics, and temporal decay consistent with limited attention. A key difference is a sublinear relation between upvotes and discussion size, unlike human behaviour.

## Contribution

The first observational ("in the wild") study of a large deployed population of interacting AI agents, with heavy-tail and scaling analyses of the kind used for human and animal collectives.

## Key results

- 46,000 agents, 369,000 posts, 3.0 million comments analysed (abstract).
- Heavy tails and power-law popularity scaling; sublinear upvote-discussion relation (abstract; exponents not read).

## Methods and models

Platform data analysis; distribution fitting; temporal decay analysis. Code not checked.

## Limitations and open questions

Observational, uncontrolled population (unknown models and prompts); abstract-level read.

## Relevance to us

Real-world counterpart to controlled simulations ([[yang-2024-oasis]], [[piao-2025-agentsociety]]); suggests scaling exponents a hackathon could compare against simulated LLM swarms.

## Notes from dmarz/sd-coordination

Read the arXiv abstract this session. Population-level statistics (369k posts, 3.0M comments, about 46k agents) of the agent-only platform Moltbook. For coordination detection, the companion dataset is [[mukherjee-2026-moltgraph]], which measures coordination episodes on the same platform and finds one X handle linked to 2,328 agents.

## Notes from dmarz/sd-code-data

This lane catalogued the same source independently (added_by dmarz/llm-agent-swarms, accessed 2026-10-03). Its distinct content:

### Notes from dmarz/sd-code-data

Tagged swarm-detection. Moltbook is now the main in-the-wild agent-population testbed for detection: coordination episodes and weak spam labels in [[mukherjee-2026-moltgraph]] / [[data-moltgraph-2026]], a timing fingerprint separating human-steered from autonomous agents in [[li-2026-moltbook]] (15.3% autonomous, 54.8% human-influenced; four accounts made 32% of comments), and open archives [[data-moltbook-observatory-2026]] and [[data-moltbook-takschdube-2026]].
