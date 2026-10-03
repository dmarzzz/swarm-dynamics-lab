---
id: chiu-2025-learn
type: paper
title: "LEARN: Learning End-to-End Aerial Resource-Constrained Multi-Robot Navigation"
authors: ["Darren Chiu", "Zhehui Huang", "Ruohai Ge", "Gaurav S. Sukhatme"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2511.17765
doi: null
arxiv: "2511.17765"
cite: "Chiu, D., Huang, Z., Ge, R., & Sukhatme, G. S. (2025). LEARN: Learning End-to-End Aerial Resource-Constrained Multi-Robot Navigation. arXiv preprint arXiv:2511.17765."
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "0 (OpenAlex W7106674591, 2026-10-03)"
code: []
---

## Summary

LEARN is a lightweight, two-stage, safety-guided RL framework for multi-nano-UAV navigation in clutter. Low-resolution time-of-flight sensors and a simple motion planner are combined with a compact attention-based RL policy. In simulation it beats two state-of-the-art planners by 10% while using far fewer resources. It runs fully onboard on six Crazyflie quadrotors in indoor and outdoor scenes at up to 2.0 m/s and through 0.2 m gaps.

## Contribution

The USC follow-up to [[huang-2024-collision]] that removes the motion-capture and known-obstacle-map assumptions: fully onboard sensing and compute on nano-drones.

## Key results

- 10% better than two state-of-the-art planners in simulation with fewer resources (per the abstract).
- Fully onboard flight on 6 Crazyflies, up to 2.0 m/s, through 0.2 m gaps (measured).

## Methods and models

Two-stage safety-guided RL, attention policy, low-resolution ToF sensing and a simple planner, Crazyflie hardware.

## Limitations and open questions

Abstract-depth entry. Preprint.

## Relevance to us

The most realistic learned nano-drone swarm navigation result in this scan; a baseline for any hackathon Crazyflie work.
