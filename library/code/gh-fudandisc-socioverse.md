---
id: gh-fudandisc-socioverse
type: code
title: "SocioVerse: Fudan social-simulation 'world model' with a 10-million real-user pool; repo holds questionnaires and evaluation scripts, simulator code not released"
repo: FudanDISC/SocioVerse
url: https://github.com/FudanDISC/SocioVerse
authors: ["Xinnong Zhang", "Jiayu Lin", "Xinyi Mou", "Zhongyu Wei", "et al."]
year: 2025
language: Python
license: "Apache-2.0"
stars: 216
last_commit: 2026-02-08
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulation model: population-level survey-style simulation; agents are built from a pool of 10 million real social-media users and aligned to a target population via four alignment modules, then answer questionnaires (US presidential election, breaking-news feedback, Chinese national economic survey). Scale: user pool of 10M; agent counts per run not stated in README. LLM-native: yes. Adversarial hooks: none. Weight: unknown; the README says the world-model code is 'coming soon'; only questionnaires, evaluation scripts and part of the user pool (HF dataset Lishi0905/SimulateAnything) are released. Paper arXiv 2504.10157 (not catalogued here).

## What it can do for us

Possible source of realistic persona distributions (the released user-pool subset) for seeding a social sim; nothing runnable for interaction dynamics.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code.

## Limitations

Core simulator not public. Agents answer questionnaires rather than interact, so it is closer to silicon sampling than to a swarm sim.
