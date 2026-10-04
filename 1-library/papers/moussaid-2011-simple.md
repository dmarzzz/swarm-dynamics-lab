---
id: moussaid-2011-simple
type: paper
title: How simple rules determine pedestrian behavior and crowd disasters
authors:
- Mehdi Moussaïd
- Dirk Helbing
- Guy Theraulaz
year: 2011
venue: Proceedings of the National Academy of Sciences
url: https://arxiv.org/abs/1105.2152
doi: 10.1073/pnas.1016507108
arxiv: '1105.2152'
cite: Moussaïd, M., Helbing, D., & Theraulaz, G. (2011). How simple rules determine pedestrian behavior and crowd disasters. Proceedings of the National Academy of Sciences, 108(17), 6884–6888. https://doi.org/10.1073/pnas.1016507108
topics:
- crowds-and-traffic
- collective-motion
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 1218 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Replaces summed pairwise social forces with two vision-based heuristics. Each pedestrian computes, for every candidate direction in its field of view, the distance to first collision f(α); it picks the direction that minimises remaining distance to its goal given obstacles, and walks at a speed that keeps at least τ = 0.5 s to collision. Body contact forces act only at extreme density. The model reproduces avoidance trajectories from controlled experiments, lane formation, the empirical speed–density relation, stop-and-go waves, and crowd turbulence with a power-law displacement distribution.

## Contribution

A cognitive, heuristic alternative to force models that integrates many neighbours through a single visual field rather than superposing binary interactions, sidestepping the questions of how to sum, which neighbours count, and how to weight occluded ones. It adds a clean separation between intentional avoidance (heuristics) and unintentional physical pushing (contact forces), which is the mechanism it proposes for crowd turbulence.

## Key results

- Measured vs simulated: average avoidance trajectories in a 7.88 m x 1.75 m corridor for passing a standing person (N = 148) and an oncoming walker (N = 123) match model predictions (figure 2; parameters τ = 0.5 s, φ = 75°, d_max = 10 m, k = 5 x 10^3, v0 = 1.3 m/s).
- Simulated: spontaneous lane formation in bidirectional flow (SI).
- Simulated vs empirical: velocity–density relation in an 8 m x 3 m periodic street (6 to 96 people) agrees with field data (figure 3a).
- Simulated: stop-and-go waves for occupancy between 0.4 and 0.65 (fraction of area covered by bodies), backward propagation speed about 0.6 m/s, detected via significant correlation of local speed at x and x − 2 m with a 3 s lag.
- Simulated: at higher density, contact forces dominate and "crowd turbulence" appears near bottlenecks; displacement distribution follows a power law with exponent 1.95 ± 0.09, which the authors say agrees with the Hajj video analysis in [[helbing-2007-dynamics]].

## Methods and models

Direction: α_des minimises d(α)^2 = d_max^2 + f(α)^2 − 2 d_max f(α) cos(α0 − α). Speed: v_des = min(v0, d_h/τ). Dynamics: dv/dt = (v_des − v)/τ + Σ f_ij/m + Σ f_iW/m, with contact f_ij = k g(r_i + r_j − d_ij) n_ij. Body radius r = m/160 with mass uniform in [60, 100] kg. Experiments: Bordeaux 2006, 40 naive participants, three cameras at 12 fps, trajectories smoothed over 10 frames. Crowd "pressure" P(x) = ρ(x) Var(V(x,t)) as in [[helbing-2007-dynamics]], Gaussian-weighted local fields with R = 0.7 m.

## Limitations and open questions

- Single-pedestrian validation is limited to two simple two-person scenarios; collective predictions are compared to aggregate data only. Several collective claims (lanes, turbulence) are simulation results, not tested against tracked high-density data.
- The heuristic chooses the best direction greedily each step; it has no explicit anticipation of others' future moves beyond constant-velocity extrapolation (contrast [[karamouzas-2014-universal]], [[bonnemain-2023-pedestrians]], [[murakami-2021-mutual]]).
- Turbulence exponent agreement rests on one disaster video analysis.

## Relevance to us

A swarm model whose interaction is defined through a perception field (visual collision-distance map) instead of metric or topological neighbour lists; directly useful for vision-based robot swarms, as the authors note. The paper also gives operational definitions (local speed, crowd pressure, stop-and-go correlation) that we can reuse as order parameters. Pairs with [[helbing-1995-social]] (what it replaces) and [[rio-2018-local]] (an alignment-based alternative inferred from virtual-reality experiments).
