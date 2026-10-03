---
id: sun-2023-mean
type: paper
title: "Mean-shift exploration in shape assembly of robot swarms"
authors: ["Guibin Sun", "Rui Zhou", "Zhao Ma", "Yongqi Li", "Roderich Groß", "Zhang Chen", "Shiyu Zhao"]
year: 2023
venue: "Nature Communications"
url: https://www.nature.com/articles/s41467-023-39251-5
doi: "10.1038/s41467-023-39251-5"
arxiv: null
cite: "Sun, G., Zhou, R., Ma, Z., Li, Y., Groß, R., Chen, Z., & Zhao, S. (2023). Mean-shift exploration in shape assembly of robot swarms. Nature Communications, 14(1), 3476."
topics: [swarm-robotics, sync-consensus]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "88 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Shape assembly methods either assign each robot a goal cell (centralised assignment does not scale;
distributed assignment needs conflict resolution) or avoid assignment but move slowly or imprecisely (edge
following in [[rubenstein-2014-programmable]], Turing patterns in [[slavkov-2018-morphogenesis]]). This paper
removes goal assignment entirely. Each robot sums three velocity commands: a shape-entering term that descends
a grey-level distance transform of the target image, a shape-exploring term that moves toward the
kernel-weighted mean of nearby unoccupied target cells (the mean-shift algorithm from machine learning), and an
interaction term with repulsion plus velocity alignment. Robots also agree on the shape's position and
orientation by finite-time consensus, so a few informed robots can steer a moving shape. With 50 holonomic
ground robots they assemble a snowflake and other non-convex shapes, regrow a removed starfish arm, transport a
cargo by encircling it, and flood a maze.

## Contribution

A simple, assignment-free, scalable local rule for shape formation whose key ingredient (robots inside the
shape keep moving toward free space) removes the jamming that stops other methods. It belongs to the
pattern-formation line ([[rubenstein-2014-programmable]], [[slavkov-2018-morphogenesis]]) and to
consensus-based formation control ([[olfati-saber-2004-consensus]], [[ren-2005-consensus]]).

## Key results

- Measured: snowflake (6 major and 18 minor branches) reaches 100% coverage with the exploring term; without
  it coverage drops to 75% as robots stall at the boundary.
- Simulated comparison (10 trials each): similar convergence time to an assignment-based method and an
  assignment-free saliency method at N = 20, but at N = 300 the proposed method converges at least 20 times
  faster.
- Simulated robustness (512 runs): coverage above 93% and entering rate 100% for n_cell/n_robot from 0.45 to
  128; convergence time rises only mildly from N = 16 to 1024.
- Measured: starfish regrows an arm after robots are removed, with no reassignment; 2 informed robots out of 8
  steer cargo transport; 7 informed robots out of 128 suffice for a moving shape in simulation.

## Methods and models

Kinematic agents p_i' = v_i = v_ent + v_exp + v_int. Shape-entering: kappa1 xi_rho (p_T - p_i)/|p_T - p_i| plus
the negotiated shape velocity. Shape-exploring (mean shift): weighted mean of (p_rho - p_i) over unoccupied
black cells within r_sense, weight psi(z) = (1 + cos(pi z))/2. Interaction: kappa3 sum mu(|p_i - p_j|)(p_i - p_j)
with mu = r_avoid/|p_i - p_j| - 1 inside r_avoid, minus the mean velocity difference to neighbours. Negotiation:
finite-time consensus p_dot = -(c1/|N_i|) sum sign(.)|.|^alpha + mean neighbour velocity with 0 < alpha < 1.
Metrics: coverage rate, entering rate, distribution uniformity, velocity polarisation. Hardware: 50 "Rainbow"
holonomic robots; positions come from motion capture, and each robot's controller runs as a separate thread on
a workstation using only its local information. Code for the human-swarm interface:
https://github.com/WestlakeAerialRobotics/Human-swarm-interface (Zenodo 10.5281/zenodo.7960508). Data on request.

## Limitations and open questions

Authors: shapes must be a single connected component; all robots need a common global reference frame (GPS or
motion capture); the hardware experiments are not on-board. I add: the comparison with prior methods is in
simulation only and the uniformity metric is weakly defined; no analysis of how sensing radius trades off
against speed.

## Relevance to us

A strong baseline for any shape-formation or coverage task, simple enough to reimplement in an afternoon, and
a nice example of an ML primitive (mean shift) turned into a local swarm law. Pair with
[[rubenstein-2014-programmable]] for the minimal-sensing contrast and with [[elamvazhuthi-2019-mean]] for
density-level analysis.
