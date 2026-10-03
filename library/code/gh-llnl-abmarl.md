---
id: gh-llnl-abmarl
type: code
title: "Abmarl (LLNL): agent-based simulation interface and GridWorld framework wired to RLlib for MARL"
repo: llnl/Abmarl
url: https://github.com/llnl/Abmarl
authors: ["LLNL"]
year: 2020
language: Python
license: "unspecified (GitHub NOASSERTION)"
stars: 84
last_commit: 2026-05-11
topics: [marl-emergence]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

Framework: defines an Agent-Based Simulation interface and a Simulation Manager controlling which agents act each step, a GridWorld framework for custom grid ABMs, CLI for train/visualise/analyse, and adapters to gym.Env, RLlib MultiAgentEnv and OpenSpiel. pip install abmarl.

## What it can do for us

Bridge from hand-written ABMs to RLlib training if we want learned policies inside an ABM.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

RLlib dependency is heavy; small community.
