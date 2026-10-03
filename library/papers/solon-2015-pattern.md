---
id: solon-2015-pattern
type: paper
title: 'Pattern formation in flocking models: A hydrodynamic description'
authors: [Alexandre P. Solon, Jean-Baptiste Caussin, Denis Bartolo, Hugues Chaté, Julien Tailleur]
year: 2015
venue: Physical Review E
url: https://arxiv.org/pdf/1509.03395
doi: 10.1103/PhysRevE.92.062111
arxiv: '1509.03395'
cite: 'Solon, A. P., Caussin, J.-B., Bartolo, D., Chaté, H., & Tailleur, J. (2015). Pattern formation in flocking models: A hydrodynamic description. Physical Review E, 92(6), 062111.'
topics: [collective-motion, active-matter]
added_by: dmarz/collective-motion-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "84 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

A detailed study of the deterministic hydrodynamic equations for polar flocking (Vicsek and active Ising
models). Using a phenomenological density-polarization theory, the authors show there is an infinity of
propagating solutions, which fall into three types: periodic orbits (microphase separation: trains of
bands), homoclinic orbits (solitary bands) and heteroclinic orbits (full phase separation into a polar
liquid and a disordered gas). Only a small fraction are linearly stable, but all three types are among
them. Coarsening in the hydrodynamic equations favours the fastest, largest pattern, so it ends in phase
separation, which then sets the binodals of the phase diagram. Read: abstract, contents, introduction,
Section II and the conclusion of arXiv v1; the solution-space analysis (Sections IV-VIII) was skimmed.

## Contribution

The long companion to the PRL [[solon-2015-phase]]. Together they establish that the Vicsek "order-disorder
transition" is best understood as a liquid-gas transition with a coexistence region, and explain why the
Vicsek model shows microphase separation (finite bands) while the active Ising model shows full phase
separation: in the Vicsek case, fluctuations arrest coarsening because large bands are destabilized by
the giant number fluctuations of the polar liquid. This resolves the band phenomenology first reported in
[[gregoire-2004-onset]] and [[chate-2008-collective]].

## Key results

- Three classes of propagative solutions (periodic, homoclinic, heteroclinic) exist in the generic
  hydrodynamic equations, in the active Ising equations and in a simplified Vicsek hydrodynamics.
- Linear stability (numerical, 1D): stable solutions are a small subset but include all three types.
- Coarsening at the deterministic level leads to the phase-separated (heteroclinic) solution; spinodal and
  binodal lines are computed for both models, and the hydrodynamic phase diagrams agree qualitatively with
  the microscopic ones.
- Microphase separation in the Vicsek model is interpreted as arrested coarsening caused by noise, a claim
  supported by [[solon-2015-phase]] rather than shown in this paper.

## Methods and models

Phenomenological equations for density rho and polarization m with constant or density-dependent
coefficients; travelling-wave ansatz reduces them to a Newton-like ODE ("Newton mapping"), whose fixed
points, Hopf bifurcation and orbits classify the solutions; numerical linear stability in 1D; comparison
with microscopic simulations of the Vicsek model (eta = 0.4, v0 = 0.5) and the active Ising model in
800 x 100 boxes (their Fig. 1).

## Limitations and open questions

- Deterministic analysis; the selection of band size in the Vicsek model is left open ("How this size is
  selected however remains to be determined").
- Mostly 1D stability; transverse instabilities of bands are not treated here.

## Relevance to us

If a hackathon simulation of Vicsek agents shows travelling bands near the transition, this paper and
[[solon-2015-phase]] are what explains them, and they warn against reading the transition as continuous
(the error in [[vicsek-1995-novel]]). Background: [[chate-2020-dry]], [[ginelli-2016-physics]].
