---
id: scan-code-robotics-marl
type: task
title: Catalogue swarm robotics simulators and MARL environments
kind: scan
status: open
priority: p0
owner: null
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- swarm-robotics
- marl-emergence
---

## Goal

Find the simulators and training environments for robot swarms and multi-agent RL, with an eye to what trains fast on one GPU.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and catalogue it only if it checks out.

- ARGoS (ilpincy/argos3) and the Kilobot simulators
- VMAS, the vectorized multi-agent simulator (proroklab)
- PettingZoo and Melting Pot
- Drone swarm stacks: Crazyswarm and PX4/ROS swarm tooling
- Buzz, a programming language for robot swarms

## Search plan

- GitHub search by topic and by language, sorted by stars and by recent activity; GitHub topics pages (e.g. topics/swarm, topics/multi-agent).
- Papers With Code and paper project pages for implementations of catalogued papers.
- For each candidate, record stars, last commit date and licence from the repo page.

## Done when

- At least 15 repos catalogued with stars, last commit, licence and an honest read_depth.
- At least 3 installed and run (read_depth: ran) with the commands and results in Run notes, chosen as the most likely to be used in the hackathon.
- Coverage note filled, including a short ranked list of what we would build on.

## Coverage note

The agent that finishes this task writes here: what was searched, counts by type, what is still missing, and which follow-up tasks it opened.
