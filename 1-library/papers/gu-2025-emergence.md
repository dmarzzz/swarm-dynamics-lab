---
id: gu-2025-emergence
type: paper
title: Emergence of collective oscillations in massive human crowds
authors:
- François Gu
- Benjamin Guiselin
- Nicolas Bain
- Iker Zuriguel
- Denis Bartolo
year: 2025
venue: Nature
url: https://www.nature.com/articles/s41586-024-08514-6
doi: 10.1038/s41586-024-08514-6
arxiv: null
cite: Gu, F., Guiselin, B., Bain, N., Zuriguel, I., & Bartolo, D. (2025). Emergence of collective oscillations in massive human crowds. Nature, 638(8049), 112–119. https://doi.org/10.1038/s41586-024-08514-6
topics:
- crowds-and-traffic
- active-matter
- collective-motion
- criticality-measurement
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 76 (Crossref, 2026-10-03)
code: []
---

## Summary

Films the densely packed crowd (up to about 6,000 people, 50 m x 20 m plaza) at the opening of the San Fermín festival in Pamplona in 2019, 2022, 2023 and 2024 and measures density and velocity fields with head detection and particle image velocimetry. Above a critical density ρ* = 4.0 ± 0.5 m^-2, the crowd self-organises into chiral orbital oscillations with a period of about 18 s that involve hundreds of people at once. A minimal mean-field mechanical theory with an active "odd" friction term explains these as a non-reciprocal phase transition, and the same signature is found in footage from the 2010 Love Parade disaster.

## Contribution

Replaces the long-standing description of dense crowd quakes as "turbulent" with evidence that they are periodic and chiral, and derives a first-principles active-matter theory of dense crowds that needs no behavioural assumptions. It adds human crowds to the experimental realisations of non-reciprocal phase transitions ([[fruchart-2021-non]]) and proposes a practical early-warning signal (the emergence of a spectral peak in raw velocity fields).

## Key results

All measured unless marked:
- Mean density rises linearly to about 6 m^-2 at opening; local density reaches about 9 m^-2. Speed and density are uncorrelated locally, so a fundamental diagram does not apply.
- Velocity fluctuations rise sharply when density passes ρ* = 4.0 ± 0.5 m^-2, about 30 min before opening. Orientation correlation length grows past 10 m while speed correlation length stays a few metres.
- Kinetic-energy spectra peak at ω0 = 0.35 ± 0.05 rad/s (period about 18 s) in all four years; the peak comes from orientational oscillations (orbital motion), not from speed oscillations (no back-and-forth).
- Handedness of oscillations is ±1 with equal probability (spontaneous chiral symmetry breaking); same-handedness domains span the system.
- Frequency scales with confinement length: spectra collapse when plotted against ωL for L = 23.1, 10.0, 9.1 m (Chupinazo) and 11 m (Love Parade, density estimated 8 ± 1 m^-2). Groups oscillating together can exceed 10 tonnes.
- Theory (derived, checked against data): ∂t v = −γv + p − k u; ∂t p = −γ_p p + γ_p β v − α^2 (p × v) × p (plus a stabilising nonlinearity). Quiescent state for β < β_c = γ + k/γ_p; above it a chiral limit cycle. Integrating out p gives an overdamped particle on a Mexican-hat potential with an odd spring ±K⊥ u⊥, i.e. cyclotron-like orbits. Predicts ω0 ∝ 1/L.

## Methods and models

4K video (25 fps) from two balconies; planar homography to Google Earth reference, height correction Δx = Δx'(H − h)/H with h = 1.73 m, H = 16 ± 1 m. Heads detected with P2PNet fine-tuned on 4 annotated images (counting error < 5% versus manual); flags and balloons masked with YOLOv8. PIV with about 1.5 m windows and 0.5 s steps (error 0.05–0.1 m/s). Spectra from FFT per position, averaged; spin field from band-pass filtered velocity in ω ∈ [0.25, 0.40] rad/s. Love Parade analysis on public YouTube footage without perspective correction. Data and simulation code: https://doi.org/10.5281/zenodo.14050598. Uses trackpy for trajectories.

## Limitations and open questions

- Mean-field (spatially homogeneous) theory; the spatial structure of chiral domains and the microscopic origin of the odd friction (body deformation to propulsion) are not derived.
- One venue (four years) plus one disaster clip; crowd composition (festive, alcohol, locals) is specific. Love Parade analysis lacks perspective correction.
- The early-warning protocol is proposed, not tested prospectively.

## Relevance to us

A rare large-N, real-world measurement of a symmetry-breaking transition in a human swarm, with a compact model we could simulate in an afternoon. It shows that dense swarms of self-propelled bodies under confinement can develop coherent oscillations through non-reciprocal friction alone, which matters for dense robot swarms (for example jammed kilobot-like collectives) as much as for crowds. Methods (PIV, spectral early warning, spin-field correlation length) are directly reusable order parameters. Related: [[bain-2019-dynamic]] (same group, polarized crowds), [[helbing-2012-crowd]] (Love Parade), [[helbing-2007-dynamics]] (crowd turbulence claim it revises), [[corbetta-2023-physics]].
