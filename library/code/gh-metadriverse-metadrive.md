---
id: gh-metadriverse-metadrive
type: code
title: "MetaDrive: lightweight compositional driving simulator with multi-agent scenarios (roundabout, intersection, tollgate, bottleneck, parking lot)"
repo: metadriverse/metadrive
url: https://github.com/metadriverse/metadrive
authors: ["Quanyi Li", "Zhenghao Peng", "Bolei Zhou", "MetaDriverse contributors"]
year: 2021
language: Python
license: "Apache-2.0"
stars: 1252
last_commit: 2025-08-15
topics: [marl-emergence, crowds-and-traffic]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates driving on procedurally composed or real (nuScenes, Waymo) road maps with physics and sensor simulation, and includes multi-agent environments (`roundabout`, `intersection`, `tollgate`, `bottleneck`, `parkinglot`, `pgmap`) where many learning vehicles share the road; interaction is simultaneous, partially observed, self-interested. Population is 20-40 agents per scenario per [[hu-2025-toward]]; the README claims up to 1000+ FPS on a standard PC for the single-agent case; not measured here. RL-only. Open population is built in: in `metadrive/envs/marl_envs/multi_agent_metadrive.py` the default config has `num_agents=15`, `allow_respawn=True` and `delay_done=25`, dead or finished vehicles are removed and `_respawn_vehicles` adds new agents with new ids, and `num_agents=None` adds vehicles endlessly while spawn points are free (read in code, not run). Moderate install (Panda3D-based, runs on macOS).

## What it can do for us

A lighter, CPU-runnable alternative to [[gh-emerge-lab-gpudrive]] for traffic-as-swarm experiments with agents entering and leaving.

## Run notes

Not run. README read via GitHub API on 2026-10-03. Documented demo: `python -m metadrive.examples.drive_in_multi_agent_env --env roundabout`.

## Limitations

Driving-specific. Respawned agents get fresh ids, so per-identity history must be tracked by the experimenter.
