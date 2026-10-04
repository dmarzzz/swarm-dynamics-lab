---
id: gh-zju-llms-agent-kernel
type: code
title: "Agent-Kernel: microkernel framework for LLM social simulation with runtime agent addition/removal"
repo: ZJU-LLMs/Agent-Kernel
url: https://github.com/ZJU-LLMs/Agent-Kernel
authors: ["Yuren Mao", "et al."]
year: 2025
language: Python
license: "Apache-2.0"
stars: 534
last_commit: 2026-06-03
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: [mao-2025-agent-kernel]
---

## Summary

Framework: society-centric microkernel separating system core, simulation logic, cognition and environment/action modules; supports dynamic addition and removal of LLM agents at runtime and claims unlimited agent scalability; 'SocietyHub' for sharing simulations. Demonstrations: Universe 25 population dynamics and a 10,000-agent campus simulation. LLM-native: yes. Adversarial hooks: none. Weight: Python.

## What it can do for us

Population churn (agents entering and leaving mid-run) out of the box, which matters for Sybil-arrival scenarios.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Scalability claims unverified; documentation partly Chinese-first.
