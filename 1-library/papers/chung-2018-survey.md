---
id: chung-2018-survey
type: paper
title: "A Survey on Aerial Swarm Robotics"
authors: ["Soon-Jo Chung", "Aditya Avinash Paranjape", "Philip Dames", "Shaojie Shen", "Vijay Kumar"]
year: 2018
venue: "IEEE Transactions on Robotics"
url: https://doi.org/10.1109/tro.2018.2857475
doi: "10.1109/tro.2018.2857475"
arxiv: null
cite: "Chung, S.-J., Paranjape, A. A., Dames, P., Shen, S., & Kumar, V. (2018). A Survey on Aerial Swarm Robotics. IEEE Transactions on Robotics, 34(4), 837–855."
topics: [swarm-robotics, sync-consensus, collective-motion]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "685 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

A control- and estimation-centred review of aerial swarms. It argues that aerial swarms differ from ground
swarms in operating in 3D and in having vehicle dynamics that add a layer of complexity, and it reviews dynamic
modelling, stability and controllability conditions, then the main algorithmic layers usually organised
hierarchically: trajectory generation and formation control, task allocation, adversarial control, distributed
sensing, monitoring and mapping, showing where the physics of aerial robots enters each.

## Contribution

The standard engineering reference for aerial swarms, complementary to the biology-inspired flocking line
([[vasarhelyi-2018-optimized]]) and the swarm-intelligence line ([[brambilla-2013-swarm]]).

## Key results

- Organises aerial swarm autonomy as a hierarchy from vehicle control up to mission-level allocation (review
  claim).
- Notes falling hardware costs as the driver of aerial swarm research.

## Methods and models

Literature survey with control-theoretic framing (consensus, formation control, distributed estimation). Abstract
only read.

## Limitations and open questions

Written before onboard-perception swarms in clutter ([[zhou-2022-swarm]]) and learned policies became common.

## Relevance to us

Use for control-theory vocabulary and as the bridge to the sync-consensus topic ([[olfati-saber-2006-flocking]],
[[ren-2007-information]]).
