---
id: gh-salesforce-ai-economist
type: code
title: "Foundation (AI Economist): composable economic simulation with worker agents and a tax-setting social planner"
repo: salesforce/ai-economist
url: https://github.com/salesforce/ai-economist
authors: ["Stephan Zheng", "Alexander Trott", "Sunil Srinivasa", "Salesforce Research"]
year: 2020
language: Python
license: "BSD-3-Clause"
stars: 114
last_commit: 2023-08-20
topics: [marl-emergence, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates a small economy in a 2D gridworld where mobile worker agents gather resources, build, and trade while a social-planner agent (a "government") sets taxes; the framework is composed from base classes for Agents, Components (which add dynamics and action spaces) and Scenarios, with a Gym-style reset/step API. Interaction is simultaneous two-level (workers and planner). Agent scale is small (a handful of workers in published scenarios; not checked beyond the README); throughput not reported in the README, though GPU training via [[gh-salesforce-warp-drive]] is shown in a tutorial. RL-first, but observations are dict-structured and the economic actions (trade, build, move) are easily verbalised, so LLM workers are plausible. Agent classes are pluggable, which makes it easy to add a deviant agent type (e.g. a colluding or sybil worker) through the component system. Light: pure Python. Archived (read-only).

## What it can do for us

The cleanest reference design for "mechanism designer vs population" experiments: a planner agent tuning a rule (tax) against learning agents is structurally the same as a defender tuning a Sybil filter against adapting attackers. The Simulation Card in the repo is a model for documenting intended use.

## Run notes

Not run. README read via GitHub API on 2026-10-03.

## Limitations

Archived, last push August 2023. Small populations. The repo's own papers (arXiv 2004.13332, 2108.02755) are not catalogued here yet.
