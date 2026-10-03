---
id: ceron-2024-reciprocal
type: paper
title: Reciprocal and Non-Reciprocal Swarmalators with Programmable Locomotion and Formations for Robot Swarms
authors: [Steven Ceron, Wei Xiao, Daniela Rus]
year: 2024
venue: 2024 IEEE International Conference on Robotics and Automation (ICRA)
url: https://api.openalex.org/works/doi:10.1109/icra57147.2024.10610540
doi: 10.1109/icra57147.2024.10610540
arxiv: null
cite: "Ceron, S., Xiao, W., & Rus, D. (2024). Reciprocal and non-reciprocal swarmalators with programmable locomotion and formations for robot swarms. In 2024 IEEE International Conference on Robotics and Automation (ICRA) (pp. 12233-12239). IEEE."
topics: [sync-consensus, swarm-robotics, active-matter]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "6 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Uses a general swarmalator model to study reciprocal and non-reciprocal interactions (agents exerting unequal
attractive and repulsive forces on each other) over long and short ranges. Non-reciprocal coupling is used to
make the collective locomote toward or away from target sites, and control barrier functions are used to
optimise the non-reciprocal couplings so that the swarm reaches a desired spatial formation.

## Contribution

Turns swarmalators from a descriptive model into a programmable controller: on-demand, agent-specific coupling
gains steer emergent behaviour. Links the non-reciprocal active-matter line ([[fruchart-2021-non]]) with
safety-critical control (control barrier functions) for robot swarms.

## Key results

- Abstract-level: non-reciprocal coupling produces directed collective locomotion; CBF optimisation yields
  desired formations; behaviours shown in simulation with claimed potential for macro- and micro-scale robots.

## Methods and models

Generalised 2D swarmalator model with pairwise asymmetric coupling; control barrier function optimisation.
Abstract from OpenAlex; full text not read.

## Limitations and open questions

Appears to be simulation-only (hardware follow-up is [[beattie-2025-realizing]]); not verified.

## Relevance to us

Closest prior work to any hackathon idea of "steering a swarmalator swarm with a few tunable couplings";
check it before proposing such a hypothesis.
