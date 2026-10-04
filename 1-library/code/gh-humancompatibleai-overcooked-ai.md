---
id: gh-humancompatibleai-overcooked-ai
type: code
title: "Overcooked-AI: two-player cooperative cooking gridworld benchmark for human-AI and zero-shot coordination"
repo: HumanCompatibleAI/overcooked_ai
url: https://github.com/HumanCompatibleAI/overcooked_ai
authors: ["Micah Carroll", "Rohin Shah", "Center for Human-Compatible AI contributors"]
year: 2019
language: Python
license: "MIT"
stars: 1015
last_commit: 2025-03-22
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulates a small kitchen gridworld where two chefs must split tasks (fetch onions, fill pot, wait, plate, serve) to deliver soups fast; interaction is simultaneous-move, fully observed, fully cooperative, with five standard layouts plus programmatic layout generation. Agent scale is fixed at 2; throughput not measured here (pure Python; JAX and Madrona ports exist in [[gh-bold-lab-ai-jaxmarl]] and [[gh-shacklettbp-madrona]] for speed). Its strength is the human-AI play web demo and human trajectory data. The state is symbolic (object positions), so an LLM agent can be driven from a text rendering, and several LLM papers do so (e.g. "Collab-Overcooked" listed in [[hu-2025-toward]]). No population or identity manipulation beyond swapping which policy controls each chef (which is how ad hoc and zero-shot coordination is tested). Light: `pip install overcooked-ai`.

## What it can do for us

Partner-swap evaluation: the standard way to test whether an agent coordinates with unfamiliar partners, which is the two-agent version of "can an agent tell a stranger from a teammate". Not a swarm environment.

## Run notes

Not run. README read via GitHub API on 2026-10-03; metadata from the API.

## Limitations

Two agents only. The repo notes its built-in BC and PPO training code is deprecated. Mostly a coordination benchmark, not a population simulator.
