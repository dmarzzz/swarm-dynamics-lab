---
id: brambati-2025-learning
type: paper
title: Learning to flock in open space by avoiding collisions and staying together
authors: [Martino Brambati, Antonio Celani, Marco Gherardi, Francesco Ginelli]
year: 2025
venue: "Journal of Statistical Mechanics: Theory and Experiment"
url: https://arxiv.org/html/2506.15587
doi: 10.1088/1742-5468/ae4969
arxiv: '2506.15587'
cite: 'Brambati, M., Celani, A., Gherardi, M., & Ginelli, F. (2026). Learning to flock in open space by avoiding collisions and staying together. Journal of Statistical Mechanics: Theory and Experiment, 2026(3), 033501. arXiv:2506.15587 (first posted 2025).'
topics: [marl-emergence, collective-motion, criticality-measurement]
added_by: dmarz/marl-emergence
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "3 (Semantic Scholar, 2026-10-03); 1 (Crossref, 2026-10-03)"
code: []
---

## Summary

A finite group of self-propelled agents in unbounded 2D space must stay cohesive, which pure alignment cannot do.
Each agent sees its Voronoi (topological) neighbours, and at each step picks a coupling beta in [0,1] that mixes
alignment with the neighbours' mean heading (beta = 0, topological Vicsek) and attraction toward their centre of
mass (beta = 1). The state is the agent's mean neighbour distance d; the cost is the change in a soft
Lennard-Jones-like potential L(d) = a/d - b/sqrt(d), which penalises both crowding and separation. Tabular
Q-learning, centralised (shared Q) or decentralised (one Q per agent), yields cohesive flocks with polar order
about 0.95 and starling-like structure. Removing the short-range penalty yields disordered cohesive swarming
instead, so collision avoidance, not cohesion alone, is what makes alignment optimal.

## Contribution

Extends [[durve-2020-learning]] from periodic boxes and a single heading-difference state to open space,
topological neighbours and a learned alignment-versus-attraction trade-off. Gives a learning-based answer to
"why flock rather than swarm?" and checks the learned flocks against empirical starling observables
(pair correlation, neighbour mixing rate), which ML-side MARL papers almost never do.

## Key results

- N = 100, centralised training (300 episodes) and decentralised (1000 episodes): cohesive flocks with mean
  distance to centre of mass about 2 and time-averaged polar order about 0.95 (measured). Centralised training
  settles in about 30 episodes.
- Finite-size scaling up to N = 1600: centralised policies keep order near 0.94 with flock size growing as
  sqrt(N) (constant density); decentralised training degrades to order about 0.84 and partial loss of cohesion
  at N = 1600 because individual agents under-explore states; changing exploration and learning exponents
  (nu = 0.5, omega = 0.99) partly fixes this.
- Order falls with orientational noise, with a transition to swarming (order ~ 1/sqrt(N)) near eta_c ~ 1; not
  analysed further.
- Learned policy: pure alignment (beta ~ 0) for d < d* ~ 2 (near the cost's inflection at 16/9), and an
  essentially arbitrary alignment-attraction mix at larger d; replacing large-d actions with random beta still
  flocks ("policy distillation"). This mirrors zonal models (Aoki, Couzin) without assuming them.
- Shifting the cost so small distances are not penalised (z = 1) gives attraction-dominated cohesive swarming;
  flocking survives up to a shift z_c ~ 0.6.
- Structure: neighbour mixing rate about 5e-2, pair distribution g(r) with a single peak near r ~ 0.5 and no
  further structure, qualitatively like starling flocks. Using Voronoi-cell area as the cost argument (to
  reward being interior) changes nothing qualitatively.

## Methods and models

r_i(t+1) = r_i(t) + v0 s_i(t+1), v0 = 0.2; s_i(t+1) = Theta[(1 - beta) V_i + beta R_i + eta xi_i] with V_i the
normalised mean heading and R_i the normalised direction to the centre of mass of Voronoi neighbours, eta = 0.3.
State d discretised in 20 bins of 0.2 (last bin d > 4); 11 actions beta in {0, 0.1, ..., 1}. Cost
c = L(d(t+1)) - L(d(t)), a = 1, b = 2 (minimum at d = 1). Myopic update Q <- Q + alpha [c - Q], visit-count
decaying learning rate alpha_0 / (1 + Omega/Omega_0)^omega and exploration (1 + Omega/Omega_0)^-nu, alpha_0 =
0.005, nu = omega = 0.7. Episodes of T = 20N steps, agents initialised in a disc of radius 10 sqrt(2).
No code link given in the paper.

## Limitations and open questions

Still a one-dimensional state (mean neighbour distance) and myopic, bandit-like updates, so the "policy" is a
lookup of beta versus d; no recurrent or deep policy. 2D only. The noise-driven transition and the
flocking-to-swarming transition in z are mentioned but not characterised, which is an obvious opening. No
predators, heterogeneity or leaders, which the authors list as future work.

## Relevance to us

Probably the closest prior art to any "learn a flocking rule, then measure its physics" hackathon project. Two
transitions it leaves open (in noise eta and in short-range penalty z) are cheap to map with its tabular setup.
Read with [[durve-2020-learning]], the active-matter RL review [[cai-2025-reinforcement]], and
[[huttenrauch-2019-deep]] for a deep-RL encoder that could replace the one-dimensional state.

## Notes from dmarz/marl-emergence-audit

Audited 2026-10-03 against Crossref (10.1088/1742-5468/ae4969) and the arXiv PDF of 2506.15587. Corrected the
journal name to "Journal of Statistical Mechanics: Theory and Experiment" in venue and cite. Crossref gives the
journal version as 2026, 2026(3), article 033501; the `year: 2025` field and the id follow the first arXiv posting,
which the cite string already explains. All numbers in Key results and Methods (order 0.95 / 0.94 / 0.84, N up to
1600, eta_c ~ 1, z_c ~ 0.6, d = 16/9, mixing rate 5e-2, v0 = 0.2, eta = 0.3, alpha_0 = 0.005, nu = omega = 0.7,
T = 20N) match the paper. read_depth full is consistent with the content.
