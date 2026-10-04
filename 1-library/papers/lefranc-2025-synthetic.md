---
id: lefranc-2025-synthetic
type: paper
title: "Synthetic Quorum Sensing and Absorbing Phase Transitions in Colloidal Active Matter"
authors: ["Thibault Lefranc", "Alberto Dinelli", "Carla Fernandez Rico", "Roel P. A. Dullens", "Julien Tailleur", "Denis Bartolo"]
year: 2025
venue: "Physical Review X"
url: https://arxiv.org/abs/2502.13919
doi: "10.1103/8csn-71jk"
arxiv: "2502.13919"
cite: "Lefranc, T., Dinelli, A., Fernandez Rico, C., Dullens, R. P. A., Tailleur, J., & Bartolo, D. (2025). Synthetic Quorum Sensing and Absorbing Phase Transitions in Colloidal Active Matter. Physical Review X, 15(3), 031050."
topics: ["active-matter", "collective-decision"]
added_by: dmarz/active-matter-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "5 (OpenAlex, 2026-10-03)"
code: []  # library ids of code that implements this paper
---

## Summary

Lefranc, Dinelli, Bartolo, Tailleur and colleagues make colloidal rods (about 3.7 µm long, aspect ratio about 6.7)
self-propel by Quincke electrorotation and find that they switch their motor off in crowds: in dilute regions they
roll on the electrode, but after collisions at high local density they stand up along the field and stop. This is an
autonomous, physically embodied form of quorum sensing, with no external feedback loop. Varying density and voltage
they observe a homogeneous active liquid, coexistence of the active liquid with dense clusters of arrested rods, and
at high density a fully arrested amorphous solid. A minimal model of active Brownian particles with density-dependent
switching rates shows that quorum sensing alone gives an absorbing phase transition (everything freezes), and that
steric repulsion is what arrests the absorption and stabilises coexistence, with a pressure drop across a flat
interface.

## Contribution

First large-scale (not computer-controlled) synthetic active system with density-regulated motility, compared with the
feedback-loop experiment [[bauerle-2018-self]] and the theory of density-dependent motility in
[[cates-2015-motility]]. It identifies a phase-coexistence mechanism distinct from MIPS: absorbing-state dynamics
competing with mechanical stress.

## Key results

- Measured: the fraction of standing (arrested) rods is near zero below a threshold density ρ̄ ≈ 0.1 µm⁻² and grows
  above it; the switching is collective, not a single-rod property.
- Measured: liquid and arrested-phase densities at coexistence hardly depend on mean density (binodals from the
  lever rule on the arrested area fraction); a single arrested cluster grows as R(t) ~ (t − t₀)^(1/3); periodic voltage
  driving gives hysteresis loops, evidence of metastability.
- Model: rolling→standing rate α(ρ) = α₀(ρ − ρ̄)Θ(ρ − ρ̄), standing→rolling rate β(ρ_R) = β₀ρ_R. Mean field gives
  all-active for ρ₀ < ρ̄, all-arrested above ρ_c = α₀ρ̄/(α₀ − β₀), and a mixed state in between that experiments
  never show. With diffusion of rolling particles alone (J = −D_eff∇ρ_R) a nucleated arrested cluster absorbs the whole
  system.
- Simulated with WCA repulsion: coexistence is stabilised; each bulk phase has an equation of state for wall
  pressure, but the liquid pressure exceeds the arrested-phase pressure (P_L > P_A) across a flat interface, the
  difference coming from switching events localised at the interface.

## Methods and models

Photoresist (SU-8) rods in a V-shaped microfluidic channel under DC fields (10 to 300 V), fluorescence and bright-field
imaging with 25 % labelled rods; 3D-printed rods 100 times larger as a macroscopic check. Theory: mean-field rate
equations, fluctuating hydrodynamics, ABP simulations with density-dependent switching (details in appendices and SM,
not read). Read the abstract, introduction, experimental section, model sections and conclusion of arXiv:2502.13919v2.

## Limitations and open questions

The microscopic mechanism of the switching (contact, electrostatic, hydrodynamic) is not modelled; the minimal model
imposes the rates phenomenologically. Rods are polydisperse (±1.5 µm). Statistics on individual switching rates are
limited; only their ratio is measured.

## Relevance to us

A robot-swarm rule "stop when crowded, restart when bumped by a mover" is exactly this model, and the paper predicts
its failure mode: without enough repulsion the whole swarm can freeze (absorbing state). It also gives the minimal
two-rate model to test in simulation. Related: [[bauerle-2018-self]], [[zhao-2023-chemotactic]],
[[ziepke-2025-acoustic]], [[aina-2022-toward]], [[bricard-2013-emergence]] (Quincke rollers).
