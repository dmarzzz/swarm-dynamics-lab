---
id: ling-2019-behavioural
type: paper
title: Behavioural plasticity and the transition to order in jackdaw flocks
authors: [Hangjian Ling, Guillam E. Mclvor, Joseph Westley, Kasper van der Vaart, Richard T. Vaughan, Alex Thornton, Nicholas T. Ouellette]
year: 2019
venue: Nature Communications
url: https://doi.org/10.1038/s41467-019-13281-4
doi: 10.1038/s41467-019-13281-4
arxiv: null
cite: 'Ling, H., Mclvor, G. E., Westley, J., van der Vaart, K., Vaughan, R. T., Thornton, A., & Ouellette, N. T. (2019). Behavioural plasticity and the transition to order in jackdaw flocks. Nature Communications, 10(1), 5174.'
topics: [collective-motion, criticality-measurement]
added_by: dmarz/collective-motion-audit
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "80 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

High-speed 3D stereo tracking of wild jackdaws (Corvus monedula) in Cornwall in two ecological contexts:
6 transit flocks flying to the roost (25-330 birds) and 10 anti-predator "mobbing" flocks gathered around
a model predator (4-120 birds). Using alignment angle and the anisotropy of neighbour positions as
functions of both topological rank n and metric distance r, they show the same species interacts
topologically in transit but metrically when mobbing. As a consequence, mobbing groups show a
density-driven transition from disordered swarms to ordered flight, while transit flocks are highly
ordered at all densities. Read: abstract, introduction, results and figure captions of the PMC full text;
methods skimmed.

## Contribution

The first field evidence that one species switches between metric and topological interaction rules with
context, which reconciles the topological result of [[ballerini-2008-interaction]] (starlings) with
metric-rule reports in other birds. It is also the first density-driven order transition reported in
flocking birds, joining locusts ([[buhl-2006-disorder]], now disputed by [[sayin-2025-behavioral]]) and
cells.

## Key results

- Mobbing flocks: alignment angle and anisotropy depend on r, and curves for different n collapse, so the
  interaction is metric, with range about r = 5 m (roughly 14 body lengths).
- Transit flocks: anisotropy depends mainly on n; birds interact with about 7-8 neighbours (as in the
  authors' earlier jackdaw study), and gamma(n) collapses across flocks of different density.
- Order-density relation measured on 154 mobbing sub-groups: order parameter phi rises from disordered at
  low density to near 1 at high density, and the curve agrees with a generic metric self-propelled-particle
  model; transit sub-groups are nearly perfectly polarized at every density.
- Density defined as rho = 6N / (pi <d_i>^3), with d_i the distance to bird i's farthest neighbour.
- Interpretation (argued, not tested): topological rules suit long-distance cohesion and predator
  awareness; metric rules suit converging on a localized threat.

## Methods and models

Multi-camera high-speed 3D imaging of wild flocks at roosts and at a model-predator mobbing site;
3D trajectory reconstruction; analysis of alignment angle theta = g(n, r) at fixed n or r, anisotropy
factor gamma of neighbour distributions; comparison with a standard self-propelled-particle (Vicsek-type)
model with metric interactions. Supplementary Data 1 lists the sub-group order and density values.

## Limitations and open questions

- Small samples (6 transit, 10 mobbing events) and small mobbing groups; edge effects limit gamma(n) for
  n > 5 in transit flocks.
- Transit flocks share a common external goal (the roost), so their high order is partly
  environmentally imposed, as the authors note.
- The model comparison is qualitative; the switching mechanism itself is not identified.

## Relevance to us

Directly useful for agent design: interaction rules need not be fixed, and a swarm that switches from
k-nearest-neighbour coupling (robust cohesion) to metric coupling (local convergence) by task context is
biologically grounded. It also gives a real-data order-versus-density curve to compare simulations with.
Related: [[ballerini-2008-interaction]], [[vicsek-1995-novel]], [[ouellette-2022-physics]],
[[papadopoulou-2023-dynamics]].
