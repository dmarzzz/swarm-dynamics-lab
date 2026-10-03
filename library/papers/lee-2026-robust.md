---
id: lee-2026-robust
type: paper
title: Robust Multi-Agent LLMs under Byzantine Faults
authors:
- Haejoon Lee
- Vincent-Daniel Yun
- Dimitra Panagou
- Sai Praneeth Karimireddy
year: 2026
venue: EMNLP 2026 (Main), accepted per arXiv comment
url: https://arxiv.org/abs/2605.09076
doi: null
arxiv: '2605.09076'
cite: 'Lee, H., Yun, V.-D., Panagou, D., & Karimireddy, S. P. (2026). Robust Multi-Agent LLMs under Byzantine Faults. arXiv preprint arXiv:2605.09076. Accepted to EMNLP 2026 (Main).'
topics:
- sybil-resistance
- llm-agent-swarms
- sync-consensus
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 10 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proposes Self-Anchored Consensus (SAC), a fully decentralised filter-and-refine protocol for LLM agents on peer-to-peer graphs: agents exchange responses, locally evaluate and filter unreliable messages, and refine their own outputs. The authors give (F+1)-robustness conditions on the communication graph under which honest agents preserve and propagate reliable information despite Byzantine neighbours. Across open- and closed-weight LLMs on mathematical and commonsense reasoning benchmarks and several topologies, SAC suppresses Byzantine influence while prior methods degrade under attack.

## Contribution

Brings graph-robustness conditions of the kind used in resilient consensus for networked control (my inference from the (F+1)-robustness framing) to LLM agent networks.

## Key results

- Reported in abstract: SAC consistently improves performance across topologies under Byzantine attack; prior methods degrade significantly. Numbers not checked.

## Methods and models

Iterative local filtering and refinement; (F+1)-robustness graph conditions; reasoning benchmarks.

## Limitations and open questions

Abstract only. Robustness is stated in terms of F Byzantine neighbours per agent, so a Sybil attacker who inserts many nodes adjacent to a target breaks the condition; topology control is therefore the Sybil defence.

## Relevance to us

The networked-control route to Byzantine and Sybil robustness in swarms, directly comparable to the leaderless geometric-median approach of [[jo-2025-byzantine]]. It cites [[jo-2025-byzantine]] and connects to the robot-swarm literature in [[strobel-2023-robot]]. Graph-robustness conditions give a concrete parameter to vary in swarm simulations.
