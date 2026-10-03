---
id: savoie-2019-robot
type: paper
title: "A robot made of robots: Emergent transport and control of a smarticle ensemble"
authors: ["William Savoie", "Thomas A. Berrueta", "Zachary Jackson", "Ana Pervan", "Ross Warkentin", "Shengkai Li", "Todd D. Murphey", "Kurt Wiesenfeld", "Daniel I. Goldman"]
year: 2019
venue: "Science Robotics"
url: https://doi.org/10.1126/scirobotics.aax4316
doi: "10.1126/scirobotics.aax4316"
arxiv: null
cite: "Savoie, W., Berrueta, T. A., Jackson, Z., Pervan, A., Warkentin, R., Li, S., Murphey, T. D., Wiesenfeld, K., & Goldman, D. I. (2019). A robot made of robots: Emergent transport and control of a smarticle ensemble. Science Robotics, 4(34), eaax4316."
topics: [swarm-robotics, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "95 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Smarticles are individually immotile, periodically deforming robots. Enclosed in a ring (a "supersmarticle"),
they diffuse collectively through stochastic mechanical interactions. The authors show experimentally and
theoretically that inactivating individual smarticles produces directed drift of the whole ensemble, use this
for endogenous phototaxis, and build a data-driven model of the activity-to-transport map from a single
experimental trial that lets them steer the supersmarticle anywhere in the plane with decentralised
closed-loop control.

## Contribution

Shows control of a collective whose input-output relation is stochastic and emergent, the experimental partner
to the rattling theory in [[chvykov-2021-low]].

## Key results

- Directed drift by deactivating individual smarticles (measured); phototaxis demonstrated.
- Control model fitted from one experimental trial enables steering anywhere in the plane (claimed in
  abstract).

## Methods and models

Three-link smarticles with two servo-driven arms, confined in a ring; numerical modelling of activity versus
transport. Abstract read.

## Limitations and open questions

Small ensembles; enclosure required; performance metrics not checked.

## Relevance to us

A minimal collective where control emerges from mechanical interactions; a template for "control a swarm
through a few switches". See [[li-2019-particle]].
