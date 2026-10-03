---
id: fang-2025-provably
type: paper
title: Provably Robust Federated Reinforcement Learning
authors:
- Minghong Fang
- Xilong Wang
- Neil Zhenqiang Gong
year: 2025
venue: The Web Conference 2025 (WWW 2025), per arXiv comment
url: https://arxiv.org/abs/2502.08123
doi: null
arxiv: '2502.08123'
cite: Fang, M., Wang, X., & Gong, N. Z. (2025). Provably Robust Federated Reinforcement Learning. The Web Conference 2025 (WWW 2025), per arXiv comment. arXiv:2502.08123.
topics:
- fork-merge-security
- marl-emergence
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Two contributions on federated reinforcement learning where some agents send poisoned policy updates. First, the Normalized attack: malicious agents craft updates that maximise the angle between the aggregated update before and after the attack (rather than its distance), which breaks Byzantine-robust aggregators including FedPG-BR. Second, an ensemble defence: agents are split deterministically into K non-overlapping groups by hashing their IDs, each group trains its own global policy with any aggregation rule, and at test time the K policies vote (majority for discrete actions, geometric median for continuous ones). Evaluated on CartPole, LunarLander and InvertedPendulum with 30 agents, 30% malicious and K = 5 groups by default, against four prior attacks and six aggregation rules. Read: abstract, introduction, threat model, attack and ensemble descriptions, both theorems as stated, parameter settings and the main experimental results; proofs and appendix figures not read.

## Contribution

Shows existing robust aggregation for federated RL can be beaten by a direction-aware attack, and gives a defence with a provable count threshold that does not depend on the aggregator being robust.

## Key results

- Normalized attack against non-ensemble aggregators: LunarLander Median reward fell from 219.3 (benign) to -33.3; CartPole FedPG-BR fell from 500 to 101.4; it was the only tested attack that substantially hurt FedPG-BR on all three tasks (measured).
- Ensemble defence: with robust rules inside groups, test reward under all attacks matched FedAvg without attack (for example FedPG-BR 500 and Trimmed-mean 1000 on InvertedPendulum under attack); tolerated 40% malicious agents on CartPole (measured, Figures 3-4).
- Proved (discrete actions): the ensemble's action at a state is unchanged if the number of malicious agents is at most floor((v(s,x) - v(s,y) - 1{y<x}) / 2), where v counts how many of the K group policies chose the top and runner-up actions; each malicious agent can flip at most one group (Theorem 1).
- Proved (continuous actions): the change in the predicted action is bounded while malicious agents control fewer than half of the groups (Theorem 2).
- FedAvg remained vulnerable even inside the ensemble (measured).

## Methods and models

Categorical and Gaussian MLP policies; attacker with full knowledge of the system by default; agent counts 30-90 with K = 5-9. The Web Conference 2025 (per arXiv comment).

## Limitations and open questions

The certified threshold depends on the vote margin at each state, which may be small; partitioning reduces the data per group and so each group's policy quality; test-time voting requires keeping K policies.

## Relevance to us

Q2: this is the most directly usable construction for dmarz's question. Instead of merging all parts into one parent (where one well-crafted update can steer a robust aggregator), keep K separately merged sub-parents built from disjoint groups of parts and decide by vote; then an attacker must corrupt enough parts to flip more than half the groups, and the paper proves the exact count. Q1: assignment of parts to groups by hashing IDs is deterministic but could be keyed with a secret, so an attacker would not know which parts share a group; the paper uses plain hashing, so the secret-keyed variant is an inference. Q3: the Normalized attack is a reminder that defences tuned to the magnitude of a returned update miss attacks on its direction. Related: [[fan-2021-fault-tolerant]], [[chen-2022-byzantine-robust]], [[ma-2023-local]].
