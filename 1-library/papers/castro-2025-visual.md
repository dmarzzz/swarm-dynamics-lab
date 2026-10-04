---
id: castro-2025-visual
type: paper
title: "Visual collective behaviors on spherical robots"
authors: ["Diego Castro", "Christophe Eloy", "Franck Ruffier"]
year: 2025
venue: "Bioinspiration & Biomimetics"
url: https://arxiv.org/abs/2409.20539
doi: "10.1088/1748-3190/adaab9"
arxiv: "2409.20539"
cite: "Castro, D., Eloy, C., & Ruffier, F. (2025). Visual collective behaviors on spherical robots. Bioinspiration & Biomimetics, 20(2), 026006."
topics: [swarm-robotics, collective-motion]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "3 (OpenAlex W4406412213, 2026-10-03); 3 (Crossref, 2026-10-03)"
code: []
---

## Summary

A visual flocking model that uses only panoramic visual cues (retinal position, optical size and optic flow of neighbours), in the spirit of [[bastien-2020-model]], is run 'robot-in-the-loop' on a flock of 10 independent spherical robots. A virtual anchor confines the group away from walls. The robots reproduce several collective-motion phases, notably swarming and milling, and behaviour is nearly identical in simulation and physical experiments with the same model.

## Contribution

A physical test of vision-only collective-motion models showing phase reproduction and close sim-to-real agreement.

## Key results

- Swarming and milling phases reproduced with 10 spherical robots using only visual cues (measured).
- Nearly identical behaviour between simulation and robot-in-the-loop experiments (claimed).

## Methods and models

Visual interaction model with retinal position, optical size and optic flow; robot-in-the-loop setup with external computation of visual fields (inferred from 'robot-in-the-loop'; not checked).

## Limitations and open questions

Abstract-depth entry. Robot-in-the-loop means perception may be emulated rather than onboard. N = 10.

## Relevance to us

Complements fully onboard vision-based flocking ([[mezey-2025-purely]]) and vision-based fault tolerance ([[shefi-2025-bugs]]).
