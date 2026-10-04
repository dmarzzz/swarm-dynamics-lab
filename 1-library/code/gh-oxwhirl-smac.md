---
id: gh-oxwhirl-smac
type: code
title: "SMAC: StarCraft Multi-Agent Challenge environments"
repo: oxwhirl/smac
url: https://github.com/oxwhirl/smac
authors: ["Mikayel Samvelyan", "Tabish Rashid", "WhiRL Oxford"]
year: 2019
language: Python
license: "MIT"
stars: 1368
last_commit: 2024-02-18
topics: [marl-emergence]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 1
papers: []
---

## Summary

The StarCraft II micromanagement benchmark for cooperative MARL: squads of allied units controlled by decentralised agents against the built-in AI, with partial observability and the standard win-rate metric. MIT, 1.4k stars, last commit 2024-02-18; SMACv2 and JaxMARL SMAX are the successors.

## What it can do for us

Background only.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Needs the StarCraft II binary.

## Notes from dmarz/sim-envs

SMAC is saturated and partly open-loop solvable: [[ellis-2022-smacv2]] (read in full) shows policies that see only the timestep and agent ID reach closed-loop-level win rates on several maps (e.g. bane_vs_bane, 3s5z, 2s3z), and [[gorsane-2022-towards]] finds most maps near 100% win rate by 2021 with inconsistent QMIX numbers across papers. Use [[gh-oxwhirl-smacv2]] instead for any new evaluation.
