---
id: jang-2025-reinforcement
type: paper
title: 'Reinforcement Learning-Based Oscillation Dampening: Scaling Up Single-Agent Reinforcement Learning Algorithms to a 100-Autonomous-Vehicle Highway Field Operational Test'
authors:
- Kathy Jang
- Nathan Lichtlé
- Eugene Vinitsky
- Adit Shah
- Matthew Bunting
- Matthew Nice
- Benedetto Piccoli
- Benjamin Seibold
- Daniel B. Work
- Maria Laura Delle Monache
- Jonathan Sprinkle
- Jonathan W. Lee
- Alexandre M. Bayen
year: 2025
venue: IEEE Control Systems
url: https://arxiv.org/abs/2402.17050
doi: 10.1109/mcs.2024.3503372
arxiv: '2402.17050'
cite: 'Jang, K., Lichtlé, N., Vinitsky, E., Shah, A., Bunting, M., Nice, M., Piccoli, B., Seibold, B., Work, D. B., Delle Monache, M. L., et al. (2025). Reinforcement Learning-Based Oscillation Dampening: Scaling Up Single-Agent Reinforcement Learning Algorithms to a 100-Autonomous-Vehicle Highway Field Operational Test. IEEE Control Systems, 45(1), 61–94. https://doi.org/10.1109/mcs.2024.3503372'
topics:
- crowds-and-traffic
- marl-emergence
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 10 (Crossref, 2026-10-03)
code: []
---

## Summary

Technical account of the reinforcement learning controllers deployed in the 100-AV CIRCLES field test, described as the largest field test of traffic-smoothing automated vehicles as of 2023. It covers simulator design, reward shaping, the path from simulation to deployment, safety considerations and hardware details, and reports flow-smoothing benefits in simulation and deployment.

## Contribution

Documents how single-agent RL policies trained in simulation were scaled to a real multi-vehicle deployment for collective wave dampening.

## Key results

- Reported (abstract): RL controllers deployed on 100 AVs on a highway; flow-smoothing benefits shown in simulation and deployment (magnitudes not extracted).

## Methods and models

Deep RL, simulator design and reward shaping; IEEE Control Systems Magazine 45(1), 61–94. arXiv title uses "100 AV highway field operational test"; published title differs slightly (arXiv id set because titles match closely).

## Limitations and open questions

Abstract only; quantitative field results not checked.

## Relevance to us

The most direct precedent for sim-to-real learned swarm control in human traffic. Pairs with [[wu-2022-flow]] and [[lee-2025-traffic]].
