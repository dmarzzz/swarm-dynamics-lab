---
id: tan-2025-go
type: paper
title: "GO-Flock: Goal-Oriented Flocking in 3D Unknown Environments with Depth Maps"
authors: ["Yan Rui Tan", "Wenqi Liu", "Wai Lun Leong", "John Guan Zhong Tan", "Wayne Wen Huei Yong", "Shaohui Foong", "Fan Shi", "Rodney Swee Huat Teo"]
year: 2025
venue: "2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)"
url: https://arxiv.org/abs/2510.05553
doi: "10.1109/iros60139.2025.11246049"
arxiv: "2510.05553"
cite: "Tan, Y. R., Liu, W., Leong, W. L., Tan, J. G. Z., Yong, W. W. H., Foong, S., Shi, F., & Teo, R. S. H. (2025). GO-Flock: Goal-Oriented Flocking in 3D Unknown Environments with Depth Maps. In 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) (pp. 2598-2605). IEEE."
topics: [swarm-robotics, collective-motion]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (OpenAlex W4416750379, 2026-10-03); 1 (Crossref, 2026-10-03)"
code: []
---

## Summary

Artificial-potential-field (APF) flocking tends to deadlock and fall into local minima in clutter, and fixes are usually passive and slow. GO-Flock adds a perception module that turns depth maps into waypoints and virtual agents for obstacle avoidance, then a collective-navigation module with a new APF strategy for flocking in cluttered 3-D space. It is compared against passive APF approaches and validated in obstacle-filled simulations and hardware-in-the-loop forest flights with nine drones (six physical, three virtual).

## Contribution

A hybrid planning-plus-reactive flocking design that tackles the classic APF local-minimum problem in 3-D clutter.

## Key results

- Overcomes local minima where passive APF approaches stall (per the abstract).
- Hardware-in-the-loop flocking of 9 drones (6 physical, 3 virtual) in a forest.

## Methods and models

Depth-map perception to waypoints and virtual agents, plus a modified APF collective-navigation controller. The arXiv author list omits Shaohui Foong; I use the IROS author list.

## Limitations and open questions

Abstract-depth entry. Partly virtual agents in the hardware test.

## Relevance to us

A hand-designed flocking-in-clutter baseline; compare [[choi-2026-communication]] (learned) and [[horyna-2024-fast]].
