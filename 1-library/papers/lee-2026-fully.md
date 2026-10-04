---
id: lee-2026-fully
type: paper
title: Fully Byzantine-Resilient Multi-Agent Reinforcement Learning
authors:
- Haejoon Lee
- Dimitra Panagou
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.25701
doi: null
arxiv: '2609.25701'
cite: Lee, H., & Panagou, D. (2026). Fully Byzantine-Resilient Multi-Agent Reinforcement Learning. arXiv preprint. arXiv:2609.25701.
topics:
- fork-merge-security
- marl-emergence
- sync-consensus
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Studies decentralized actor-critic multi-agent reinforcement learning in which agents with private rewards reach consensus on shared critic and team-reward parameters over a time-varying graph, under "Byzantine edge attacks": an adversary may arbitrarily alter or drop at most F messages per time step, but every agent is assumed honest (Assumption 2). The method, FRAC-MARL, has each agent relay what it hears so that every message arrives along several two-hop paths; an agent accepts a neighbour's parameters only if the most frequent copy appears at least tau times, then averages over the accepted set. Read: introduction, problem setup, attack model, method, the redundancy definitions and lemmas, simulation results and conclusion; proofs not checked.

## Contribution

Upgrades the guarantee in Byzantine-resilient MARL from convergence to a neighbourhood of the attack-free solution (trimmed mean, projection, geometric median) to almost-sure convergence to the same limit points as with no attack, under a new graph condition, (r, r')-redundancy, that can be verified in polynomial time, whereas the commonly used (2F+1)-robustness is coNP-complete to verify.

## Key results

- Theorem-level (proved, linear function approximation): if the graph is (r, r-2F-1)-redundant with r > 2F, the filtered communication graph stays connected and undirected and all Byzantine-altered messages are filtered, so parameters converge almost surely to the attack-free limits.
- A constructive procedure produces such graphs; (2F+1, 0)-redundant graphs are also (2F+1)-robust.
- Simulation, 10 agents forming a circle in MPE2, F = 1 and F = 2, five seeds, 10,000 episodes: FRAC-MARL's reward curve matched the attack-free baseline, while trimmed-mean and projection defences converged to visibly lower rewards (measured, Figure 3; small neural networks rather than linear critics).
- The introduction summarises prior results: a single adversarial agent can destabilise cooperative MARL, and learning optimal policies is generally impossible with Byzantine agents (cited, not re-measured).

## Methods and models

Consensus-based AC-MARL of Zhang et al. 2018 as the base algorithm; two message rounds per step (send, relay); mode-count filter with threshold tau. Attack in simulation: positive offsets added to parameters on F edges incident to one agent. Code at github.com/joonlee16/frac-marl.

## Limitations and open questions

Only the communication layer is adversarial; a corrupted agent that sends the same wrong value to all neighbours would pass a redundancy check, so the exact-recovery result does not cover compromised agents. Needs enough path redundancy (r > 2F) and two message rounds per step.

## Relevance to us

Q2: gives a precise threshold of the kind dmarz asked about, but for corrupted channels, not corrupted parts. If the risk is that a child's report is tampered with on the way back (the hostile network between the child and the parent), sending the same returned update through at least 2F+1 independent relays and accepting only the majority copy recovers the uncorrupted merge exactly. If the child itself is corrupted, this paper's own summary of the literature says only neighbourhood guarantees are known, and exact recovery is generally impossible. That split (channel adversary gets exact recovery, agent adversary gets bounded damage at best) is the main Q2 answer from the RL side. Related: [[fan-2021-fault-tolerant]], [[alistarh-2018-byzantine]], [[he-2025-red]] (channel adversary for LLM agents).
