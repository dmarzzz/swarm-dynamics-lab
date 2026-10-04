---
id: brambilla-2013-swarm
type: paper
title: "Swarm robotics: a review from the swarm engineering perspective"
authors: ["Manuele Brambilla", "Eliseo Ferrante", "Mauro Birattari", "Marco Dorigo"]
year: 2013
venue: "Swarm Intelligence"
url: https://link.springer.com/article/10.1007/s11721-012-0075-2
doi: "10.1007/s11721-012-0075-2"
arxiv: null
cite: "Brambilla, M., Ferrante, E., Birattari, M., & Dorigo, M. (2013). Swarm robotics: a review from the swarm engineering perspective. Swarm Intelligence, 7(1), 1–41."
topics: [swarm-robotics, collective-decision, collective-motion]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "1783 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

The most cited review of swarm robotics. It reads the literature through the lens of "swarm engineering", the
systematic modelling, design, realisation, verification, validation, operation and maintenance of robot
swarms, and proposes two taxonomies: one of design and analysis methods (behaviour-based versus automatic
design; microscopic versus macroscopic modelling; real-robot analysis) and one of collective behaviours
(spatial organisation such as aggregation, pattern formation and self-assembly; navigation such as
exploration, coordinated motion and transport; collective decision-making split into consensus achievement and
task allocation). It closes with the field's limits as an engineering discipline and research directions.

## Contribution

Set the canonical vocabulary and categories for the field; later reviews ([[valentini-2017-best]],
[[schranz-2020-swarm]], [[dorigo-2020-reflections]]) and most swarm-robotics papers adopt its split into
consensus achievement versus task allocation and behaviour-based versus automatic design.

## Key results

- Taxonomy of design methods: behaviour-based (probabilistic finite-state machines, virtual physics) and
  automatic (evolutionary robotics, reinforcement learning).
- Taxonomy of analysis: microscopic models, macroscopic models (rate equations, Fokker-Planck), real robots.
- Taxonomy of collective behaviours as above. These are organisational results rather than measurements.
- Highlights that real-world swarm applications were essentially absent as of 2012.

## Methods and models

Narrative review of roughly a decade of swarm robotics literature. I read only the publisher abstract; the
taxonomy categories listed here are as cited and used by [[valentini-2017-best]], which I read in full.

## Limitations and open questions

Predates drone swarms, learning-based controllers and robotic active matter. The authors argue that the lack of
principled top-down design methods is the main barrier to applications.

## Relevance to us

The starting map for any survey on swarm robotics. Use its taxonomy to structure our survey and to place
hackathon ideas. Cross-links: [[sahin-2005-swarm]] (earlier definition), [[hamann-2018-swarm]] (formal
methods), [[francesca-2014-automode]] (automatic design), [[martinoli-2004-modeling]] (micro-macro modelling).
