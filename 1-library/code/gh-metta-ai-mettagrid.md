---
id: gh-metta-ai-mettagrid
type: code
title: "MettaGrid: fast configurable C++ multi-agent gridworld for emergent cooperation, resources, combat and 'vibes'"
repo: Metta-AI/mettagrid
url: https://github.com/Metta-AI/mettagrid
authors: ["Metta AI contributors"]
year: 2025
language: C++ / Python
license: "MIT"
stars: 17
last_commit: 2026-05-31
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates a gridworld where agents move, gather typed resources from configurable objects, attack each other (an attack triggers when a move lands on an agent whose visible "vibe" matches an attack rule, freezing the target and stealing resources), defend with armor, and hold territory; all object types beyond Agent and Wall are defined in Pydantic config through an event and handler system, with procedural map generation (biomes, BSP, maze, wave function collapse). Interaction is simultaneous; agents belong to configurable groups. Throughput and agent scale are not stated in the README; not measured. RL-first, exposed through a PufferLib adapter and a PettingZoo ParallelEnv adapter, with a terminal renderer that could serve as a text observation. Agent groups, initial inventories and rewards per agent are config fields, so planting a group with different incentives is a config change. Heavy-ish build: Bazel 9, C++20, Python 3.12.

## What it can do for us

The most "social-mechanics-as-config" environment found in this lane: signalling (vibes) that determines who can attack whom is a ready-made identity/badge channel, so mimicry and false-signalling (a Sybil wearing an ally's vibe) can be studied without writing engine code.

## Run notes

Not run (Bazel build). README read via GitHub API on 2026-10-03. The same org has newer related repos (Metta-AI/cogames, 48 stars, "multi-agent cooperative and competitive environments"), not catalogued.

## Limitations

Very new and small community (17 stars; the main Metta training repo was not reachable at github.com/Metta-AI/metta). Bazel toolchain. No published throughput numbers in the README.

## Notes from dmarz/sim-envs

2026-10-03 saturation pass: Metta-AI/cogames is now a retired tombstone ([[gh-metta-ai-cogames]]); its core imports moved into mettagrid.cogame.* in this repo, and the runtime/league layer moved to [[gh-metta-ai-coworld]]. The cogames CLI and game configs (e.g. cogs_vs_clips) were not migrated.
