---
id: wu-2022-flow
type: paper
title: 'Flow: A Modular Learning Framework for Mixed Autonomy Traffic'
authors:
- Cathy Wu
- Abdul Rahman Kreidieh
- Kanaad Parvate
- Eugene Vinitsky
- Alexandre M. Bayen
year: 2022
venue: IEEE Transactions on Robotics
url: https://arxiv.org/abs/1710.05465
doi: 10.1109/tro.2021.3087314
arxiv: '1710.05465'
cite: 'Wu, C., Kreidieh, A. R., Parvate, K., Vinitsky, E., & Bayen, A. M. (2022). Flow: A Modular Learning Framework for Mixed Autonomy Traffic. IEEE Transactions on Robotics, 38(2), 1270–1286. https://doi.org/10.1109/tro.2021.3087314'
topics:
- crowds-and-traffic
- marl-emergence
- swarm-robotics
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 174 (Crossref, 2026-10-03)
code: []
---

## Summary

Presents Flow, a modular framework that couples deep reinforcement learning with microscopic traffic simulation to study mixed autonomy, where a small fraction of vehicles is automated. Modules capture stop-and-go jams, lane changes and intersections. Learned controllers improve system-level velocity by up to 57% with only 4–7% AV adoption, and in single-lane ring traffic a small neural policy using only local observations eliminates stop-and-go waves, beats all known model-based controllers, and generalises to unseen densities.

## Contribution

Established deep RL as a tool for designing sparse "Lagrangian" controllers of a human-driven swarm, turning the ring-road experiments ([[sugiyama-2008-traffic]], [[stern-2018-dissipation]]) into benchmark RL environments.

## Key results

- Simulated (abstract): up to 57% higher system velocity at 4–7% AV penetration.
- Simulated: a local-observation neural policy removes stop-and-go waves on the ring, reaching near-optimal performance and generalising across densities.

## Methods and models

Deep RL in microscopic traffic simulation with modelled human drivers (car-following models such as IDM, [[treiber-2000-congested]], are the usual choice; specifics not read); IEEE Transactions on Robotics 38(2), 1270–1286. Code: https://github.com/flow-project/flow (GitHub API, 2026-10-03: MIT licence, 1191 stars, last push 2024-07-27; not run).

## Limitations and open questions

Sim-to-real gap; human models are simplified; results are simulation-only until the field tests in [[jang-2025-reinforcement]]. Abstract only.

## Relevance to us

Ready-made environment for learned swarm control with a well-defined collective objective. Directly usable for a hackathon experiment on whether learned policies beat [[stern-2018-dissipation]]'s hand-designed controllers. Code repo for the code scan task.
