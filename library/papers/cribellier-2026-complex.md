---
id: cribellier-2026-complex
type: paper
title: "The complex swarming dynamics of malaria mosquitoes emerge from simple minimally-interactive behavioral rules"
authors: ["Antoine Cribellier", "Bèwadéyir Serge Poda", "Roch K. Dabiré", "Abdoulaye Diabaté", "Olivier Roux", "Florian T. Muijres"]
year: 2026
venue: "PLOS Computational Biology"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC13529247/
doi: "10.1371/journal.pcbi.1014685"
arxiv: null
cite: "Cribellier, A., Poda, B. S., Dabiré, R. K., Diabaté, A., Roux, O., & Muijres, F. T. (2026). The complex swarming dynamics of malaria mosquitoes emerge from simple minimally-interactive behavioral rules. PLOS Computational Biology, 22(8), e1014685."
topics: [collective-motion, criticality-measurement]
added_by: dmarz/collective-motion-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "0 (OpenAlex W7204260007, 2026-10-03)"
code: []
---

## Summary

Re-analyses two published lab datasets of 3D flight tracks of male Anopheles coluzzii mating swarms (Poda et al. 2024 and Feugère et al. 2022) formed above a ground marker under a simulated sunset. Individuals alternate straight flight with rapid saccadic turns that are triggered at the swarm edge and biased along the sunset axis, and the same kinematics appear when a male swarms alone. An agent-based model with three rules, attraction to the region above the marker and alignment with the sunset axis (both environmental) plus short-range collision avoidance (the only social rule), reproduces looping paths, central density peaks and directional alignment, so social attraction and alignment are not needed to produce a stable swarm.

## Contribution

A parsimonious counter-model to the view that insect swarms follow boids-style social rules: the apparent correlations between mosquitoes can be produced by shared responses to environmental cues. Extends the midge-swarm debate (Kelley and Ouellette; Attanasi et al.) to mosquitoes with an explicit generative model.

## Key results

- Measured: saccades concentrated at the swarm boundary; turn directions biased along the sunset direction; consistent across both datasets and in single-male swarms.
- Measured: swarm sizes in the Poda dataset from 1 to 26 simultaneous males (comparable to modal field swarm sizes).
- Model: environmental attraction + environmental alignment + collision avoidance reproduces density, acceleration-toward-axis and looping features; collision avoidance events are rare and only at < 2.5 body lengths.
- Claim (authors' interpretation): long-range 'interactions' reported in mosquito and midge swarms may be simultaneous responses to external cues.

## Methods and models

Stereo near-infrared videography (Basler acA2040-90umNIR, 2048 x 2048 px, 50 fps) and 3D track reconstruction from the original studies. Kinematic analysis of straight flight versus saccades; agent-based model where agents fly straight, sample the marker viewing angle, and on predicted boundary crossing perform a saccade whose azimuth and climb are drawn from measured distributions. Model compared in detail to the Poda dataset and broadly to the Feugère dataset.

## Limitations and open questions

Lab swarms only, small to medium sizes (up to about 26); the authors say field confirmation is needed. Boundary treated as a binary threshold, so spatial zones are sharper than in data. Absence of need for social rules is not evidence of their absence (acoustic male-female interactions are not modelled). Read at skim depth.

## Relevance to us

A clean null model for any claim that a swarm's order comes from social interaction: shared environmental cues can mimic it. Pairs with [[gupta-2024-mosquitoes]] (same system, sensory basis of short-range avoidance and mate tracking) and contrasts with fish and bird work such as [[puy-2024-selective]] and [[zheng-2024-body]]; relevant to the extended-criticality claims for insect swarms in [[gonzalez-albaladejo-2024-power]].
