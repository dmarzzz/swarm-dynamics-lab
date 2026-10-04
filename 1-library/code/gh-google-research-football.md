---
id: gh-google-research-football
type: code
title: "Google Research Football: 3D football game RL environment with single- and multi-agent (up to 11 v 11) control"
repo: google-research/football
url: https://github.com/google-research/football
authors: ["Google Brain team", "Karol Kurach et al."]
year: 2019
language: C++ / Python
license: "Apache-2.0"
stars: 3666
last_commit: 2025-06-17
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulates association football in a 3D physics game engine (based on the open-source Gameplay Football) with scenarios from small "academy" drills to full 11 v 11 matches; agents can control one or several players per team, interaction is simultaneous real-time stepping, and observations are pixels, a minimap or a 115-dimensional state vector. Scale up to 22 players (2-22 per the table in [[hu-2025-toward]]); throughput not measured here and the engine is CPU-bound. RL-only by design, though the state vector is easily textualised. No population or identity manipulation beyond assigning which players are agent-controlled. Heavy: native build with SDL, Boost and OpenGL dependencies (Docker recommended on Linux). Archived on GitHub (read-only).

## What it can do for us

Little directly for swarms: fixed team sizes, full observability of the state vector (which [[ellis-2022-smacv2]] notes simplifies coordination). Listed because it is a standard MARL benchmark a survey must place.

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

Archived. Heavy native dependencies. Fixed rosters.
