---
id: zomer-2026-unraveling
type: paper
title: Unraveling the emergence of collective behavior in networks of cognitive agents
authors:
- Nicola Zomer
- Manlio De Domenico
year: 2026
venue: npj Artificial Intelligence
url: https://www.nature.com/articles/s44387-026-00091-5
doi: 10.1038/s44387-026-00091-5
arxiv: null
cite: Zomer, N., & De Domenico, M. (2026). Unraveling the emergence of collective behavior in networks of cognitive agents. npj Artificial Intelligence, 2(1), 36. https://doi.org/10.1038/s44387-026-00091-5
topics:
- llm-agent-swarms
- swarm-intelligence
- collective-decision
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 1 (OpenAlex, 2026-10-03); 7 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

The authors compare "cognitive agents" (LLM-driven) with classical rule-following particles on two canonical collective tasks. First, LLM Agent Swarm Optimization (llmASO): a swarm of interacting LLM agents acts as an optimiser in the manner of particle swarm optimisation (PSO). Individual LLM agents make better local decisions than PSO particles, but their consensus tendency and pattern exploitation make the swarm prone to premature convergence; changing the network topology mitigates this but usually at the cost of slower convergence than classical PSO. Second, the Schelling segregation model: with local interactions and homophily, LLM agents generate emergent behaviours distinct from the rule-based model, so communication architecture matters for social simulation.

## Contribution

A direct, controlled comparison of LLM agents against the classical particle baselines of swarm intelligence and complexity science, published in a Nature-family venue. Complements [[jimenez-romero-2025-multi-agent]] (LLM ants and boids in NetLogo) and [[rahman-2025-llm-powered]] (LLM Boids/ACO cost).

## Key results

- Claimed: LLM agents outperform particles in individual decisions but swarms converge prematurely due to consensus tendencies.
- Claimed: network topology adjustments alleviate premature convergence but slow convergence relative to PSO.
- Claimed: LLM agents in the Schelling model produce distinct emergent segregation patterns under local, homophilic interaction.

## Methods and models

llmASO (LLM agents exchanging positions/values on a communication network over benchmark functions) vs PSO; LLM-driven Schelling model on a grid. Models, network types and quantitative results not checked at abstract level.

## Limitations and open questions

Abstract-level read. Quantitative gaps vs PSO (iterations, function evaluations, cost) need the full text.

## Relevance to us

High: the cleanest "LLM swarm vs particle swarm" benchmark; premature convergence through conformity echoes [[weng-2025-do]] and [[cho-2025-herd]]. Candidate for a hackathon replication with cheaper models. Related: [[de-wynter-2026-population]] (also uses Schelling).
