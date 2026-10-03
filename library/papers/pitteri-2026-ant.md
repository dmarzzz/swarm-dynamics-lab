---
id: pitteri-2026-ant
type: paper
title: Ant swarm functional control via stigmergic Reinforcement Learning agents
authors:
- Alessio Pitteri
- Andrea Guizzo
- Laura Ferrarotti
- Bruno Lepri
- Riccardo Gallotti
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2607.17709
doi: null
arxiv: '2607.17709'
cite: Pitteri, A., Guizzo, A., Ferrarotti, L., Lepri, B., & Gallotti, R. (2026). Ant swarm functional control via stigmergic reinforcement learning agents. arXiv preprint arXiv:2607.17709.
topics:
- marl-emergence
- swarm-intelligence
- criticality-measurement
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

A population of controlling agents, trained with CTDE reinforcement learning, acts only on the shared pheromone field of an ant swarm model, never on the ants directly. Rewards favour trail pheromone structures and alignment of ants with high-pheromone paths, without prescribing microscopic configurations. The learned policies shift the phase-transition line of the ant model, producing trails in parameter regimes normally dominated by randomness.

## Contribution

Shows learned controllers moving an order-disorder transition of a classic collective model, a direct link between MARL control and the phase-transition view of collectives; analogous in spirit to [[falk-2021-learning]] for active matter.

## Key results

- Learned stigmergic controllers shift the phase transition line and induce trails in otherwise disordered regimes (claimed in abstract).

## Methods and models

Ant swarm model with pheromone field; controller agents trained with centralised training and decentralised execution; reward on trail structure and ant alignment. Abstract-level read.

## Limitations and open questions

Very recent preprint; ant model specifics and robustness not checked.

## Relevance to us

Template for "learn to steer a collective across its phase transition" projects. Related: [[falk-2021-learning]], [[shaw-2020-formic]], [[cao-2022-pool]].
