---
id: valentini-2016-collective
type: paper
title: "Collective decision with 100 Kilobots: speed versus accuracy in binary discrimination problems"
authors: ["Gabriele Valentini", "Eliseo Ferrante", "Heiko Hamann", "Marco Dorigo"]
year: 2016
venue: "Autonomous Agents and Multi-Agent Systems"
url: "https://kops.uni-konstanz.de/server/api/core/bitstreams/53000cb3-3f1e-434d-8347-8243ed76b370/content"
doi: "10.1007/s10458-015-9323-3"
arxiv: null
cite: "Valentini, G., Ferrante, E., Hamann, H., & Dorigo, M. (2016). Collective decision with 100 Kilobots: speed versus accuracy in binary discrimination problems. Autonomous Agents and Multi-Agent Systems, 30(3), 553–580. https://doi.org/10.1007/s10458-015-9323-3"
topics: ["collective-decision", "swarm-robotics", "swarm-intelligence"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "152 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Proposes and analyses Direct Modulation of Majority-based Decisions (DMMD): robots alternate between exploring the site matching their opinion and disseminating that opinion for a time proportional to the sampled quality, then adopt the majority opinion of their neighbours. Tested on 100 Kilobots choosing between two sites (qualities 1 and 0.5) and analysed with ODE and Gillespie chemical-reaction-network models, the main finding is that neighbourhood size controls the speed-accuracy trade-off.

## Contribution

One of the first large physical robot swarm demonstrations of a quality-based collective discrimination task, and a clean comparison of majority rule versus voter model under the same positive-feedback modulation. It is the experimental anchor of the best-of-n framework reviewed in [[valentini-2017-best]].

## Key results

- More than 20 independent Kilobot runs (about 35 h of robot experiments) with rho_a = 1, rho_b = 0.5 reached a broad majority for the better site; full 100 per cent consensus was rarely observed.
- Larger neighbourhood sizes give faster but less accurate decisions; with G_max = 25 the swarm reached 90 per cent consensus faster than with G_max = 5 (95 per cent CI for convergence about t = 55 to 69 for G_max = 25).
- Odd neighbourhood sizes in the majority rule give higher accuracy than even ones.
- Majority rule is about 1.89 times faster than the weighted voter model in the robot scenario but less accurate except on the hardest problems (rho_b = 0.9).
- Consensus states are the only asymptotically stable equilibria of the ODE model; model and robot data agree after a linear time rescaling t' = 3t + g.

## Methods and models

Kilobots (simple vibration-driven robots with infrared messaging) in an arena with two sites signalled by beacons and a light gradient; probabilistic finite-state controller (exploration, dissemination). Macroscopic ODE for opinion fractions under majority rule with group size G; finite-size chemical reaction network simulated with the Gillespie algorithm. Estimated exploration rate sigma = 6.072, g = 8.4.

## Limitations and open questions

Binary choice only; site qualities are broadcast numbers rather than sensed properties; the well-mixed assumption breaks down when spatial correlations form. Skim-level reading: we did not check every appendix result.

## Relevance to us

A concrete, reproducible baseline for any kilobot or simulated-agent decision experiment. The neighbourhood-size trade-off connects to the less-is-more result [[talamali-2021-when]] and to the network-connectivity trade-off [[reina-2024-speed]]. Compare quorum steepness effects in [[sumpter-2009-quorum]].
