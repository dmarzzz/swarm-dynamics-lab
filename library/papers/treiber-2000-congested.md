---
id: treiber-2000-congested
type: paper
title: Congested traffic states in empirical observations and microscopic simulations
authors:
- Martin Treiber
- Ansgar Hennecke
- Dirk Helbing
year: 2000
venue: Physical Review E
url: https://arxiv.org/abs/cond-mat/0002177
doi: 10.1103/physreve.62.1805
arxiv: cond-mat/0002177
cite: Treiber, M., Hennecke, A., & Helbing, D. (2000). Congested traffic states in empirical observations and microscopic simulations. Physical Review E, 62(2), 1805–1824. https://doi.org/10.1103/physreve.62.1805
topics:
- crowds-and-traffic
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 4254 (Crossref, 2026-10-03)
code: []
---

## Summary

Presents German freeway detector data showing several kinds of congestion near road inhomogeneities (lane closures, intersections, uphill gradients): localised or extended, homogeneous or oscillating, and coexisting combinations. Introduces the intelligent driver model (IDM), a continuous single-lane car-following model, and shows that with empirical boundary conditions it reproduces all observed states when inhomogeneities are represented as local parameter changes.

## Contribution

Introduced the IDM, which became the default car-following model in traffic simulation, adaptive cruise control design and mixed-autonomy RL environments ([[wu-2022-flow]]). Also supports a phase diagram of congested states near bottlenecks.

## Key results

- Observed (abstract): coexistence of moving localised clusters and pinned clusters; oscillating congestion upstream of homogeneous congestion.
- Simulated: a local drop of road capacity via parameter change acts practically like an on-ramp.

## Methods and models

Empirical loop-detector data plus simulation; PRE 62, 1805–1824.

## Limitations and open questions

Deterministic single-lane model; later work adds noise and multi-lane behaviour. Abstract-level read only; the model equations were not checked in this session.

## Relevance to us

The standard "human driver" agent for any vehicle-swarm simulation. Its string instability above critical density is what [[sugiyama-2008-traffic]] demonstrates and [[stern-2018-dissipation]] suppresses.
