---
id: gh-lis-epfl-swarmlab
type: code
title: "SwarmLab: MATLAB drone and drone-swarm simulator (Olfati-Saber and Vasarhelyi flocking, quadcopter or point-mass)"
repo: lis-epfl/swarmlab
url: https://github.com/lis-epfl/swarmlab
authors: ["Enrica Soria", "Fabrizio Schiano", "Dario Floreano"]
year: 2020
language: MATLAB
license: "MIT"
stars: 313
last_commit: 2022-11-29
topics: [swarm-robotics, collective-motion]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
papers: []
---

## Summary

One line: drone swarm flocking with the Olfati-Saber or Vasarhelyi (Vicsek-style) algorithms, agents either full quadcopter dynamics (Beard and McLain architecture) or point masses, with run-time and offline 3D viewers and plotters; README gives no throughput figures; no LLM integration; no adversarial hooks; needs a MATLAB licence plus the Statistics and Machine Learning Toolbox.

EPFL LIS code accompanying Soria, Schiano and Floreano, SwarmLab: a Matlab Drone Swarm Simulator (arXiv 2005.02769, IROS 2020; not catalogued). Dormant since November 2022.

## What it can do for us

Clean reference implementations of the two field-tested drone flocking controllers (the README links the Vasarhelyi et al. Science Robotics version) to port into a Python or Rust sim, plus their order metrics.

## Run notes

Not run (no MATLAB).

## Limitations

MATLAB licence; dormant; scale limited by MATLAB loops.
