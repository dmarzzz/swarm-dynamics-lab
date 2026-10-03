---
id: li-2023-camel
type: paper
title: 'CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society'
authors:
- Guohao Li
- Hasan Abed Al Kader Hammoud
- Hani Itani
- Dmitrii Khizbullin
- Bernard Ghanem
year: 2023
venue: Advances in Neural Information Processing Systems 36 (NeurIPS 2023)
url: https://arxiv.org/abs/2303.17760
doi: null
arxiv: '2303.17760'
cite: 'Li, G., Hammoud, H. A. A. K., Itani, H., Khizbullin, D., & Ghanem, B. (2023). CAMEL: Communicative agents for "mind" exploration of large language model society. Advances in Neural Information Processing Systems 36 (NeurIPS 2023). arXiv:2303.17760.'
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "101 (OpenAlex W4362508448, arXiv record, 2026-10-03); Semantic Scholar 1950 same day"
code: []
---

## Summary

CAMEL proposes "role-playing": two LLM agents (an AI user and an AI assistant) are given roles and a task through "inception prompting" and then cooperate autonomously by conversation, with minimal human input. The framework is used to generate large conversational datasets for studying cooperative behaviour among communicative agents, and the library is open-sourced.

## Contribution

One of the first multi-agent LLM frameworks and the origin of the "agent society" framing; established role-based prompting as a coordination mechanism.

## Key results

- Role-playing sustains autonomous multi-turn cooperation on tasks while staying consistent with the human-specified goal (abstract claim).
- Generated datasets of agent conversations for analysis of cooperative behaviour (abstract claim).

## Methods and models

Two-agent role-playing with inception prompts and a task specifier agent; ChatGPT-era models. Code: https://github.com/camel-ai/camel (linked from the arXiv page).

## Limitations and open questions

Two-agent dyads; known failure modes include role flipping, repetition and infinite loops (described in the paper). Not a population-dynamics study.

## Relevance to us

Background. The same group later built OASIS ([[yang-2024-oasis]]), which scales the idea to a million agents.
