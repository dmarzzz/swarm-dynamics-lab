---
id: gazzola-2016-learning
type: paper
title: Learning to school in the presence of hydrodynamic interactions
authors:
- M. Gazzola
- A. A. Tchieu
- D. Alexeev
- A. de Brauer
- P. Koumoutsakos
year: 2016
venue: Journal of Fluid Mechanics
url: https://doi.org/10.1017/jfm.2015.686
doi: 10.1017/jfm.2015.686
arxiv: null
cite: Gazzola, M., Tchieu, A. A., Alexeev, D., de Brauer, A., & Koumoutsakos, P. (2016). Learning to school in the presence of hydrodynamic interactions. Journal of Fluid Mechanics, 789, 726–749.
topics:
- marl-emergence
- collective-motion
added_by: dmarz/marl-emergence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 142 (Crossref, 2026-10-03)
code: []
---

## Summary

Swimmers are modelled as vortex dipoles interacting through the Biot-Savart law. Classical agent-based schooling rules do not produce robust schooling once flow-mediated interactions are included. Swimmers that adapt their strength with reinforcement learning in response to nonlinear hydrodynamic loads can hold their positions and school in various prescribed formations, and an evolutionary search identifies formations that minimise individual and collective swimming effort.

## Contribution

Earliest paper in this set showing that hand-written collective-motion rules break under physical (hydrodynamic) coupling and that learning restores coordination; the precursor to [[verma-2018-efficient]].

## Key results

- Behavioural rules from classical agent-based models fail to school robustly with hydrodynamic interactions (claimed in abstract).
- RL swimmers maintain formation; evolutionary optimisation finds effort-minimising patterns (claimed).

## Methods and models

Vortex-dipole swimmers, Biot-Savart interactions, RL (tabular Q-learning style per later citing work, not checked) plus evolutionary optimisation of formations. Abstract-level read.

## Limitations and open questions

Point-dipole model is a strong simplification of real fish hydrodynamics; formations are prescribed rather than emergent.

## Relevance to us

Cheap hydrodynamic surrogate (vortex dipoles) that a hackathon could actually simulate, unlike the DNS of [[verma-2018-efficient]]. Related: [[couzin-2002-collective]], [[vicsek-1995-novel]].
