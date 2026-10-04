---
id: kumar-2025-throttling
type: paper
title: "Throttling Web Agents Using Reasoning Gates"
authors: ["Abhinav Kumar", "Jaechul Roh", "Ali Naseh", "Amir Houmansadr", "Eugene Bagdasarian"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2509.01619
doi: "10.48550/arXiv.2509.01619"
arxiv: "2509.01619"
cite: "Kumar, A., Roh, J., Naseh, A., Houmansadr, A., & Bagdasarian, E. (2025). Throttling Web Agents Using Reasoning Gates. arXiv preprint arXiv:2509.01619."
topics: ["swarm-detection", "llm-agent-swarms", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "2 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Kumar, Roh, Naseh, Houmansadr and Bagdasarian propose Web Agent Throttling: gates that make an agent spend LLM tokens before it gets a resource. Existing coding or maths puzzles fail their criteria (asymmetric, scalable, robust, agent-agnostic), so they introduce rebus-based Reasoning Gates, synthetic text puzzles needing multi-hop world knowledge. Solving costs 9.2x more than generating for state-of-the-art models. They deploy the gates on a website and on MCP servers and test real web agents.

## Contribution

Cost imposition on the agent's model rather than detection: a proof-of-work analogue priced in inference tokens.

## Key results

- Measured (abstract): response-generation cost 9.2x the puzzle-generation cost for SOTA models.
- Deployed (abstract): custom website and MCP servers with real web agents; numbers not in abstract.

## Methods and models

Puzzle generation and verification protocol; evaluation of token costs; deployment. Abstract only.

## Limitations and open questions

Abstract only. Humans must also pass or bypass the gate; the authors discuss environmental cost. Cheap models or cached answers could lower the asymmetry (inference).

## Relevance to us

A Sybil-cost lever for agent swarms: each identity must pay tokens per access. Compare proof-of-work (Anubis) in [[fayolle-2026-internet]] and tarpits in [[jerkins-2026-penalizing]].
