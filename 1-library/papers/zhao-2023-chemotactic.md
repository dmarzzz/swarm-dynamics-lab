---
id: zhao-2023-chemotactic
type: paper
title: "Chemotactic Motility-Induced Phase Separation"
authors: ["Hongbo Zhao", "Andrej Košmrlj", "Sujit Sankar Datta"]
year: 2023
venue: "Physical Review Letters"
url: https://arxiv.org/abs/2301.12345
doi: "10.1103/physrevlett.131.118301"
arxiv: "2301.12345"
cite: "Zhao, H., Košmrlj, A., & Datta, S. S. (2023). Chemotactic Motility-Induced Phase Separation. Physical Review Letters, 131(11), 118301."
topics: ["active-matter", "collective-decision"]
added_by: dmarz/active-matter-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "58 (OpenAlex, 2026-10-03)"
code: []  # library ids of code that implements this paper
---

## Summary

Zhao, Košmrlj and Datta ask what happens to motility-induced phase separation when active Brownian particles also
perform chemotaxis up a gradient of an attractant they themselves consume. They add a Keller–Segel chemotactic flux
to the Cahn–Hilliard ("Model B") continuum description of MIPS and couple it to a diffusing, consumed, uniformly
supplied chemoattractant. Linear stability analysis plus numerical simulations show that self-generated chemotaxis
competes with MIPS: dense domains deplete the attractant around them, so particles climb the gradient outwards and
disperse. Depending on parameters this suppresses MIPS entirely, arrests coarsening at a finite domain size, or
produces oscillatory instabilities with travelling bands and domains that stretch, rotate and translate.

## Contribution

Bridges the two classic routes to active aggregation and pattern formation, MIPS ([[cates-2015-motility]],
[[tailleur-2008-statistical]]) and Keller–Segel chemotaxis, and gives explicit criteria for when one defeats the other.
Fills the "chemotactic and quorum-sensing MIPS" gap noted in the active-matter scan.

## Key results

- Model: ∂φ/∂t = −∇·J with J = −M₀φ∇μ_h(φ, Pe_R) − κ∇²φ + χ₀φ∇f(c); ∂c/∂t = D_c∇²c − kφg(c) + S, linearised
  f(c) = g(c) = c. Five control parameters {φ₀, Pe_R, α₀ = M₀/D_c, Da₀ = κk/D_c, Pe_C = χ₀/M₀}.
- MIPS is suppressed only when both hold: reduced chemotactic Péclet Pe′_C ≥ (1 + min{Da,1})²/(4√min{Da,1}) and
  α ≤ α_crit = 1 + 2Da + 2√(Da(1+Da)) (square roots reconstructed from PDF text extraction; check Eq. in the paper) (strong chemotaxis and fast attractant diffusion relative to the particles).
- Arrest: the instability becomes finite-wavelength (domains stop coarsening) when Pe′_C > 1, versus the unbounded
  instability of ordinary MIPS for Pe′_C < 1. Simulations agree with this boundary.
- Oscillation: for strong chemotaxis and slow attractant diffusion (large α₀) the attractant field lags the density,
  unstable modes acquire Im ω ≠ 0, and domains move as travelling bands or deforming, rotating patches.
- These are predictions of a mean-field continuum model, checked against its own numerical solutions, not experiments.

## Methods and models

Continuum Cahn–Hilliard description of ABP MIPS with an equation-of-state-based bulk chemical potential, plus a
chemotactic flux and a reaction–diffusion equation for the attractant; linear stability analysis (dispersion relation
ω(q)) and finite-difference simulations in periodic 2D domains, with details in the supplement (not read). Read the
main text of arXiv:2301.12345v1.

## Limitations and open questions

No particle-level simulations or experiments in the main text; linearised sensing and uptake (no Michaelis–Menten
saturation); attractant supply taken uniform; the Model B description ignores the non-integrable gradient terms of
Active Model B+. The supplement was not read.

## Relevance to us

A swarm that both clusters through crowding and follows a self-consumed resource gradient (robots foraging for a
depletable signal, agents competing for bandwidth or charging spots) is predicted to form finite, possibly moving
clusters rather than one big clump. The two criteria give a design rule for choosing between dispersed coverage and
aggregation. Related: [[bauerle-2018-self]], [[ziepke-2022-multi]], [[ziepke-2025-acoustic]], [[lefranc-2025-synthetic]].
