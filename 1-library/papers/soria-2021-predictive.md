---
id: soria-2021-predictive
type: paper
title: "Predictive control of aerial swarms in cluttered environments"
authors: ["Enrica Soria", "Fabrizio Schiano", "Dario Floreano"]
year: 2021
venue: "Nature Machine Intelligence"
url: https://doi.org/10.1038/s42256-021-00341-y
doi: "10.1038/s42256-021-00341-y"
arxiv: null
cite: "Soria, E., Schiano, F., & Floreano, D. (2021). Predictive control of aerial swarms in cluttered environments. Nature Machine Intelligence, 3(6), 545–554."
topics: [swarm-robotics, collective-motion, sync-consensus]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "169 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Classical swarm models express coordinated motion as the sum of local potential-field interactions. These fail
to guarantee fast and safe motion for aerial swarms in cluttered real environments (forests, urban areas) and
need tuning to each scenario. The authors embed the local principles of potential-field models in the objective of a model predictive
controller that uses knowledge of agent
dynamics and the environment. The predictive swarm moves faster, more orderly and more safely than the reactive
one, is independent of the environment layout, and scales with swarm speed and inter-agent distance. Validated
with five quadrotors flying among obstacles indoors.

## Contribution

A clean head-to-head between reactive (Reynolds/Vicsek-style) and predictive (MPC) swarm control using the same
behavioural principles, positioned between [[vasarhelyi-2018-optimized]] and planning-based swarms
([[zhou-2022-swarm]]).

## Key results

- Simulated: improvements in speed, order and safety over potential-field models; layout independence;
  scalability in speed and spacing (from abstract; numbers not checked).
- Measured: five quadrotors navigate an obstacle-filled indoor environment.

## Methods and models

Predictive (MPC-style) controller whose objective encodes potential-field swarm principles, using agent
dynamics and environment knowledge. Abstract read; formulation details not checked.

## Limitations and open questions

Small real swarm; computational load per agent grows with horizon and neighbours (not checked).

## Relevance to us

If a project compares rule-based and optimisation-based collective motion, this is the reference design.
