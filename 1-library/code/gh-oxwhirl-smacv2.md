---
id: gh-oxwhirl-smacv2
type: code
title: "SMACv2: procedurally generated StarCraft II micromanagement benchmark for cooperative MARL (fixes SMAC's determinism)"
repo: oxwhirl/smacv2
url: https://github.com/oxwhirl/smacv2
authors: ["Benjamin Ellis", "Jonathan Cook", "Skander Moalla", "Mikayel Samvelyan", "Whiteson Research Lab (Oxford)"]
year: 2022
language: Python
license: "MIT"
stars: 331
last_commit: 2024-02-15
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [ellis-2022-smacv2]
---

## Summary

Simulates StarCraft II unit battles in which each allied unit is a decentralised agent fighting the built-in AI, with team composition, start positions (reflect or surround) and unit types drawn from a configurable "capability config" each episode; interaction is simultaneous, partially observed, cooperative. Scenarios have 5, 10 or 20 allies (and 10v11, 20v23 asymmetric), plus an Extended Partial Observability (EPO) variant. Throughput is bounded by the StarCraft II game binary (slow; SMAC is described as one of the most expensive MARL environments in [[gorsane-2022-towards]]). RL-only in practice (fixed feature vectors, no text). Team size and unit mix are configurable per episode through the distribution classes, which is the closest thing here to variable populations, but enemies are always the scripted built-in AI. Heavy: needs a StarCraft II install (Linux binary for headless) and the correct game version, per the README.

## What it can do for us

Mainly as a cautionary design example: the paper behind it [[ellis-2022-smacv2]] shows that its predecessor [[gh-oxwhirl-smac]] could be partly solved by open-loop policies that ignore observations. The capability-config pattern (sample team composition and positions per episode from pluggable distributions) is a good design to borrow for any sim we build.

## Run notes

Not run (needs the StarCraft II binary). README read via GitHub API on 2026-10-03.

## Limitations

StarCraft II dependency, version-sensitive results, slow, Linux-oriented. Last push February 2024. JAX approximation "SMAX" in [[gh-bold-lab-ai-jaxmarl]] avoids the binary but is not the same game.
