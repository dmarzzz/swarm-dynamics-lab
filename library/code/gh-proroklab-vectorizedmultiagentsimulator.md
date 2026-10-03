---
id: gh-proroklab-vectorizedmultiagentsimulator
type: code
title: "VMAS: vectorised differentiable 2D multi-agent simulator in PyTorch with multi-robot scenarios including flocking"
repo: proroklab/VectorizedMultiAgentSimulator
url: https://github.com/proroklab/VectorizedMultiAgentSimulator
authors: ["Matteo Bettini", "Prorok Lab, Cambridge"]
year: 2022
language: Python
license: "GPL-3.0"
stars: 617
last_commit: 2026-05-19
topics: [marl-emergence, swarm-robotics, collective-motion]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: []
---

## Summary

A fully differentiable, vectorised 2D physics engine in PyTorch that runs many environment copies in parallel on CPU or GPU, with a library of multi-robot scenarios (flocking, dispersion, transport, football, navigation and more) exposed through its own API plus Gym, Gymnasium, RLlib and TorchRL wrappers; BenchMARL is the companion training library. Paper arXiv 2207.03530. GPL-3.0, 617 stars, last commit 2026-05-19.

## What it can do for us

Batched swarm scenarios where every agent is a learner or a scripted policy, with rewards and observations already defined; running 64 copies of an 8-agent flocking world is one call. Differentiability allows gradient-based inverse design of interaction rules.

## Run notes

venv/bin/pip install vmas (pulls torch 2.14.1 cu130; vmas 1.5.2). Script run_vmas.py: env = vmas.make_env(scenario='flocking', num_envs=64, device='cpu', continuous_actions=True, n_agents=8, seed=0); 100 steps of uniform random actions. Output 2026-10-03: 64 envs x 8 agents x 100 steps in 31.70 s = 1,615 agent-steps/s on CPU; obs shape per agent (64, 18); mean reward of agent 0 at the last step -0.0048. CPU throughput is low because the flocking scenario's pairwise terms are not cheap; the simulator is designed for GPU where the batch dimension is free.

## Limitations

GPL-3.0 (copyleft matters if we ship code). CPU-only here, so the headline GPU throughput numbers were not reproduced. Scenarios are robot-flavoured (collisions, goals), not minimal physics models.
