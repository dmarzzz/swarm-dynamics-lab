---
id: suarez-2023-neural
type: paper
title: "Neural MMO 2.0: A Massively Multi-task Addition to Massively Multi-agent Learning"
authors: [Joseph Suárez, Phillip Isola, Kyoung Whan Choe, David Bloomin, Hao Xiang Li, Nikhil Pinnaparaju, Nishaanth Kanna, Daniel Scott, Ryan Sullivan, Rose S. Shuman, Lucas de Alcântara, Herbie Bradley, Louis Castricato, Kirsty You, Yuhao Jiang, Qimai Li, Jiaxin Chen, Xiaolong Zhu]
year: 2023
venue: Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track
url: https://arxiv.org/abs/2311.03736
doi: null
arxiv: '2311.03736'
cite: "Suárez, J., Isola, P., Choe, K. W., Bloomin, D., Li, H. X., Pinnaparaju, N., Kanna, N., Scott, D., Sullivan, R., Shuman, R. S., et al. (2023). Neural MMO 2.0: A massively multi-task addition to massively multi-agent learning. In Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track. arXiv:2311.03736."
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: null
code: [gh-neuralmmo-environment]
---

## Summary

Short platform paper for Neural MMO 2.0: a complete rewrite of the massively multi-agent MMO-style environment (128 agents in the standard setting, procedurally generated maps, foraging, NPCs, three combat styles, professions, items, equipment and a global market) whose new feature is a task system built from a vectorised GameState, float-valued Predicates and Tasks that can assign any agent rewards based on any group's state. The new engine runs about 3,000 agent steps per CPU core per second (up from about 800-1,000), measured with random actions and mortality removed.

## Contribution

Turns a fixed-objective many-agent world into a multi-task one where performance is redefined as executing novel tasks, aiming at generalisation, open-endedness and curriculum learning with academic-scale compute; contrasts itself with Melting Pot (set of scenarios) and XLand (closed, mostly two-agent).

## Key results

- About 3,000 agent-steps per CPU core per second, i.e. 5,000x real time per agent (one action = 0.6 s), about 250M agent steps or roughly 2.5 TB of observations per day per core at about 10 KB per observation.
- 25 built-in predicates; tasks can be per-agent, per-team, or assigned to one agent based on another's outcome (example: agent 1 rewarded when agent 2 is dead).
- Competition setting: users control 8 of 128 agents; prior competitions had 3,500+ submissions from 1,200+ users.
- Baselines: CleanRL PPO made compatible through PufferLib's multi-agent vectorisation; individual models trainable in about 8 A100 hours (checklist).

## Methods and models

Engine stores entire game state as flattened tensors (GameState) plus event datastores (hits, gathers) so predicates can query events cheaply. PettingZoo ParallelEnv API. MIT licence, pip package and container.

## Limitations and open questions

No new game mechanics beyond 1.x. In the previous competition top teams did not learn to use all systems and team specialisation stayed limited, which the authors attribute to an overly broad survival objective promoting dominant strategies. Team-based tasks were postponed because learning libraries could not handle them. No error bars in this paper (deferred to competition report).

## Relevance to us

Strongest laptop-runnable many-agent social world for our purposes; the cross-agent task assignment is the hook for collusion and Sybil experiments. We measured about 6,100-6,400 random-action agent-steps/s on an M1 Max without removing mortality, see [[gh-neuralmmo-environment]]. Builds on [[zheng-2018-magent]]-era many-agent gridworlds; compare [[leibo-2021-scalable]].
