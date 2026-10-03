---
id: toner-1995-long
type: paper
title: "Long-Range Order in a Two-Dimensional Dynamical XY Model: How Birds Fly Together"
authors: ["John Toner", "Yuhai Tu"]
year: 1995
venue: "Physical Review Letters"
url: https://arxiv.org/abs/adap-org/9506001
doi: "10.1103/physrevlett.75.4326"
arxiv: "adap-org/9506001"
cite: "Toner, J., & Tu, Y. (1995). Long-Range Order in a Two-Dimensional Dynamical XY Model: How Birds Fly Together. Physical Review Letters, 75(23), 4326–4329."
topics: ["active-matter", "collective-motion", "criticality-measurement"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "1261 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Toner and Tu write a continuum, coarse-grained theory of flocking: a velocity field v and a conserved density ρ obeying
Navier–Stokes-like equations without Galilean invariance, with a Landau term (α − β|v|²)v that gives the field a
preferred magnitude, anisotropic diffusion, a density-dependent pressure and additive noise. Using a dynamical
renormalization group they show the convective nonlinearities are relevant below d = 4, obtain exact exponents in d = 2
(z = 6/5, ζ = 3/5, χ = −1/5), and conclude that, unlike the equilibrium XY model, a 2D flock has true long-range
orientational order, so the Mermin–Wagner theorem does not apply to moving agents.

## Contribution

The founding hydrodynamic theory of polar active matter. It explains why the ordered phase of the Vicsek model
([[vicsek-1995-novel]]) is possible in 2D and defines the "Toner–Tu universality class" that all later flocking theory
refers to. Extended in [[toner-1998-flocks]] and [[toner-2005-hydrodynamics]]; the 2D exponents were later shown not to
be exact (Toner 2012) and were tested numerically in [[mahault-2019-quantitative]].

## Key results

- Equations of motion (Eqs. 1–2): ∂ₜv + (v·∇)v = αv − β|v|²v − ∇P + D_L∇(∇·v) + D₁∇²v + D₂(v·∇)²v + f;
  ∂ₜρ + ∇·(vρ) = 0. The convective term (v·∇)v is what distinguishes the model from model-A dynamics of an XY magnet.
- Linear theory: χ = 1 − d/2, so transverse velocity fluctuations diverge for d ≤ 2 without the nonlinearities.
- Nonlinear terms λ(v⊥·∇)v⊥ and σ₂∇(δρ²) are relevant for d < 4 (critical dimension d_c = 4).
- Claimed exact d = 2 exponents from symmetry ("pseudo-Galilean" invariance plus non-renormalization of D∥ and noise
  strength Δ): z = 2(d+1)/5, ζ = (d+1)/5, χ = (3−2d)/5, i.e. z = 6/5, ζ = 3/5, χ = −1/5 in 2D. Since χ < 0, order is
  long-ranged. (The non-renormalization argument was later found to fail; see Toner 2012 as summarized in
  [[chate-2019-dry]].)
- Prediction: density correlations have sound-like peaks at ω = ±c q⊥ with c = √(σ₁ρ₀); rms transverse fluctuations
  approach a constant as L⊥^(−2/5) in 2D.
- Even if the cubic vertex were relevant, rotational invariance gives χ = (z − d)/3 < 0 for z < 2, preserving order.

## Methods and models

Phenomenological symmetry-based field theory; dynamical renormalization group (Forster–Nelson–Stephen style), one-loop
calculation near d = 4 (fixed line (g₁/2 + g₂)g₁ = 768π²ε/55), and an exact-exponent argument in d = 2 via a
height-field mapping v_x = ∂ₓh. No simulations; compares qualitatively with Vicsek et al. Read from the arXiv preprint
adap-org/9506001 (author order Tu and Toner there; the PRL lists Toner and Tu).

## Limitations and open questions

- The "exact" 2D exponents rest on assumptions that turned out to be wrong once all relevant nonlinearities are kept
  (Toner 2012); quantitative tests in simulations came only decades later ([[mahault-2019-quantitative]]).
- Assumes the homogeneous ordered phase; it does not address the band/microphase-separated regime near onset that
  dominates finite systems ([[gregoire-2004-onset]], [[solon-2015-phase]]).
- Dry (no momentum conservation) and additive noise only; real birds have finite groups, cohesion and inertia.

## Relevance to us

Any swarm that aligns headings and moves in 2D is predicted to sustain global order despite noise, with anomalous
(giant) number fluctuations and superdiffusion transverse to motion. These are measurable signatures for our
simulations or robot data: measure ⟨ΔN²⟩ ~ ⟨N⟩^φ (φ ≈ 1.6 predicted in 2D) and transverse MSD. Read together with
[[chate-2019-dry]] for what simulations actually show, [[simha-2002-hydrodynamic]] for the wet counterpart, and
[[marchetti-2013-hydrodynamics]] for the full framework.

## Notes from dmarz/active-matter-audit

Audit 2026-10-03: metadata confirmed against Crossref (75(23), 4326–4329); the arXiv preprint adap-org/9506001 (title order reversed, authors Tu and Toner) is the page that was read, so I set the arxiv field to it. Checked the exponents z = 2(d+1)/5 and the one-loop fixed line 768π²ε/55 against the preprint. Replaced the Semantic Scholar count with OpenAlex (1261). `lab.py verify` still flags this entry because Crossref wraps "XY" in MathML and the arXiv title is reversed; it is a false positive.
