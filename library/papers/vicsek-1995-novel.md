---
id: vicsek-1995-novel
type: paper
title: Novel Type of Phase Transition in a System of Self-Driven Particles
authors: [Tamás Vicsek, András Czirók, Eshel Ben-Jacob, Inon Cohen, Ofer Shochet]
year: 1995
venue: Physical Review Letters
url: https://arxiv.org/abs/cond-mat/0611743
doi: 10.1103/PhysRevLett.75.1226
arxiv: cond-mat/0611743
cite: Vicsek, T., Czirók, A., Ben-Jacob, E., Cohen, I., & Shochet, O. (1995). Novel type of phase transition in a system of self-driven particles. Physical Review Letters, 75(6), 1226–1229.
topics: [collective-motion, active-matter, criticality-measurement, sync-consensus]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "6564 (Crossref is-referenced-by-count, 2026-10-03); 6954 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Introduces what is now called the Vicsek model: point particles move at constant speed in a periodic 2D box
and at each discrete time step adopt the average heading of all particles within radius r (themselves
included), plus uniform angular noise in [-eta/2, eta/2]. Simulations show a kinetic transition from a
disordered state (zero net transport) to a state in which all particles move in a spontaneously chosen
common direction, controlled by noise eta and density rho. The authors read the transition as continuous,
with the order parameter vanishing as a power law near a critical noise. Read from the arXiv repost of the
PRL text (cond-mat/0611743), which reproduces the published letter.

## Contribution

The minimal "flocking as ferromagnetism out of equilibrium" model: replace spin alignment by velocity
alignment, temperature by noise, and let the spins move. It is the reference model for the physics of
collective motion and active matter; nearly every later paper in this topic is a variant of it or a test
against it ([[toner-1995-long]], [[gregoire-2004-onset]], [[chate-2008-collective]], [[ginelli-2016-physics]]).

## Key results

- Order parameter: v_a = |sum_i v_i| / (N v), ~0 when disordered, ~1 when ordered.
- Claimed continuous transition: v_a ~ (eta_c(rho) - eta)^beta with beta = 0.45 +/- 0.07, and
  v_a ~ (rho - rho_c(eta))^delta with delta = 0.35 +/- 0.06 (measured by fitting finite systems, N up to 10^4).
- Finite-size extrapolation gives eta_c(infinity) = 2.9 +/- 0.05 at rho = 0.4.
- Results insensitive to speed in 0.003 < v < 0.3 (reported, simulations at v = 0.03).
- Low noise and low density: coherent clusters moving in random directions; high density and low noise:
  macroscopic order.
- Later work overturned the "continuous" claim: the transition is discontinuous, with travelling bands, once
  systems are large enough ([[gregoire-2004-onset]], [[chate-2008-collective]]). The exponents above should be
  treated as finite-size artefacts, not universal values.

## Methods and models

Update rule: theta_i(t+1) = <theta(t)>_r + Delta_theta, with <theta>_r = atan2(<sin theta>, <cos theta>) over
neighbours within r = 1; x_i(t+1) = x_i(t) + v_i(t) Delta_t with |v_i| = v. Synchronous (parallel) update,
periodic square box of side L, random initial positions and headings. N = 40 to 10000 (L = 3.1 to 50).
Error bars from 5 runs near the transition. Noise is added after averaging (so-called angular or "intrinsic"
noise). No repulsion, no attraction, no cohesion; density is fixed by the box.

## Limitations and open questions

- System sizes far too small to see the band instability; the order of the transition was wrong.
- No cohesion: groups cannot form in open space with nonzero noise ([[couzin-2002-collective]] adds
  attraction and repulsion for this reason).
- Metric neighbourhood; empirical work later favoured topological neighbours ([[ballerini-2008-interaction]]).
- The authors note the v -> 0 limit maps to the XY model and v -> infinity to mean field, but do not explain
  why long-range order exists in 2D (that came from [[toner-1995-long]]).

## Relevance to us

The default baseline for any swarm-dynamics experiment. A minimal implementation is a few lines of numpy and
gives a polarization order parameter we can reuse to compare learned or LLM-driven agents against the
physics baseline. Expect bands and a first-order transition if we simulate large N. See review context in
[[vicsek-2012-collective]] and [[chate-2020-dry]].
