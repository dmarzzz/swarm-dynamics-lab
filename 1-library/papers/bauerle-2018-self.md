---
id: bauerle-2018-self
type: paper
title: "Self-organization of active particles by quorum sensing rules"
authors: ["Tobias Bäuerle", "Andreas Fischer", "Thomas Speck", "Clemens Bechinger"]
year: 2018
venue: "Nature Communications"
url: https://doi.org/10.1038/s41467-018-05675-7
doi: "10.1038/s41467-018-05675-7"
arxiv: null
cite: "Bäuerle, T., Fischer, A., Speck, T., & Bechinger, C. (2018). Self-organization of active particles by quorum sensing rules. Nature Communications, 9(1), 3232."
topics: ["active-matter", "collective-motion", "collective-decision"]
added_by: dmarz/active-matter
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "185 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Bäuerle, Fischer, Speck and Bechinger give light-driven Janus colloids an artificial quorum-sensing rule. A camera
locates every particle at 2 Hz, a computer evaluates a virtual signalling-molecule concentration at each particle,
c_i = c̃ Σ_j (σ/r_ij) exp(−r_ij/λ), and a scanned laser makes the particle motile (v₀ = 0.2 µm/s) when c_i < c_th and
purely Brownian when c_i > c_th. Only the speed is controlled; the heading still diffuses freely. Clusters of
non-motile particles surrounded by a motile gas form only inside a window of thresholds, at a density (about 15 % of
close packing) and speed where constant-motility particles do not cluster at all. Brownian-dynamics simulations and a
mean-field theory reproduce the cluster density and radius, and anisotropic or two-threshold rules give ring,
ellipse and square-shaped aggregates.

## Contribution

The first experimental system with a programmable, per-particle density-dependent motility rule, i.e. a direct
realisation of the v(ρ) input of MIPS theory ([[tailleur-2008-statistical]], [[cates-2015-motility]]) but with a
sharp on/off switch and a tunable sensing range λ. It shows that the switching dynamics at the cluster interface,
not just the coexistence of motile and passive particles, is what drives aggregation. Precursor of the
feedback-controlled colloid work in [[lavergne-2019-group]] (same group, vision-cone rules).

## Key results

- Measured: with c_th = 0 (all Brownian) and c_th = ∞ (all motile) the suspension stays homogeneous; clusters
  (ρ > 1.2ρ₀) form for intermediate thresholds, e.g. c_th = 5.9, 7.3, 8.6 c̃ at λ = 10σ. Raising c_th makes clusters
  smaller and denser.
- Measured and simulated: cluster density ρ_c and radius r* versus c_th and λ agree between experiment and
  simulation; mean-field theory gets the lower clustering boundary but badly overestimates the upper one.
- Simulated: clusters smaller than N_p ≈ 65 passive particles dissolve and re-form spontaneously, independent of λ
  (the number depends on system size), which sets the upper stability boundary.
- Simulated: fixed mixtures of motile and non-motile particles without switching never cluster at this packing
  fraction, whatever the ratio. Clustering needs a minimum total switching rate, which peaks at intermediate c_th.
- Measured: a second threshold c_th,2 (motile again at very high c) gives rings; an angular weight f(Θ) = cos⁴Θ gives
  ellipses, sin⁴Θ rotates them by 90°, cos⁴(2Θ) gives squares.
- Mean-field theory: passive core plus active gas, polarization decays as a modified Bessel function K₁(r/ξ) with
  ξ = (v²/(2D₀²) + D_R/D₀)^(−1/2).

## Methods and models

Silica spheres σ = 4.4 µm with a 30 nm carbon cap in a near-critical water–lutidine mixture; laser intensity
0.2 W/mm² for motion, onset at 0.1 W/mm²; acousto-optic deflector illuminates each particle 8 µs every 4 ms, so up
to 400 particles can be addressed; motility updated every 500 ms; circular confinement R = 65 µm holding about
122 particles (ρ₀ = 0.0092 µm⁻²) with reflective walls implemented by off-centre illumination torques. Measured
D₀ = 0.0208 µm²/s. Simulations: overdamped ABPs with WCA repulsion (ε = 100 k_BT), D_R = 1/120 s⁻¹, Δt = 40 ms,
N = 132 in confinement or N = 1000 periodic. No code released; data on request. Full text read from the
open-access Nature Communications page.

## Limitations and open questions

- Sensing and actuation are external (camera plus laser), so this is centralised computation of a local rule, the
  same architecture as a motion-capture robot arena, not autonomous sensing.
- Small systems (about 120 particles), one global density and one speed; no systematic finite-size study beyond the
  supplementary note that the dissolution size depends on system size.
- Mean-field theory neglects excluded volume and fluctuations, which matter most for small clusters.
- Only the speed is modulated; heading responses, delays and non-reciprocal rules are proposed but not tested here.

## Relevance to us

A direct template for a swarm quorum rule: each agent stops when a distance-weighted neighbour count exceeds a
threshold. The paper gives the phase window (threshold versus sensing range), the minimum stable cluster size and the
failure mode (small clusters evaporate). The MIPS criterion v'/v < −1/ρ from [[cates-2015-motility]] is the
smooth-rule counterpart. Related: [[lavergne-2019-group]], [[ziepke-2025-acoustic]], [[ziepke-2022-multi]],
[[fily-2012-athermal]].

## Notes from dmarz/active-matter-audit

Audit 2026-10-03: the entry was at abstract depth with citations "0 (Semantic Scholar)", which was wrong (OpenAlex
gives 185). I read the full open-access article and rewrote Summary through Relevance with the paper's numbers, and
raised read_depth to full. Metadata (title, authors, volume 9, article 3232) confirmed against Crossref/OpenAlex.
