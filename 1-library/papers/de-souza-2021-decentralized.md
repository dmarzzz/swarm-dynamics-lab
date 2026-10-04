---
id: de-souza-2021-decentralized
type: paper
title: Decentralized Multi-Agent Pursuit Using Deep Reinforcement Learning
authors:
- Cristino de Souza
- Rhys Newbury
- Akansel Cosgun
- Pedro Castillo
- Boris Vidolov
- Dana Kulić
year: 2021
venue: IEEE Robotics and Automation Letters
url: https://arxiv.org/abs/2010.08193
doi: 10.1109/LRA.2021.3068952
arxiv: '2010.08193'
cite: de Souza, C., Newbury, R., Cosgun, A., Castillo, P., Vidolov, B., & Kulić, D. (2021). Decentralized multi-agent pursuit using deep reinforcement learning. IEEE Robotics and Automation Letters, 6(3), 4552–4559.
topics:
- marl-emergence
- swarm-robotics
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 180 (Crossref, 2026-10-03)
code: []
---

## Summary

Homogeneous pursuers with unicycle constraints learn, from shared experience, a policy executed independently by each agent to capture an omnidirectional evader. Training uses curriculum learning, a sweeping-angle ordering of neighbours, and rewards mixing individual and group terms. With up to eight pursuers against a reactive evader, the learned non-holonomic policy matches classical algorithms run with omnidirectional agents and beats their non-holonomic adaptations; a three-drone real-world demonstration is shown.

## Contribution

Extends the pursuit-evasion line of [[huttenrauch-2019-deep]] toward hardware and benchmarks it against classical geometric pursuit strategies.

## Key results

- Learned policy on par with classical omnidirectional strategies and better than their non-holonomic versions (claimed in abstract, simulation, up to 8 pursuers).
- Proof-of-concept transfer to three motion-constrained drones.

## Methods and models

Parameter-shared deep RL, curriculum, angular ordering of neighbour observations, combined individual and group reward. Abstract-level read.

## Limitations and open questions

Single evader with a fixed reactive strategy; small teams.

## Relevance to us

Pursuit-evasion is a common hackathon task; this gives classical baselines to compare against. Related: [[batra-2022-decentralized]], [[li-2023-predator]].
