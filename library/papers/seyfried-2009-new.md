---
id: seyfried-2009-new
type: paper
title: New Insights into Pedestrian Flow Through Bottlenecks
authors:
- Armin Seyfried
- Oliver Passon
- Bernhard Steffen
- Maik Boltes
- Tobias Rupprecht
- Wolfram Klingsch
year: 2009
venue: Transportation Science
url: https://arxiv.org/abs/physics/0702004
doi: 10.1287/trsc.1090.0263
arxiv: physics/0702004
cite: Seyfried, A., Passon, O., Steffen, B., Boltes, M., Rupprecht, T., & Klingsch, W. (2009). New Insights into Pedestrian Flow Through Bottlenecks. Transportation Science, 43(3), 395–406. https://doi.org/10.1287/trsc.1090.0263
topics:
- crowds-and-traffic
- collective-motion
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: full
relevance: 3
citations: 419 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

Laboratory experiment at Forschungszentrum Jülich in which groups of 20, 40 and 60 people, starting at density 3.3 m^-2, walk "purposefully but without haste" through a 2.8 m long bottleneck whose width is varied from 0.8 to 1.2 m in 0.1 m steps (18 runs). Hand-tracked head trajectories give time gaps, densities and speeds inside the bottleneck. Flow grows linearly and continuously with width, not stepwise; lanes form through a "zipper" effect but their spacing grows continuously with width. Combined with other groups' data, the large disagreements between capacity guidelines are traced mainly to differing initial densities in front of the bottleneck.

## Contribution

A careful empirical correction to engineering practice: it refutes the claim (Hoogendoorn and Daamen) that bottleneck capacity grows in steps as extra lanes appear, supports the specific-flow concept (capacity proportional to width), and argues that a jam can form upstream of a bottleneck even when the incoming flow is below the capacity defined by the fundamental diagram maximum. It is part of the Jülich programme of controlled pedestrian experiments that also produced [[seyfried-2005-fundamental]].

## Key results

All measured:
- Specific flow J_s = ΔN/(Δt b) for N = 60 rises slightly from 1.61 (b = 0.8 m) to 1.97 (ms)^-1 (b = 1.2 m); for N = 20 and 40 values scatter between 1.77 and 2.31 (ms)^-1 (table 2), well above handbook capacities of 1.2 to 1.6 (ms)^-1.
- For b ≥ 0.9 m the lateral position distribution is bimodal (two lanes); lane separation grows continuously with b, and time-gap distributions broaden and shift smaller, with no evidence of stepwise changes except the one-to-two-lane transition.
- Fitted stationary values inside the bottleneck: v_stat between 0.94 and 1.22 m/s and ρ_stat between 1.42 and 1.73 m^-2 (table 3); for b ≥ 1.0 m a stationary state is not reached even with N = 60.
- Density in the jam 1 m in front of the bottleneck fluctuates between 4 and 6 m^-2 independent of width.
- Across five experimental datasets (Kretz, Muir, Müller, Nagai, this study), flow is compatible with a linear increase in width; Nagai's data show flow at b = 1.2 m rising from 1.04 to 3.31 s^-1 when initial density increases from 0.4 to 5 m^-2, explaining much of the spread.
- Claimed: capacity estimates in guidelines (SFPE, Weidmann, Predtechenskii–Milinskii) differ among themselves by up to a factor of two, and from experiments by up to a factor of four.

## Methods and models

Bottleneck built from desks in the Jülich "Rotunde" auditorium; two overhead cameras (25 fps PAL); head centres marked manually every second frame (80 ms) in Adobe After Effects, rectified to metric coordinates. Quantities: individual time gaps Δt_i at the bottleneck centre (J = 1/⟨Δt_i⟩), individual speeds from finite differences over ±2 points, density n(t)/b in a 1 m long measurement section. Relaxation to stationarity fitted with f(t) = f_stat + A exp(−t/τ) using MINUIT. No simulation model.

## Limitations and open questions

- Small groups (N ≤ 60) and a homogeneous student/staff population; for wide bottlenecks the stationary state is not reached, so stationary values are extrapolations without error margins.
- Normal-motivation walking only; competitive or pushing behaviour (see [[pastor-2015-experimental]]) is excluded by design.
- Trajectories hand-annotated; later Jülich work automated tracking (PeTrack) and extended to larger datasets.

## Relevance to us

A clean empirical baseline for flow through a constriction at normal motivation: linear capacity in width, zipper-like lane interleaving, and the dominant role of the upstream density. Any swarm-through-doorway experiment (robots or simulated agents) should report the same quantities (time gaps, specific flow, lane positions). Compare with [[zuriguel-2014-clogging]] and [[helbing-2000-simulating]] for the competitive regime, and [[corbetta-2023-physics]] for context.
