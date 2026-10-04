---
id: vega-2024-agent
type: paper
title: "Agent-Based Emulation for Deploying Robot Swarm Behaviors"
authors: ["Ricardo Vega", "Kevin Zhu", "Connor Mattson", "Daniel S. Brown", "Cameron Nowzari"]
year: 2024
venue: "arXiv preprint (submitted to ICRA 2025)"
url: https://arxiv.org/abs/2410.16444
doi: null
arxiv: "2410.16444"
cite: "Vega, R., Zhu, K., Mattson, C., Brown, D. S., & Nowzari, C. (2024). Agent-Based Emulation for Deploying Robot Swarm Behaviors. arXiv preprint arXiv:2410.16444."
topics: [swarm-robotics]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (OpenAlex W4404260869, 2026-10-03)"
code: []
---

## Summary

A bottom-up 'embodied agent-based modelling and simulation' workflow for very simple robots. It uses the Reality-to-Simulation-to-Reality for Swarms (RSRS) loop to tie low-fidelity simulations tightly to physical experiments with 20+ robots, so cheap simulations generate hypotheses that guide expensive physical runs. The goal is to find conditions under which collective behaviours self-organise, not to close the sim-to-real gap. The authors reproduce two known behaviours from the literature and report a third behaviour found by accident.

## Contribution

It sets out the RSRS methodology that underlies the group's later discovery work ([[mattson-2025-discovery]]), favouring cheap robots and bottom-up exploration over top-down behaviour specification.

## Key results

- Two known swarm behaviours emulated on real robots and one new behaviour discovered (per the abstract).
- Experiments with 20+ robots.

## Methods and models

Embodied agent-based modelling, low-fidelity simulation, RSRS iteration between simulator and hardware.

## Limitations and open questions

Abstract-depth entry. Preprint.

## Relevance to us

Practical methodology if the hackathon runs physical swarm experiments; see [[vega-2025-analytical]].
