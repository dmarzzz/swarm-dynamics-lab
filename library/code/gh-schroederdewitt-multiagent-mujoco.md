---
id: gh-schroederdewitt-multiagent-mujoco
type: code
title: "Multi-Agent MuJoCo (MaMuJoCo): continuous multi-agent robotic control benchmark splitting MuJoCo bodies across agents (original repo; maintained fork in Gymnasium Robotics)"
repo: schroederdewitt/multiagent_mujoco
url: https://github.com/schroederdewitt/multiagent_mujoco
authors: ["Christian Schroeder de Witt", "Bei Peng", "Pierre-Alexandre Kamienny", "Philip Torr", "Wendelin Böhmer", "et al."]
year: 2020
language: Python
license: "Apache-2.0"
stars: 375
last_commit: 2023-03-16
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

Benchmark for decentralised cooperative continuous control built on OpenAI Gym MuJoCo tasks, where a robot's joints are partitioned among several agents that must coordinate; described in 'Deep Multi-Agent Reinforcement Learning for Decentralized Continuous Cooperative Control' (arXiv 2003.06709, not catalogued). The README points to the maintained fork in Farama's Gymnasium Robotics, which adds fixes, docs, pip install and current Python support.

## What it can do for us

Standard continuous-action cooperative MARL benchmark; use the Gymnasium Robotics fork rather than this repo.

## Run notes

Not run. GitHub API data and README read 2026-10-03. Original requires Gym 0.10.8 and MuJoCo 2.1 with Linux-specific GLEW preload for rendering.

## Limitations

Original repo unmaintained since 2023-03; few agents per task.
