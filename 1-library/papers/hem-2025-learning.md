---
id: hem-2025-learning
type: paper
title: "Learning general pair interactions between self-propelled particles"
authors: ["Jérôme Hem", "Alexis Poncet", "Pierre Ronceray", "Daiki Nishiguchi", "Vincent Démery"]
year: 2025
venue: "Soft Matter"
url: https://arxiv.org/abs/2507.13667
doi: "10.1039/d5sm00655d"
arxiv: "2507.13667"
cite: "Hem, J., Poncet, A., Ronceray, P., Nishiguchi, D., & Démery, V. (2025). Learning general pair interactions between self-propelled particles. Soft Matter, 21(37), 7257-7269."
topics: [collective-motion, active-matter]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "0 (OpenAlex W4413448842, 2026-10-03)"
code: []
---
## Summary

Uses Stochastic Force Inference to learn general pair interactions (radial, transverse forces and torques) between self-propelled Janus colloids from experimental trajectories, in one experiment where particles flock and one where they stay disordered. Learned interactions fed into simulations reproduce all measured observables and can be extrapolated to other densities. The radial interaction is mostly repulsive and isotropic, the angular interaction has richer angular dependence and controls the behaviour, and the transverse part is negligible; symmetry tests show the interactions cannot be purely electrostatic, so hydrodynamics contributes.

## Contribution

A worked, validated example of inferring full pairwise interaction functions in a flocking active system from data.

## Key results

- Measured/inferred (abstract): repulsive isotropic radial force, angle-dependent torque governs flocking, negligible transverse force; simulations reproduce experiments.

## Methods and models

Stochastic Force Inference applied to experimental trajectories, with the learned interactions re-simulated (basis choices not read).

## Limitations and open questions

Abstract only; colloids, not animals.

## Relevance to us

Method template for inferring rules from our data; compare [[han-2024-collective]] and [[gao-2024-learning]]. Same colloid class as [[das-2024-flocking]].

## Notes from dmarz/collective-motion-recent-audit

Metadata (title, authors, year, venue, DOI/arXiv) cross-checked against OpenAlex and passes verify. citations replaced with the OpenAlex cited_by_count (2026-10-03) in place of the Crossref count.
