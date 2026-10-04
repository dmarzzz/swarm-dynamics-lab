---
id: werfel-2014-designing
type: paper
title: "Designing Collective Behavior in a Termite-Inspired Robot Construction Team"
authors: ["Justin Werfel", "Kirstin Petersen", "Radhika Nagpal"]
year: 2014
venue: "Science"
url: https://doi.org/10.1126/science.1245842
doi: "10.1126/science.1245842"
arxiv: null
cite: "Werfel, J., Petersen, K., & Nagpal, R. (2014). Designing Collective Behavior in a Termite-Inspired Robot Construction Team. Science, 343(6172), 754–758."
topics: [swarm-robotics, swarm-intelligence]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "610 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

The TERMES system solves an inverse problem in collective construction: a user specifies a target 3D
structure, and the system automatically compiles low-level rules for independent climbing robots that are
guaranteed to produce that structure. Robots use only local sensing and coordinate through the shared
environment (stigmergy), as mound-building termites do. A physical realisation with three autonomous climbing
robots using only onboard sensing builds structures from specialised bricks.

## Contribution

A rare example of top-down design with a correctness guarantee in swarm robotics: from global goal to
provably correct local rules, with stigmergy as the coordination channel. Pairs with
[[rubenstein-2014-programmable]] as the two 2014 Science papers that defined the Nagpal lab's agenda.

## Key results

- Claimed with proof: compiled rules guarantee the specified structure (from abstract).
- Measured: three physical climbing robots built structures using onboard sensing only.

## Methods and models

Target structure compiled offline into local movement and placement rules for climbing robots that sense only
locally and coordinate through the partially built structure. Abstract read only (Europe PMC); compilation
details not checked.

## Limitations and open questions

Small physical team; speed and robustness to robot failures at scale not checked here.

## Relevance to us

Reference for stigmergy-based coordination in robots; see [[salman-2024-automatic]] for automatically designed
stigmergy and the swarm-intelligence topic for algorithmic stigmergy.

## Notes from dmarz/swarm-robotics-audit

Checked the abstract (OpenAlex record) and the Crossref metadata (Science 343(6172), 754-758). The summary and the three-robot claim match the abstract. No corrections.
