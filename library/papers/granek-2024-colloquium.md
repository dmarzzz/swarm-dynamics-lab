---
id: granek-2024-colloquium
type: paper
title: "Colloquium: Inclusions, boundaries, and disorder in scalar active matter"
authors: ["Omer Granek", "Yariv Kafri", "Mehran Kardar", "Sunghan Ro", "Julien Tailleur", "Alexandre Solon"]
year: 2024
venue: "Reviews of Modern Physics"
url: https://arxiv.org/abs/2310.00079
doi: "10.1103/revmodphys.96.031003"
arxiv: "2310.00079"
cite: "Granek, O., Kafri, Y., Kardar, M., Ro, S., Tailleur, J., & Solon, A. (2024). Colloquium: Inclusions, boundaries, and disorder in scalar active matter. Reviews of Modern Physics, 96(3), 031003."
topics: ["active-matter"]
added_by: dmarz/active-matter-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "29 (OpenAlex, 2026-10-03)"
code: []  # library ids of code that implements this paper
---

## Summary

Colloquium on how dry scalar active matter (active particles whose only hydrodynamic field is density, e.g. active
Brownian or run-and-tumble particles without alignment) interacts with its surroundings: walls, curved or flexible
boundaries, localized obstacles, passive tracers, quenched bulk disorder and disordered boundaries. The unifying idea
is that an asymmetric object exerts a net force on the active fluid, and because momentum is not conserved this force
acts as a source of long-range density modulations and ratchet currents. As a result active fluids are far more
sensitive to their environment than passive ones: weak random potentials or rough walls destroy motility-induced
phase separation in dimensions where a passive fluid would still phase separate.

## Contribution

Synthesises a decade of work on active pressure ([[solon-2015-pressure]]), ratchets, obstacle-mediated interactions and
disorder into one framework built on a force-monopole multipole expansion. It is the reference for MIPS
([[cates-2015-motility]]) in non-ideal environments and complements [[bechinger-2016-active]] (complex environments,
single-particle focus) with collective, field-theoretic results.

## Key results

- An obstacle exerting a net force monopole p on non-interacting ABPs creates far-field density
  ρ(r) − ρ_b ≈ β_eff (r·p)/(S_d r^d) and current J ∝ r^(−d), with β_eff = μ/D_eff and D_eff = D_t + (μf_p)²/(d D_r).
  The total current equals μp exactly. Symmetric (spherical) obstacles give no modulation at any order.
- Pressure on walls has no equation of state in general (depends on wall details), recovered only for torque-free
  particles; curved walls give pressure differences proportional to curvature.
- Two asymmetric inclusions in an active bath feel non-reciprocal mediated interactions.
- Bulk quenched disorder (field theory and lattice run-and-tumble simulations): the homogeneous phase becomes
  scale-free with S(q) ∝ 1/q² as q → 0, versus a squared Lorentzian in equilibrium. Disorder destroys MIPS in d = 2 and
  d = 3: the lower critical dimension rises from 2 (Imry–Ma, passive) to 4.
- Disordered boundaries alone destroy bulk MIPS below d_c = 3, replacing it with scale-free density modulations in 2D.

## Methods and models

Analytical: Fokker–Planck equations for ABPs/RTPs, Poisson equation with localized source and multipole expansion,
Helmholtz–Hodge decomposition of random forcing, Imry–Ma-type droplet arguments, linear field theory with
self-consistency checks. Numerics: lattice and off-lattice RTP/ABP simulations from the cited papers. Read the
introduction, the single-obstacle section, the bulk-disorder section and the conclusions of arXiv:2310.00079v1;
pressure and tracer sections skimmed.

## Limitations and open questions

Scalar (non-aligning, dry) systems only: polar and nematic active fluids, and wet systems, are explicitly out of scope.
Surface tension of active interfaces remains debated. Most disorder results are for non-interacting or weakly
interacting particles plus field theory; experimental tests are scarce.

## Relevance to us

For a robot or agent swarm in a real arena, walls, obstacles and floor irregularities are not perturbations: an
asymmetric obstacle pumps agents over long distances, and modest disorder can prevent the clustering a clean
simulation predicts. A useful check before trusting an idealised periodic-box simulation. Related:
[[solon-2015-pressure]], [[cates-2015-motility]], [[bechinger-2016-active]], [[deblais-2018-boundaries]].
