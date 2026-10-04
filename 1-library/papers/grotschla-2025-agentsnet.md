---
id: grotschla-2025-agentsnet
type: paper
title: 'AgentsNet: Coordination and Collaborative Reasoning in Multi-Agent LLMs'
authors:
- Florian Grötschla
- Luis Müller
- Jan Tönshoff
- Mikhail Galkin
- Bryan Perozzi
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2507.08616
doi: null
arxiv: '2507.08616'
cite: 'Grötschla, F., Müller, L., Tönshoff, J., Galkin, M., & Perozzi, B. (2025). AgentsNet: Coordination and Collaborative Reasoning in Multi-Agent LLMs. arXiv preprint arXiv:2507.08616.'
topics:
- llm-agent-swarms
- sync-consensus
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1 (OpenAlex, 2026-10-03); 37 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

AgentsNet is a benchmark that places LLM agents on the nodes of a network and asks them to solve classical distributed-computing and graph-theory problems through message passing over that network, measuring self-organisation, protocol formation and communication given the topology. Homogeneous agent networks must first agree on basic organisation and communication protocols. Some frontier LLMs do well on small networks but performance falls off as the network grows. Unlike most multi-agent benchmarks, which cover 2-5 agents, AgentsNet scales without a fixed limit, and the authors probe frontier models with up to 100 agents.

## Contribution

Connects LLM collectives to distributed algorithms (the tasks are local-communication problems where the topology matters), making it the closest LLM benchmark to the consensus/coordination tasks of networked control. Complements [[ruan-2025-benchmarking]] (spatial swarm tasks).

## Key results

- Claimed: strong performance on small networks for some frontier LLMs; degradation as network size grows.
- Claimed: experiments with up to 100 agents.

## Methods and models

LLM agents on graph nodes exchanging messages over rounds; tasks drawn from distributed systems and graph theory (specific problems not checked here).

## Limitations and open questions

Abstract-level read; which tasks break first with size and how this scales with graph diameter are open questions to check in the full text.

## Relevance to us

A ready benchmark for size-scaling experiments on fixed topologies; could be combined with small-world rewiring ([[wang-2025-rethinking]]). Related: [[tastan-2026-stochastic]], [[hirota-2026-collective]].

## Notes from dmarz/sim-envs

Code catalogued as [[gh-floriangroetschla-agentsnet]] and run on 2026-10-03 with local llama3.1 8B: 4-node colouring, 4 rounds, score 0.833 in 8.5 min. Needs Python 3.10+ and langchain 0.3 pins; see that entry's Run notes.
