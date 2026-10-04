---
id: gh-ntnu-arl-aerial-gym-simulator
type: code
title: "Aerial Gym Simulator: Isaac Gym-based, GPU-parallel simulator for multirotors with GPU controllers and ray-cast sensors"
repo: ntnu-arl/aerial_gym_simulator
url: https://github.com/ntnu-arl/aerial_gym_simulator
authors: ["Mihir Kulkarni", "Welf Rehberg", "Theodor J. L. Forgaard", "Kostas Alexis"]
year: 2023
language: Python
license: "BSD-3-Clause"
stars: 776
last_commit: 2026-06-28
topics: [swarm-robotics]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

One line: thousands of multirotors (quad, fully actuated, arbitrary configurations) simulated in parallel on NVIDIA Isaac Gym with GPU geometric controllers and GPU ray-cast depth/segmentation/LiDAR; README claims state-based policies train in under a minute; no LLM integration; no adversarial hooks; heavy to run (Isaac Gym, NVIDIA GPU).

From NTNU's Autonomous Robots Lab; second release, papers arXiv 2305.16510 and 2503.01471 (not catalogued here). Focus is single-robot navigation in clutter, parallelised across environments, rather than interacting swarms.

## What it can do for us

Reference for GPU sensor simulation if a swarm study needs perception (e.g. a drone detecting other drones).

## Run notes

Not run (needs Isaac Gym and an NVIDIA GPU).

## Limitations

Isaac Gym is a deprecated NVIDIA preview line; parallel environments, not inter-agent interaction, are the design centre.
