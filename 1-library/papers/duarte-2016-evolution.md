---
id: duarte-2016-evolution
type: paper
title: "Evolution of Collective Behaviors for a Real Swarm of Aquatic Surface Robots"
authors: ["Miguel Duarte", "Vasco Costa", "Jorge Gomes", "Tiago Rodrigues", "Fernando Silva", "Sancho Moura Oliveira", "Anders Lyhne Christensen"]
year: 2016
venue: "PLOS ONE"
url: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0151834
doi: "10.1371/journal.pone.0151834"
arxiv: null
cite: "Duarte, M., Costa, V., Gomes, J., Rodrigues, T., Silva, F., Oliveira, S. M., & Christensen, A. L. (2016). Evolution of Collective Behaviors for a Real Swarm of Aquatic Surface Robots. PLOS ONE, 11(3), e0151834."
topics: ["swarm-robotics"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "131 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Claimed as the first swarm with evolved control operating in a real, uncontrolled environment. Neural-network
controllers were evolved in simulation with NEAT for four canonical tasks (homing, dispersion, clustering,
area monitoring), then transferred without change to up to ten cheap aquatic surface robots in a 300 m x 190 m
waterbody connected to the Tagus river. Robots use GPS, a compass and Wi-Fi broadcasts of position (about once
per second, range about 40 m). Performance on the real robots was similar to simulation for most tasks, and the
controllers kept the scalability, flexibility and robustness expected of swarm control. A final run combines
several evolved behaviours into an environmental monitoring mission.

## Contribution

The field-deployment counterpoint to lab swarms and to the reality-gap pessimism in automatic design
([[francesca-2014-automode]], [[kuckling-2023-recent]]); a rare marine swarm in the library besides
[[berlinger-2021-implicit]].

## Key results

- Measured: homing, dispersion and monitoring controllers evolved within 100 generations; clustering needed up
  to 400 generations.
- Measured: dispersion with eight robots to a 20 m target distance; in simulation all controllers reached an
  error near 1 m, but on real robots only one of three reached an average error of 2 m. This is the clearest
  reality-gap case in the paper.
- Observed: real robots varied in speed much more than in simulation (motor power drops with battery level),
  and GPS readings were often wrong.
- Fitness used 10 simulation trials per controller and a safety coefficient that penalised robots closer
  than 3 m.

## Methods and models

NEAT with default parameters; JBotEvolver simulator (open source, GitHub), with a shared middle layer so the
same controller code runs in simulation and on the robots. Robots: small, inexpensive autonomous surface vessels
with GPS, compass and 802.11g ad hoc Wi-Fi (UDP broadcast).

## Limitations and open questions

At most ten robots; position comes from GPS broadcast, so this is not purely local sensing. Fitness design
was the main bottleneck for more complex tasks, as the authors admit. Read: abstract, methods, results
highlights.

## Relevance to us

Concrete, quantified numbers on the sim-to-real gap for evolved swarm controllers outdoors. Useful if the
hackathon considers evolved or learned controllers ([[ferrante-2015-evolution]], [[mattson-2025-discovery]]).
