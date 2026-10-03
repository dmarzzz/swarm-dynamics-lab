---
id: vasarhelyi-2018-optimized
type: paper
title: "Optimized flocking of autonomous drones in confined environments"
authors: ["Gábor Vásárhelyi", "Csaba Virágh", "Gergő Somorjai", "Tamás Nepusz", "Agoston E. Eiben", "Tamás Vicsek"]
year: 2018
venue: "Science Robotics"
url: https://hal.elte.hu/~vasarhelyi/doc/vasarhelyi2018optimized.pdf
doi: "10.1126/scirobotics.aat3536"
arxiv: null
cite: "Vásárhelyi, G., Virágh, C., Somorjai, G., Nepusz, T., Eiben, A. E., & Vicsek, T. (2018). Optimized flocking of autonomous drones in confined environments. Science Robotics, 3(20), eaat3536."
topics: [swarm-robotics, collective-motion, criticality-measurement, sync-consensus]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "498 citing papers listed by Semantic Scholar; 553 (Crossref), 2026-10-03"
code: []
---
## Summary

The paper asks how to make a Vicsek-style self-propelled flocking model work on real outdoor quadcopters that
have inertia, bounded acceleration, GPS noise of 2-3 m, about 1 s of communication delay and a finite radio
range, inside a bounded arena with obstacles. The authors keep only short-range repulsion and velocity
alignment (no explicit attraction; a soft virtual wall built from "shill" agents keeps the flock together), but
replace the usual distance-decaying alignment with an alignment term derived from an ideal braking curve: the
allowed velocity difference between two drones grows with their distance according to what an
acceleration-limited agent could still brake away. The 11 free parameters are tuned with CMA-ES against a
single fitness that multiplies six partial order-parameter scores, in a realistic simulator. They then fly 30
autonomous drones outdoors at 4, 6 and 8 m/s with no collisions, which at publication was the largest
decentralised outdoor flock with collective collision and obstacle avoidance.

## Contribution

It is the reference demonstration that a statistical-physics flocking model can be engineered into a robust
real-robot controller once motion constraints and delays are put explicitly into the interaction terms, and it
makes "model instance = model + optimised parameters" the unit of design. It builds directly on the authors'
10-drone flock ([[vasarhelyi-2014-outdoor]]) and simulation framework ([[viragh-2014-flocking]]), and sits
between idealised flocking theory (Vicsek, Reynolds, [[olfati-saber-2006-flocking]]) and later
optimisation-based aerial swarms ([[soria-2021-predictive]], [[zhou-2022-swarm]]).

## Key results

- Measured (field): 30 quadcopters, 10-15 min flights, v_flock = 4, 6, 8 m/s, arena 200-260 m, wind up to about
  40 km/h tolerated. No drone-drone, drone-wall or drone-obstacle collisions. Average nearest-neighbour distance
  12-30 m; minimum inter-agent distance stayed between about 5 and 15 m.
- Emergent patterns in the square arena: diagonal "bouncing" motion with cyclic expansion/contraction, and
  stable circular (milling) flight, quantified by a local angular-polar order parameter phi_LAP; obstacles
  break these into livelier, less correlated motion (velocity correlation drops, minimum distance does not).
- Simulation (100 agents, 10-min runs, 1 s delay, noise): best fitness 0.92, 0.87, 0.80 at 4, 6, 8 m/s;
  mean over 100 stochastic runs 0.812 +/- 0.101, 0.776 +/- 0.086, 0.728 +/- 0.075. Optimiser used population
  100 x 150 generations (15,000 evaluations), 2-6 days per run on a cluster.
- Velocity scalability: re-optimised at 16 and 32 m/s (with larger comm range and arena) giving best fitness
  0.91 and 0.89; at 32 m/s collisions (3.53 +/- 3.61 per run) vanish only when delay < 1 s and comm range
  > about 240 m (Fig. 2): a measured phase diagram of safety versus delay and range.
- Simulated flock sizes 30-1000 work, but momentum builds "pressure" against walls at large N, analogous to
  crowd crushes; obstacles inside the arena relieve it (claimed from movies, no statistics given).
- Surprising optimiser findings: a soft, spatially extended repulsion beats a hard core; close-range alignment
  should be strong and nearly distance-independent.
- Old versus new model at 4 m/s: velocity correlation 0.63 +/- 0.07 versus 0.92 +/- 0.002; mean speed
  3.37 versus 3.83 m/s.

## Methods and models

Desired velocity v_i^d = v_flock * v_i/|v_i| + sum_j v_ij^rep + sum_j v_ij^frict + sum_s v_is^wall + sum_s v_is^obst,
capped at v_max. Repulsion is a half-spring p_rep (r0_rep - r_ij) for r_ij < r0_rep. Alignment ("friction")
acts only if |v_i - v_j| exceeds v_ij^frictmax = max(v_frict, D(r_ij - r0_frict, a_frict, p_frict)), where D is a
braking curve (linear at short distance, sqrt(2 a r) at long), and then equals C_frict times the excess along
v_i - v_j. Walls and convex obstacles are represented by virtual shill agents moving inward/outward with
v_shill, coupled by the same alignment law. Robot model (from [[viragh-2014-flocking]]): delay t_del,
exponential velocity relaxation tau_CTRL, a_max, sensor refresh, comm range r_c, Langevin GPS noise, and
additive acceleration noise. Order parameters: cluster-wise velocity correlation phi_corr, collision ratio,
wall excursion, largest-cluster size, disconnected agents, mean speed; fitness is the product of sigmoid-shaped
partial fitnesses. Hardware: custom quadcopters with onboard computers, GNSS and local radio broadcast.
Code: simulator at https://github.com/csviragh/robotsim (CMA-ES via https://github.com/CMA-ES/pycma).

## Limitations and open questions

The authors list: no rigorous stability analysis in the 11-D parameter space (only statistical working ranges);
parameters must be re-optimised per platform; wall pressure at large N is unsolved. I note that the field
parameters were hand-adjusted away from the optimum for safety (more repulsion, more alignment), so the
real-flight results test a detuned instance, and the field evidence is a handful of flights rather than
replicated statistics. GNSS positions are shared by radio, so this is not purely local sensing.

## Relevance to us

This is the anchor paper for "physics flocking model to real swarm". Its order parameters and fitness design
are a ready-made measurement kit, and its delay/comm-range collision map is a concrete scaling result to
reproduce or extend in simulation. Compare with vision-only flocking ([[mezey-2025-purely]]), MPC-based
swarms ([[soria-2021-predictive]]) and planning-based swarms ([[zhou-2022-swarm]]); theory context in
[[olfati-saber-2006-flocking]] and [[tanner-2007-flocking]].
