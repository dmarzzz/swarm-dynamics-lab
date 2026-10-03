---
id: gh-cyberbotics-webots
type: code
title: "Webots: open-source desktop robot simulator (Cyberbotics) with ODE physics, sensor models and multi-language controllers"
repo: cyberbotics/webots
url: https://github.com/cyberbotics/webots
authors: ["Cyberbotics Ltd.", "EPFL (original, 1996)"]
year: 1996
language: C++
license: "Apache-2.0"
stars: 4688
last_commit: 2026-10-03
topics: [swarm-robotics]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

One line: full 3D robot simulation (ODE physics, many robot and sensor models, controllers in C, C++, Python, Java, MATLAB, ROS 2) the README gives no swarm-scale numbers (my background knowledge, not verified this session: robots talk through emitter/receiver devices and each controller is a separate process, which keeps practical swarms to tens of robots); no LLM integration in the README; no adversarial hooks; medium to heavy to run (desktop app, GPU rendering, has a headless mode).

Designed at EPFL in 1996, commercial from 1998, open-sourced in December 2018; Cyberbotics funds development through support and consulting. Very active.

## What it can do for us

When a study needs realistic e-puck or Thymio style robots with sensors and a radio channel to which a faulty transmitter can be added, Webots is the polished choice; for swarm statistics it is too slow compared with [[gh-ilpincy-argos3]].

## Run notes

Not run.

## Limitations

Scale limits are not documented in the README; heavy GUI-first tooling.
