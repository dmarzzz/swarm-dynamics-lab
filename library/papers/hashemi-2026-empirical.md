---
id: hashemi-2026-empirical
type: paper
title: An Empirical Study of Collective Behaviors and Social Dynamics in Large Language
  Model Agents
authors:
- Farnoosh Hashemi
- Michael W. Macy
year: 2026
venue: arXiv
url: https://export.arxiv.org/api/query?id_list=2602.03775
doi: null
arxiv: '2602.03775'
cite: Farnoosh Hashemi; Michael W. Macy. (2026). An Empirical Study of Collective
  Behaviors and Social Dynamics in Large Language Model Agents. arXiv:2602.03775.
topics:
- llm-agent-swarms
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

The authors analyze one year of Chirper.ai interactions to investigate homophily, influence, toxic language, ideology, and polarization among LLM agents. The abstract reports seven million posts from 32,000 agents and proposes Chain of Social Thought reminders to reduce harmful posting.

## Contribution

A one-year observational study of 7M posts by 32K LLM agents on Chirper.ai measuring homophily, influence, toxicity and polarization, plus a prompt-level intervention.

## Key results

- Seven million posts and interactions among 32K agents over one year.

## Methods and models

Longitudinal observational social-network analysis and Chain of Social Thought intervention.

## Limitations and open questions

Platform findings do not establish human-equivalent social mechanisms or a replicated universal effect; intervention effect sizes are absent from the abstract.

## Relevance to us

One of the largest observed LLM-agent social datasets; a natural comparison corpus for any agent-society metric we propose, alongside the Moltbook studies [[hou-2026-structural]] and [[li-2026-socialization]].

## Access provenance

Opened the HTTPS arXiv export record and read its abstract on 2026-10-03. No citation count inferred from an absent or mismatched index record.

## Notes from shadow/sol-1

Read on 2026-10-03 from arXiv HTML (https://arxiv.org/html/2602.03775): sections 1 to 7. Depth for this note: skim of methods and results.

- Data: Chirper.ai English posts April 2023 to May 2024, 32K active agents, 7M posts and 1M+ interactions; agents are memory-enhanced and receive a "backstory" prompt (4,805 have none). Non-reciprocal follow network.
- Homophily: agents in the same follow community are 1.22 times more similar than random pairs; at link creation agents are 1.91 times more likely to follow similar agents.
- Influence: post-backstory similarity declines over time; neighbour similarity grows about 6x over a year of connection, including for agents with no backstory, which the authors read as consistent with social influence (observational, not causal).
- Polarisation: bimodal stance toward "humans"; political subgraph of 1,988 agents (1,678 liberal, 310 conservative) has polarisation 0.78 versus 0.33 to 0.42 for human networks, but lower assortativity (0.13 vs 0.58). A "Chain of Social Thought" prompt cuts harmful posting by up to 42%.
- Relevance: a year-long, multi-agent, memory-enabled population, so the AI Village is not the only longitudinal population. What remains distinctive about the Village is task orientation, multiple frontier models acting with tools, and live human perturbation.
