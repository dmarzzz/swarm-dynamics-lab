---
id: mallmann-trenn-2021-crowd
type: paper
title: "Crowd Vetting: Rejecting Adversaries via Collaboration With Application to Multirobot Flocking"
authors: ["Frederik Mallmann-Trenn", "Matthew Cavorsi", "Stephanie Gil"]
year: 2021
venue: "IEEE Transactions on Robotics"
url: https://arxiv.org/pdf/2012.06291
doi: "10.1109/tro.2021.3089033"
arxiv: "2012.06291"
cite: "Mallmann-Trenn, F., Cavorsi, M., & Gil, S. (2021). Crowd Vetting: Rejecting Adversaries via Collaboration With Application to Multirobot Flocking. IEEE Transactions on Robotics, 38(1), 5-24. arXiv:2012.06291."
topics: [sybil-resistance, swarm-robotics, sync-consensus, collective-motion]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "33 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Each robot gets a noisy per-message trust observation X in [0,1] about whether a neighbour's transmission is unique (from the Wi-Fi fingerprint of [[gil-2015-guaranteeing]]), with expectation at least 1/2+epsilon in the right direction. FindSpoofedRobots: every robot first forms an interim trust vector by majority over r rounds of its own observations, then exchanges interim vectors and re-decides each neighbour j by majority vote among the robots it trusts that are also neighbours of j. The authors bound the number of rounds needed for all legitimate robots to hold the correct trust vector with probability 1-delta, and apply it to flocking around a moving target that spawning adversaries try to free.

## Contribution

Shows that second-hand opinions ("crowd vetting") collapse the time to detect Sybil identities: on a complete graph with 10 spoofed robots per legitimate one, the required rounds become a constant independent of team size, whereas any scheme that does not share opinions needs Omega(log n / epsilon^2) observations (proved lower bound). Also shows that a Sybil attack creates a false sense of resilience: fake nodes inflate apparent graph robustness so W-MSR [[leblanc-2013-resilient]] and related methods believe they tolerate an adversary they cannot.

## Key results

- Theorem 1: rounds r* depend on epsilon, max legitimate degree d_L and tau, the "tau-triangular" gap between legitimate and hidden-adversary common neighbours; requires tau > 0, which the authors show is necessary.
- Table I (empirical, complete graph, h = l/2 hidden adversaries, s = 10 l spoofers, epsilon = 1/3): Baseline needs 22, 32, 43 rounds for l = 10, 100, 1000; FindSpoofedRobots needs 10, 7, 6.
- Spawned identities can exceed legitimate robots in number; only hidden adversaries (real compromised robots that do not spoof) must stay below legitimate common neighbours.
- Example network (Fig. 5, 12 real plus 2 spoofed): perceived tolerance of W-MSR, fault identification and distributed function calculation is 1 adversary, actual is 0 (Table II). In 1000 random networks the algebraic connectivity looks higher with spoofed nodes present (Fig. 7).
- Flocking (ROS/Gazebo, 13 robots, 3 hacked at t = 10 s each spawning 1 spoof): without the algorithm the target escapes; with it the spoofs are rejected inside the derived escape window Delta = (u_max - vel_cen) / (k_ref (u_max + vel_cen)).

## Methods and models

Probabilistic analysis with Azuma-Hoeffding and binomial tail bounds, (epsilon, delta) identity-testing lower bound, anytime doubling schedule when r* is unknown, FindResilientAdjacencyMatrix built on trusted vectors, Reynolds-style flocking controller with reference, avoidance and velocity-matching terms.

## Limitations and open questions

Assumes the physical trust observations are independent across messages and time and that hidden adversaries cannot fake them; detection is only for identities whose radio signature is non-unique. Synchronous rounds, static membership during the algorithm. Simulation only for flocking.

## Relevance to us

The closest robotics analogue of reputation gossip in agent swarms. Two transferable results: (1) neighbour opinion sharing turns a log n detection cost into a constant when the graph has many triangles, so dense local agent topologies should help Sybil detection; (2) Sybils not only add votes, they corrupt the topology estimates that resilience guarantees rely on. Extended in [[cavorsi-2023-dynamic]] and [[yemini-2021-characterizing]]; compare the accusation-matching approach of [[wardega-2023-byzantine]].

## Notes from dmarz/sybil-foundations

Bibliographic detail from Crossref (2026-10-03): IEEE Transactions on Robotics 38(1), 5-24, issue dated February 2022; 29 Crossref citations. Found independently as a forward citation of [[douceur-2002-sybil]] on Semantic Scholar, which places this line of work in the classical Sybil literature as well as in robotics. The flocking scenario (three robots hacked at t = 10 s, each spawning one spoofed robot that pushes legitimate robots out of the convergence range) is a ready-made attack template for swarm experiments.
