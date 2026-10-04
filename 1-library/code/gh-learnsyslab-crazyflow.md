---
id: gh-learnsyslab-crazyflow
type: code
title: "Crazyflow: batched, differentiable JAX simulator of Crazyflie quadrotors (n_worlds x n_drones) with MuJoCo/MJX integration"
repo: learnsyslab/crazyflow
url: https://github.com/learnsyslab/crazyflow
authors: ["Learning Systems Lab (Jacopo Panerati et al.)"]
year: 2024
language: Python (JAX)
license: "MIT"
stars: 184
last_commit: 2026-09-30
topics: [swarm-robotics, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

One line: quadrotor dynamics (first-principles plus three fitted abstract models) batched over independent worlds and multi-drone swarms; README reports 3.3M to 15.6M steps/s on a Ryzen 9 7950X CPU and up to 914M steps/s on an RTX 4090 at 262k worlds (single drone, first-principles); no LLM integration; no adversarial hooks; light to run on CPU (pip install crazyflow), GPU extra is Linux x86-64 CUDA 12.

From the same lab as [[gh-learnsyslab-gym-pybullet-drones]]. Step and reset are tuples of plain JAX functions, so custom stages can be inserted anywhere; jax.grad works through dynamics and control.

## What it can do for us

The GPU successor for drone swarms: thousands of worlds in parallel for RL or for statistics over attacker placements, with differentiable dynamics for gradient-based attack or defence design.

## Run notes

Not run (time budget spent on gym-pybullet-drones).

## Limitations

Throughput figures are for one drone per world; multi-drone interaction and collisions go through MJX. GPU extra is x86-64 only per README.
