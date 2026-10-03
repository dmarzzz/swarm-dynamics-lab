---
id: buttinoni-2013-dynamical
type: paper
title: "Dynamical Clustering and Phase Separation in Suspensions of Self-Propelled Colloidal Particles"
authors: ["Ivo Buttinoni", "Julian Bialké", "Felix Kümmel", "Hartmut Löwen", "Clemens Bechinger", "Thomas Speck"]
year: 2013
venue: "Physical Review Letters"
url: https://arxiv.org/abs/1305.4185
doi: "10.1103/physrevlett.110.238301"
arxiv: "1305.4185"
cite: "Buttinoni, I., Bialké, J., Kümmel, F., Löwen, H., Bechinger, C., & Speck, T. (2013). Dynamical Clustering and Phase Separation in Suspensions of Self-Propelled Colloidal Particles. Physical Review Letters, 110(23), 238301."
topics: ["active-matter", "collective-motion"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "1181 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Experiment plus simulation on quasi-2D suspensions of carbon-capped Janus colloids (R ≈ 2.13 µm) that self-propel by
light-triggered local demixing of a near-critical water–lutidine mixture, so speed is tuned continuously by laser
intensity. At low area fraction (φ ≈ 0.1) the particles form dynamic clusters whose mean size grows linearly with speed;
at higher φ (≈ 0.25–0.36) they phase separate into a few large clusters and a dilute gas. Turning the light off
dissolves the clusters, so aggregation is purely activity-driven. Brownian dynamics of purely repulsive active disks
reproduce both behaviours, and imaging of cap orientations shows the self-trapping mechanism: particles on a cluster rim
point inward and leave only after rotational diffusion turns them outward.

## Contribution

First experimental report of motility-induced phase separation-like behaviour in synthetic active colloids where
attractions were deliberately minimized (carbon instead of metal caps), directly supporting the theory reviewed in
[[cates-2015-motility]] and the simulations of [[fily-2012-athermal]] and [[redner-2013-structure]]. Contrast with
[[palacci-2013-living]], where clustering was attributed to phoretic attraction.

## Key results

- Measured: dilute single-particle motion is a persistent random walk with D₀ ≈ 0.029 µm²/s; D_r independent of v and
  consistent with no-slip rotation.
- Measured: mean cluster size grows roughly linearly with speed (fit 1.1 + 1.1v, v in µm/s) at φ ≈ 0.1; simulations
  reproduce the trend but with weaker growth and fewer, larger clusters (authors attribute the difference to
  hydrodynamics).
- Measured: order parameter P = fraction of particles in the largest cluster jumps at a critical speed that decreases
  with φ (data at φ ≈ 0.18, 0.26, 0.36; v up to ≈ 1.6 µm/s); the experimental transition occurs at lower density than
  in simulations except at φ ≈ 0.36 where they agree.
- Mechanism (imaged with R ≈ 4 µm particles): rim particles point inward; escape time ~ 1/D_r independent of v, while
  arrival rate grows with v, so clusters grow with speed (flux balance).

## Methods and models

Janus SiO₂ beads with 10 nm graphite cap in 28 mass % 2,6-lutidine, 400 × 400 µm² cavities 6 µm high, 532 nm
illumination ≤ 5 µW/µm²; tracking and cluster detection by overlap/area. Simulations: N = 4900 ABPs, WCA repulsion
(ε = 100 k_BT) with optional attractive tail λ = 0.5 k_BT used only to match passive g(r); Pe = 2Rv/D₀; time step
10⁻⁵. Full read of arXiv:1305.4185 (main text; Supplementary not read).

## Limitations and open questions

Final coarsening to a single cluster not observed (too slow); hydrodynamic interactions neglected in the model; small
residual attractions present in experiment; quasi-2D with 3D rotation. Not a measurement of binodals.

## Relevance to us

Physical evidence that crowding plus persistence alone makes active agents clump, the same failure mode a dense robot
swarm with head-on blocking will show. The self-trapping picture gives a back-of-envelope rule: cluster size set by
arrival flux ∝ ρv versus escape rate ∝ D_r. Related: [[cates-2015-motility]], [[fily-2012-athermal]],
[[bechinger-2016-active]] (same group), [[digregorio-2018-full]].

## Notes from dmarz/active-matter-audit

Audit 2026-10-03: checked metadata against Crossref (110(23), 238301) and numbers against the arXiv PDF (R ≈ 2.13 µm, 10 nm cap, 28 mass % lutidine, D₀ ≈ 0.029 µm²/s, fit 1.1 + 1.1v, N = 4900, ε = 100 k_BT, φ ≈ 0.18, 0.26, 0.36, ≤ 5 µW/µm²). All correct; no changes.
