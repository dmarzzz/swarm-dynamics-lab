---
id: corbetta-2023-physics
type: paper
title: Physics of Human Crowds
authors:
- Alessandro Corbetta
- Federico Toschi
year: 2023
venue: Annual Review of Condensed Matter Physics
url: https://iris.cnr.it/retrieve/07d667df-aece-412f-9970-162332c75da7/annurev-conmatphys-031620-100450.pdf
doi: 10.1146/annurev-conmatphys-031620-100450
arxiv: null
cite: Corbetta, A., & Toschi, F. (2023). Physics of Human Crowds. Annual Review of Condensed Matter Physics, 14(1), 311–333. https://doi.org/10.1146/annurev-conmatphys-031620-100450
topics:
- crowds-and-traffic
- active-matter
- collective-motion
- criticality-measurement
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: 66 (Crossref, 2026-10-03)
code: []
---

## Summary

Review (open access, CC BY) of how physics describes human crowds across five scales: supermacroscopic (networks of nodes and links with a speed–density equation of state), macroscopic (continuum fields and fundamental diagrams), mesoscopic (cellular automata, floor fields, path-integral and variational formulations), microscopic (social forces, avoidance, groups) and submicroscopic (body orientation, height, gait). It pairs each scale with the measurement technology that made it testable, from people counters to overhead depth-sensor tracking of millions of trajectories.

## Contribution

The most recent physics-oriented map of the field, explicitly placing crowds within active matter and stressing data-driven validation (large real-life tracking campaigns such as Eindhoven station) over laboratory-only experiments. Its reference list is a dense seed for any survey.

## Key results

- Synthesis claims (review): crowds display universal, statistically reproducible features from dilute to dense; social forces are non-Newtonian (F_ij ≠ −F_ji) and non-additive because they are mediated by sight and cognition; fundamental diagrams depend on crowd composition.
- Highlights a path-integral view in which observed trajectories sample P[γ] ∝ e^{−S[γ]}, allowing data-driven inference of an action functional.
- Future issues listed: psychological factors, submicroscopic observation (shoulder orientation from depth maps), and hybrid model-driven plus data-driven approaches.

## Methods and models

Narrative review, 2023, Annual Review of Condensed Matter Physics 14:311–333. Covers measurement methods (people counters, Bluetooth and Wi-Fi tracking, PIV-like Eulerian methods, optical and depth tracking) and models (fluid, kinetic, CA [[burstedde-2001-simulation]], social force [[helbing-1995-social]], anticipatory [[karamouzas-2014-universal]], group models [[moussaid-2010-walking]]).

## Limitations and open questions

Physics-centred; less coverage of ML trajectory prediction ([[alahi-2016-social]]) and of vehicular traffic control. Skimmed, not read line by line: section 3 (macroscopic) and some of section 5 were only scanned.

## Relevance to us

Best single entry point for a survey agent on crowds as active matter. It frames the questions our swarm work can address: which observables are universal, and how to infer interaction rules from large trajectory datasets. Pairs with [[helbing-2001-traffic]] (older, broader) and [[gu-2025-emergence]] (most striking recent result).
