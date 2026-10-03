---
id: jimenez-romero-2025-multi-agent
type: paper
title: 'Multi-agent systems powered by large language models: applications in swarm intelligence'
authors:
- Cristian Jimenez-Romero
- Alper Yegenoglu
- Christian Blum
year: 2025
venue: Frontiers in Artificial Intelligence
url: https://arxiv.org/abs/2503.03800
doi: 10.3389/frai.2025.1593017
arxiv: '2503.03800'
cite: 'Jimenez-Romero, C., Yegenoglu, A., & Blum, C. (2025). Multi-agent systems powered by large language models: applications in swarm intelligence. Frontiers in Artificial Intelligence, 8, 1593017. https://doi.org/10.3389/frai.2025.1593017'
topics:
- llm-agent-swarms
- swarm-intelligence
- collective-motion
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 29 (OpenAlex, journal record, 2026-10-03); 55 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

The authors replace the hard-coded rules of agents in two classic swarm-intelligence models, ant colony foraging and bird flocking, with prompts to GPT-4o, using a toolchain that connects NetLogo to the OpenAI API through NetLogo's Python extension. At each tick an agent's local environmental state is turned into a prompt and the LLM returns its action. Two prompting styles are compared: structured, rule-based prompts that restate the classical rules, and autonomous, knowledge-driven prompts that let the model decide from its own knowledge. The paper demonstrates that both styles can produce self-organising foraging and flocking-like behaviour and presents the toolchain as a way to study emergent behaviour with LLM agents.

## Contribution

An early, reproducible bridge between the NetLogo agent-based-modelling tradition and LLM agents for the canonical swarm models, published in a journal with code and data. Precedes the benchmark of [[ruan-2025-benchmarking]] and the cost critique of [[rahman-2025-llm-powered]].

## Key results

- Claimed: LLM-driven ants reproduce pheromone-mediated foraging dynamics and LLM-driven birds produce flocking-like alignment under both prompt styles.
- Claimed: rule-based prompts give behaviour closer to the classical models; knowledge-driven prompts produce more varied behaviour.
- Quantitative comparisons not checked at abstract level.

## Methods and models

NetLogo simulations (ant foraging, flocking) with per-agent GPT-4o calls via the NetLogo Python extension; structured vs autonomous prompts. Code and data: https://github.com/crjimene/swarm_gpt .

## Limitations and open questions

Abstract-level read. Single model (GPT-4o), small swarms implied by API cost; no order-parameter analysis reported in the abstract.

## Relevance to us

Directly reusable infrastructure if the team wants NetLogo-based LLM swarms; a baseline for "does an LLM reproduce Boids". Related: [[zomer-2026-unraveling]], [[li-2024-challenges]], [[strobel-2024-llm2swarm]].
