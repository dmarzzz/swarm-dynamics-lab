---
id: gh-sunblaze-ucb-fedagent
type: code
title: 'FedAgent: federated reinforcement learning of LLM agents across decentralized clients (NeurIPS 2026)'
repo: sunblaze-ucb/FedAgent
url: https://github.com/sunblaze-ucb/FedAgent
authors: [Canyu Chen, Kangyu Zhu, Zhaorun Chen, Zhanhui Zhou, Shizhe Diao, Yiping Lu, Tian Li, Manling Li, Dawn Song]
year: 2025
language: Python
license: Apache-2.0
stars: 17
last_commit: 2026-09-27
topics: [fork-merge-security, marl-emergence]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

FedAgent trains LLM agents with RL (PPO, GRPO) on separate clients that keep their own data and periodically aggregates their checkpoints with FedAvg (optional client-side FedProx), on top of stock verl 0.8. It accompanies "Is Decentralized LLM Agent RL Robust to Heterogeneity? An Asymmetric Tale" (NeurIPS 2026; authors and abstract from the project page fed-agent.github.io). The abstract reports that federated agent training matches centralized training under uniform clients and beats local-only training, and derives an "asymmetric robustness" result: it is robust to task-level heterogeneity (what clients ask the agent to do) but worst-case non-robust to environment-level heterogeneity (the dynamics the agent acts in), with three sufficient conditions that restore robustness. The repository ships 176 paper configs on WebShop and ALFWorld, accelerated variants, and a single-H100 recipe measured at roughly 17 to 55 minutes per round for Qwen2.5-1.5B.

## What it can do for us

This is the nearest working system to Sutton's split-and-merge for agents: copies of one agent go into different environments, learn, and are merged back into one set of weights. Its central negative result bears on all three questions even before an adversary appears. Children sent to genuinely different environments (another country's web) produce updates that FedAvg cannot merge robustly, so the honest spread of returned updates is wide, which is exactly where robust aggregators lose power (Q2) and where an attacker's update can hide (Q3, as in ALIE [[baruch-2019-little]]). The heterogeneity suite (holdout and lookalike environments) could be reused to place one adversarial environment among honest ones and swap FedAvg for a Byzantine-robust rule from [[gh-lpd-epfl-byzfl]].

## Run notes

Not run. Needs GPUs (H100 class per the README recipes) and verl; each paper cell is one command documented in the README.

## Limitations

No adversarial clients in the README; robustness here means robustness to heterogeneity, not to Byzantine faults. FedAvg is the only aggregation rule I saw documented. Heavy compute.
