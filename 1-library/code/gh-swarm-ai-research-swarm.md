---
id: gh-swarm-ai-research-swarm
type: code
title: "SWARM: System-Wide Assessment of Risk in Multi-agent systems, a framework for measuring emergent failures in agent populations (illusion delta, quality gap, governance experiments)"
repo: swarm-ai-research/swarm
url: https://github.com/swarm-ai-research/swarm
authors: ["swarm-ai-research"]
year: 2026
language: Python
license: "MIT"
stars: 46
last_commit: 2026-09-22
topics: [llm-agent-swarms, criticality-measurement]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Python framework (pip package swarm-safety, arXiv 2604.19752 per the README badge) for simulating populations of agents and measuring interaction-level safety signals that do not appear at the single-agent level: an 'illusion delta' defined as perceived quality among accepted interactions minus 1 minus mean replay disagreement, quality gaps, adverse selection, variance amplification, and governance latency. Includes governance experiments (audits, staking, sanctions), scenario sweeps, a live Hugging Face Space sandbox, a Colab quickstart and a 60-second example (examples/illusion_delta_minimal.py, 3 agents with one deceptive actor). The same group maintains the wiki-agent-swarm-incident archive. Framing is opinionated (capability asymmetry, 'electric-mind regime'); the metrics are the reusable part.

## What it can do for us

A ready population simulator with safety metrics and governance knobs, MIT licensed, CI passing, active (last commit 2026-09-22). Could host a controlled replay of 'shared board plus leaky grader' dynamics with the authors' own incident archive as the empirical comparator.

## Run notes

Not run. Metadata (stars, licence, last commit) taken from the GitHub API on 2026-10-03; README read via the API.

## Limitations

46 stars, single group; metric definitions are the authors' own and not yet standard. Not run here. Check whether agents are LLM-backed or scripted before relying on it for LLM swarm claims.
