---
id: bertin-2006-boltzmann
type: paper
title: "Boltzmann and hydrodynamic description for self-propelled particles"
authors: ["Eric Bertin", "Michel Droz", "Guillaume Grégoire"]
year: 2006
venue: "Physical Review E"
url: https://arxiv.org/abs/cond-mat/0601038
doi: "10.1103/physreve.74.022101"
arxiv: "cond-mat/0601038"
cite: "Bertin, E., Droz, M., & Grégoire, G. (2006). Boltzmann and hydrodynamic description for self-propelled particles. Physical Review E, 74(2), 022101."
topics: ["active-matter", "collective-motion"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "391 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Bertin, Droz and Grégoire derive hydrodynamic equations for density and velocity fields from a Boltzmann equation for
Vicsek-like self-propelled particles with noisy binary alignment in 2D. A homogeneous moving state appears below a
transition line in the noise–density plane, but it is unstable to spatial perturbations near onset, suggesting more
complex structures. Read from the abstract on the page in `url`; details beyond the abstract are not checked.

## Contribution

First microscopic derivation of Toner–Tu-type equations, giving coefficients in terms of model parameters; the start
of the Boltzmann–Ginzburg–Landau programme explained in detail in [[chate-2019-dry]] (read in full). The predicted
instability is the band instability seen in [[chate-2008-collective]].

## Key results

- Transition line for spontaneous motion in the (noise, density) plane (derived).
- Homogeneous ordered state unstable near onset (derived).

## Methods and models

Boltzmann equation with binary collisions under molecular chaos; angular Fourier expansion and truncation.
arXiv:cond-mat/0601038; full text not read.

## Limitations and open questions

Molecular chaos and truncation give only qualitative agreement with particle models (see [[chate-2019-dry]]).

## Relevance to us

The recipe for turning an agent-level alignment rule into PDEs, useful if we want continuum predictions for a swarm
rule we design. Related: [[toner-1995-long]], [[gregoire-2004-onset]].
