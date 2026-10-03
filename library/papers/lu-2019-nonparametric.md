---
id: lu-2019-nonparametric
type: paper
title: "Nonparametric inference of interaction laws in systems of agents from trajectory data"
authors: ["Fei Lu", "Ming Zhong", "Sui Tang", "Mauro Maggioni"]
year: 2019
venue: "Proceedings of the National Academy of Sciences"
url: https://arxiv.org/abs/1812.06003
doi: "10.1073/pnas.1822012116"
arxiv: "1812.06003"
cite: "Lu, F., Zhong, M., Tang, S., & Maggioni, M. (2019). Nonparametric inference of interaction laws in systems of agents from trajectory data. Proceedings of the National Academy of Sciences, 116(29), 14424–14433."
topics: [swarm-detection, collective-motion, criticality-measurement]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "140 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Proposes a nonparametric statistical learning estimator for distance-based interaction kernels in systems of interacting agents, without assuming the functional form, from observed trajectories. Gives theoretical guarantees and tests on particle systems, opinion dynamics, prey-predator models, flocking and swarming, and cell phototaxis, with homogeneous and heterogeneous agents.

## Contribution

The reference method for recovering interaction rules from trajectories, applicable when agents' states can be observed over time.

## Key results

- Learns interaction laws without assuming their analytic form, with theoretical guarantees, on systems from physics to opinion dynamics (abstract; error rates not in abstract).

## Methods and models

Statistical learning of distance-based interaction kernels from sampled trajectories, scalable to large datasets (abstract). Estimator details not read.

## Limitations and open questions

Abstract only. Assumes a known model class (pairwise, distance-based interactions) and dense trajectories. Online agents have sparse event data, not continuous states.

## Relevance to us

The physics-side tool for "is there hidden coupling between these agents, and what rule". For agent swarms in opinion or embedding space, an estimated kernel that is non-zero between accounts would be coupling evidence. Related existing entries: [[katz-2011-inferring]], [[lord-2016-inference]]; social-media analogue [[sharma-2021-identifying]].
