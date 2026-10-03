---
id: ma-2023-local
type: paper
title: Local Environment Poisoning Attacks on Federated Reinforcement Learning
authors:
- Evelyn Ma
- Praneet Rathi
- S. Rasoul Etesami
year: 2023
venue: arXiv preprint (v4, January 2024)
url: https://arxiv.org/abs/2303.02725
doi: null
arxiv: '2303.02725'
cite: Ma, E., Rathi, P., & Etesami, S. R. (2023). Local Environment Poisoning Attacks on Federated Reinforcement Learning. arXiv preprint (v4, January 2024). arXiv:2303.02725.
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Studies poisoning of federated reinforcement learning, where several agents train locally in their own copies of an environment for 50 steps per round and a server averages their policy (and critic) parameters with FedAvg. A malicious agent cannot touch the environment or other agents; it perturbs the rewards it trains on, within a budget epsilon, choosing the perturbation by solving an optimisation that makes its submitted parameters push the global policy toward low global reward (untargeted) or toward a target policy (targeted). For actor-critic learners it keeps a private critic trained on true rewards and a public critic trained on poisoned ones. Read: abstract, introduction, the attack description, the experimental settings, the main results text and the conclusion; the theorem was read as stated, and the appendix with the defence and proportion experiments was not read.

## Contribution

Shows that a single malicious participant can poison averaged federated RL through its local environment alone, with a proof that the attack strictly lowers the global objective under the stated assumptions.

## Key results

- With a single attacker among three or four agents and budget epsilon = 1, global reward under the proposed attack was significantly lower than clean training and than a random reward-noise attack, over 200 rounds, on CartPole, InvertedPendulum, Hopper, LunarLander and HalfCheetah (measured, Figures 1-2).
- Against PPO the attack was more effective than against vanilla policy gradient, while random reward noise was overwhelmed by the honest agents (measured).
- The authors report that the proportion of malicious agents, rather than system size, determines success, and propose a performance-based credit defence (stated; results in the appendix, not read).
- Theorem 1: under FedAvg and smoothness assumptions, the poisoning strictly decreases the global objective (proved).

## Methods and models

VPG and PPO local learners; FedAvg aggregation; untargeted and targeted variants; private and public critics for actor-critic. Venue not stated on the arXiv page (v4, January 2024).

## Limitations and open questions

Small federations (3-4 agents), so one attacker is 25-33%; plain averaging, no robust aggregation evaluated in the main text.

## Relevance to us

Q3: closest measured analogue to a corrupted part that returns a policy update rather than raw experience. The part did not need to falsify anything it sent; it trained honestly on rewards it had distorted locally, then submitted the resulting parameters, which a parameter-level outlier check would see as an ordinary update. Q2: with plain averaging one in three or four parts sufficed; the authors' finding that the malicious proportion is what matters is consistent with Byzantine-style thresholds, which robust aggregators such as [[fan-2021-fault-tolerant]] enforce and FedAvg does not. Related: [[rakhsha-2020-policy]], [[chen-2022-byzantine-robust]].
