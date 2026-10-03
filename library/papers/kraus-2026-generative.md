---
id: kraus-2026-generative
type: paper
title: "Generative adversarial imitation learning for robot swarms: Learning from human demonstrations and trained policies"
authors: ["Mattes Kraus", "Jonas Kuckling"]
year: 2026
venue: "arXiv preprint (accepted at ICRA 2026)"
url: https://arxiv.org/abs/2603.02783
doi: null
arxiv: "2603.02783"
cite: "Kraus, M., & Kuckling, J. (2026). Generative adversarial imitation learning for robot swarms: Learning from human demonstrations and trained policies. arXiv preprint arXiv:2603.02783 (ICRA 2026)."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "not retrieved (Semantic Scholar rate-limited). OpenAlex daily budget exhausted on this IP during the session."
code: []
---

## Summary

A GAIL-based framework that learns collective behaviours for robot swarms from demonstrations, including manual human demonstrations rather than only rollouts of an existing policy. Across six missions, learning from human demonstrations and from PPO-policy demonstrations gives qualitatively meaningful behaviours that perform similarly to the demonstrations. Learned policies deployed on a TurtleBot 4 swarm keep their visually recognisable character and reach performance comparable to simulation.

## Contribution

It lets swarm designers specify behaviour by demonstration rather than reward or rule design, filling a gap in swarm imitation learning (Kuckling, automatic-design community).

## Key results

- Imitated behaviours perform similarly to demonstrations across six missions (simulation, per the abstract).
- Real TurtleBot 4 swarm deployment with performance comparable to simulation.

## Methods and models

Generative adversarial imitation learning with demonstrations from humans and from PPO policies; real-robot TurtleBot 4 experiments.

## Limitations and open questions

Abstract-depth entry. Number of robots and mission details not in the abstract.

## Relevance to us

An alternative design route for hackathon swarm behaviours; compare discovery ([[mattson-2025-discovery]]) and behaviour metrics ([[jesus-2026-how]]).
