---
id: castro-2024-modeling
type: paper
title: "Modeling collective behaviors from optic flow and retinal cues"
authors: ["Diego Castro", "Franck Ruffier", "Christophe Eloy"]
year: 2024
venue: "Physical Review Research"
url: https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.6.023016
doi: "10.1103/physrevresearch.6.023016"
arxiv: null
cite: "Castro, D., Ruffier, F., & Eloy, C. (2024). Modeling collective behaviors from optic flow and retinal cues. Physical Review Research, 6(2), 023016."
topics: [collective-motion, swarm-robotics]
added_by: dmarz/collective-motion-recent-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "17 (OpenAlex W4393932764, 2026-10-03)"
code: []
---

## Summary

Self-propelled-particle models usually assume each agent knows the positions and headings of its neighbours, although real animals may have neighbours hidden from view. The authors build a visual model in which each particle moves only according to bioplausible visual cues computed on its retina, in particular optic flow, with occlusion. The model reproduces the three classical collective states (swarming, schooling and milling) and is proposed as a basis for vision-only control of artificial swarms.

## Contribution

Part of the vision-based modelling line (Bastien and Romanczuk 2020 and after) but uses optic flow, a cue insects and fish demonstrably use, rather than only angular positions and sizes, which makes it directly transferable to camera-equipped robots.

## Key results

- Model (abstract): swarming, schooling and milling all emerge from optic-flow and retinal cues without omniscient neighbour knowledge.
- Claim: offers a route to visually controlled artificial swarms (not demonstrated on hardware in this paper).

## Methods and models

Agent-based visual model with retinal projection of neighbours and optic-flow based steering (details not read). Code: https://gitlab.com/FlokingByEyeDiego/flokingbyeye (link given on the article page; not opened).

## Limitations and open questions

Read at abstract level only; the parameter regimes, noise treatment and robustness to occlusion were not checked. No hardware validation in this paper.

## Relevance to us

A candidate controller for a vision-only swarm in our simulator. Compare with [[mezey-2025-purely]] (purely visual robots), [[krongauz-2024-vision]] (locust-inspired visual model), [[zheng-2024-body]] and [[xiao-2024-perception]] (salience-based neighbour selection).
