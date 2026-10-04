---
id: gh-cityflow-project-cityflow
type: code
title: "CityFlow: fast multithreaded microscopic traffic simulator for city-scale multi-agent traffic-signal RL"
repo: cityflow-project/CityFlow
url: https://github.com/cityflow-project/CityFlow
authors: ["Huichu Zhang", "Siyuan Feng", "Chang Liu", "Zhenhui Li", "Weinan Zhang", "CityFlow contributors"]
year: 2019
language: C++ / Python
license: "Apache-2.0"
stars: 1021
last_commit: 2025-08-19
topics: [crowds-and-traffic, marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulates every vehicle on a city road network microscopically, with the RL agents being traffic-signal controllers at intersections (vehicles follow car-following and lane-change models rather than learned policies); interaction is synchronous stepping through a Python API. The README claims city-wide scale with multithreading and shows a speed comparison against SUMO from 1x1 up to 30x30 road grids; population of controllers is more than 100 per [[hu-2025-toward]]; not measured here. RL-only; agents are intersections, not vehicles, so it does not host LLM "drivers". Vehicles continuously enter and leave from flow files, i.e. the vehicle population is open, but those vehicles are not agents. Moderate (C++ build, Docker image available).

## What it can do for us

Little directly. Useful only if we want a fast background traffic substrate; Eclipse SUMO is the heavier, more general alternative (not catalogued).

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

Agents are signal controllers only. Sparse maintenance.
