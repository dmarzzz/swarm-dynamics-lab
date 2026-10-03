---
id: wang-2021-emergent
type: paper
title: "Emergent Field-Driven Robot Swarm States"
authors: ["Gao Wang", "Trung V. Phan", "Shengkai Li", "Michael Wombacher", "Junle Qu", "Yan Peng", "Guo Chen", "Daniel I. Goldman", "Simon A. Levin", "Robert H. Austin", "Liyu Liu"]
year: 2021
venue: "Physical Review Letters"
url: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1103/PhysRevLett.126.108002?fields=title,abstract
doi: "10.1103/PhysRevLett.126.108002"
arxiv: null
cite: "Wang, G., Phan, T. V., Li, S., Wombacher, M., Qu, J., Peng, Y., Chen, G., Goldman, D. I., Levin, S. A., Austin, R. H., & Liu, L. (2021). Emergent Field-Driven Robot Swarm States. Physical Review Letters, 126(10), 108002."
topics: [swarm-robotics, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "72 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

An ecology-inspired active-matter system: robots move over a large LED array that represents a dynamic resource
field. Each robot climbs the local light-intensity gradient and depletes (dims) the light where it sits, while
the field recovers over time. This self-generated "field drive" produces dynamic and spatial states resembling
gas, crystal, liquid, glass and jammed phases, depending on robot density, consumption rate and recovery rate.

## Contribution

A clean experimental phase diagram for robots coupled through a shared, consumable environment field, which is
stigmergy viewed as active matter.

## Key results

- Measured: gas-, crystal-, liquid-, glass- and jammed-like states as functions of density, consumption and
  recovery rates.
- Counter-intuitive: non-gas states emerge from smooth, flat resource landscapes rather than rough ones; any
  state can go directly to a glassy state if the recovery rate is slow enough, at any density.

## Methods and models

Robots with light sensors on an LED array that updates intensity according to robot positions (consumption) and
recovery. Abstract read.

## Limitations and open questions

Single platform; theory of the transitions not checked.

## Relevance to us

Excellent hackathon toy model: a few parameters, rich phases, easy to simulate. Connects to stigmergy
([[salman-2024-automatic]], [[werfel-2014-designing]]) and to resource-consumer models.
