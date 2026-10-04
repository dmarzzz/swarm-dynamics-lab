---
id: gh-agiresearch-waragent
type: code
title: "WarAgent: LLM multi-agent simulation of historical world wars with country and secretary agents"
repo: agiresearch/WarAgent
url: https://github.com/agiresearch/WarAgent
authors: ["agiresearch"]
year: 2023
language: Python
license: "Apache-2.0"
stars: 459
last_commit: 2024-03-05
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
papers: []
---

## Summary

Simulation model: each country is an LLM agent defined by a country profile that picks actions each round from an action space; a secretary agent checks each action for appropriateness and logical consistency; a 'Board' manages international relations and a 'Stick' records domestic statutes. Scenarios: WWI, WWII, Warring States. Paper arXiv 2311.17227 (not catalogued). LLM-native: yes (OpenAI or Claude). Weight: light, depends on PromptCoder.

## What it can do for us

Pattern of a verifier ('secretary') agent gating each action, and a shared relations board; small-N geopolitical sim.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API; source code not read.

## Limitations

Unmaintained since 2024-03; about ten agents; historical-scenario framing.
