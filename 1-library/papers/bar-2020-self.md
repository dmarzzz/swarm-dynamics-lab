---
id: bar-2020-self
type: paper
title: "Self-Propelled Rods: Insights and Perspectives for Active Matter"
authors: ["Markus Bär", "Robert Großmann", "Sebastian Heidenreich", "Fernando Peruani"]
year: 2020
venue: "Annual Review of Condensed Matter Physics"
url: https://arxiv.org/abs/1907.00360
doi: "10.1146/annurev-conmatphys-031119-050611"
arxiv: "1907.00360"
cite: "Bär, M., Großmann, R., Heidenreich, S., & Peruani, F. (2020). Self-Propelled Rods: Insights and Perspectives for Active Matter. Annual Review of Condensed Matter Physics, 11, 441–466."
topics: ["active-matter", "collective-motion"]
added_by: dmarz/active-matter-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "293 (OpenAlex, 2026-10-03)"
code: []  # library ids of code that implements this paper
---

## Summary

Review of self-propelled rods: elongated active units (gliding and swimming bacteria such as Myxococcus xanthus and
Bacillus subtilis, motility-assay filaments, shaken granular rods) whose shape turns steric collisions into alignment.
The authors organise the field by two axes: dry versus wet (with or without long-range flow) and interaction type
(pure steric repulsion versus effective nematic alignment when rods can slide over each other). Dry steric rods form
motile polar clusters, lanes and polar bands; dry rods with effective nematic alignment form nematic bands described
by coarse-grained continuum equations; wet rods at high density show mesoscale turbulence with a selected vortex size.

## Contribution

A map that places self-propelled rods between polar flocking ([[vicsek-1995-novel]], [[chate-2019-dry]]) and active
nematics ([[doostmohammadi-2018-active]], [[narayan-2007-long]]), with MIPS of discs as the aspect-ratio-one limit
([[cates-2015-motility]]). Reviews both particle models and continuum theories, including the mesoscale-turbulence
model of [[wensink-2012-meso]].

## Key results

- Simulated (cited): steric self-propelled rods cluster above a critical aspect ratio at densities below both
  percolation and the equilibrium isotropic–nematic transition; clusters are polar and motile, sometimes smectic.
  Cluster-size distributions follow kinetic fragmentation–coagulation equations.
- Polar bands seen with periodic boundaries break up above a critical system size into disordered giant aggregates
  that eject polar clusters, which differs from MIPS drops.
- Nematic phase: giant number fluctuations σ_n ~ ⟨n⟩^α with α ≈ 0.8 in rod simulations and α ≈ 0.6 measured in
  filamentous non-tumbling E. coli (equilibrium value 0.5). Whether nematic order is truly long-range is unsettled.
- Wet rods: mesoscale turbulence with a characteristic vortex spacing, reproduced by a continuum equation derived from
  particle models with polar short-range and hydrodynamic long-range interactions.
- Their summary point: density, activity and shape are the generic control parameters, and the symmetry of the
  effective interaction (polar or nematic) decides the emergent order.

## Methods and models

Narrative review. Particle models (rods as rectangles, ellipses, spherocylinders or chains of spheres, purely repulsive
short-range forces; Vicsek-like models with nematic torque) and continuum field theories (Boltzmann–Ginzburg–Landau
derivations, Toner–Tu–Swift–Hohenberg-type equations for wet turbulence). Read abstract, introduction, the dry-rod
phenomenology sections and the summary and future-issues lists of arXiv:1907.00360v2; the wet-rod theory section only
skimmed.

## Limitations and open questions

Authors' future issues: almost nothing is known about rods in 3D (multilayers, biofilms); biochemical signalling,
reversals, trail following and adhesion are missing from most models; control of rod assemblies by confinement or
fields is in its infancy; machine learning for classifying states and inferring interaction rules is suggested.

## Relevance to us

Elongated robots or vehicles (and many bacteria) align through collisions alone, so the rod literature tells us which
emergent states (polar clusters, lanes, bands, jammed aggregates) to expect in a dense swarm of non-communicating
elongated agents, and that the result depends on whether agents can slide past each other. Related:
[[deseigne-2010-collective]], [[kumar-2014-flocking]], [[wensink-2012-meso]], [[chate-2019-dry]].
