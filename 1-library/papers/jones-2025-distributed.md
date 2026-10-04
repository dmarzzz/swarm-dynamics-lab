---
id: jones-2025-distributed
type: paper
title: "Distributed spatial awareness for robot swarms"
authors: ["Simon Jones", "Sabine Hauert"]
year: 2025
venue: "Autonomous Robots"
url: https://doi.org/10.1007/s10514-025-10228-1
doi: "10.1007/s10514-025-10228-1"
arxiv: "2411.07056"
cite: "Jones, S., & Hauert, S. (2025). Distributed spatial awareness for robot swarms. Autonomous Robots, 49(4), 41. https://doi.org/10.1007/s10514-025-10228-1"
topics: [swarm-robotics, sync-consensus]
added_by: dmarz/swarm-robotics-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "2 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex search budget exhausted during this audit)"
code: []
---

## Summary

How can robots that only see and talk to nearby neighbours agree on a shared coordinate frame? Each robot builds a small, sliding-window factor graph from its odometry and its observations of other robots, and robots exchange Gaussian belief propagation (GBP) messages within and between their graphs. As robots keep moving and meeting, the distributed graph becomes connected over time and the swarm converges on a common swarm-centric frame. The authors characterise convergence, computation and bandwidth in simulation, demonstrate shape formation and a logistics task built on the shared frame, and transfer the method to their DOTS robots with imperfect sensing.

## Contribution

A decentralised, low-cost route to global spatial information without anchors, beacons or static landmark robots, which most earlier swarm shape-formation methods needed. It brings GBP (Davison and Ortiz's "FutureMapping 2") into swarm robotics and suggests a link to best-of-n consensus via message passing.

## Key results

- Convergence (simulation, 50 seeds per point, measured): dominated by factor-graph update period and arena area; density has a small linear effect. Little gain from update rates above 10 Hz. Convergence time shows a knee where the sampling interval matches the time two robots stay within sensing range.
- Cost (measured/derived): each robot uses only a few hundred floating-point operations and a few hundred message bytes per second; the swarm converges in under 60 s in their reference arena. Bandwidth grows strongly with density.
- A convergence-time proxy based on robot encounters exceeds the true convergence time in more than 95% of 2886 converged simulations (5-100 robots, varied arena sizes).
- Shape formation (simulation, 150 robots, 7.5 m arena): each target shape emerges in about 40 s using a deliberately simple random-walk-and-aggregate rule.
- Real robots (DOTS, 1.0 m sensing radius): DSA transferred with only the uncertainty model changed; the swarm still performed when perception gaps effectively blinded two of six robots in a hexagon pattern.

## Methods and models

Table 3 parameters: max 10 variable nodes per local factor graph, new node every 0.5 s, robot diameter 0.25 m, sense/communication radius 0.5 m (1.0 m on DOTS), velocity noise 0.1 m per m travelled, position noise 0.02 m. Linear 2D factors so precisions are scalars; 32-bit floats. Simulated in a Box2D-based simulator. Videos at https://youtu.be/3S9Ko356eiY and https://youtu.be/ps5Wf-3UHr0. Preprint arXiv:2411.07056.

## Limitations and open questions

Authors' limitations: linear factors only (nonlinear needed for real-world generality), synchronous graph updates, the convergence proxy needs the swarm size, and the shape-formation rule fails with obstacles. I skimmed the introduction, results and conclusions, not the full derivations.

## Relevance to us

GBP message passing is a consensus dynamic with a measurable convergence time that depends on encounter rates, an alternative to SoNS-style hierarchy ([[zhu-2024-self]]) for giving swarms global information. A hackathon could compare GBP convergence with classical consensus (entries under the sync-consensus topic) as density and mobility vary.
