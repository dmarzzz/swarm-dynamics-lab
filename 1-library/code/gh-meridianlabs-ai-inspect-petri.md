---
id: gh-meridianlabs-ai-inspect-petri
type: code
title: "Inspect Petri: auditor-target-judge agent for automated alignment auditing, built on Inspect"
repo: meridianlabs-ai/inspect_petri
url: https://github.com/meridianlabs-ai/inspect_petri
authors: ["Meridian Labs"]
year: 2025
language: "Python"
license: "MIT"
stars: 1357
last_commit: 2026-10-02
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates: multi-turn audit scenarios in which an auditor model drives a target model through seed instructions, simulates the target's tools and rolls back conversations, and a judge model scores transcripts against a rubric. Interaction model: three-role LLM loop on [[gh-ukgovernmentbeis-inspect-ai]]. Scale: many seeds in parallel, bounded by API budget; no number in the README. LLM-driven: yes, entirely. Adversarial hooks: the auditor is an adversarial role by design; simulated tools let it fabricate environment responses. Weight: pip install from GitHub, API keys required. Version 3.0 with breaking Python API changes from 2.0 (still on the petri-v2 branch). A GitHub API request for safety-research/petri redirected to this repository, so the Petri project now lives under meridianlabs-ai.

## What it can do for us

Simulated tools plus rollback is a cheap way to stage fork-merge scenarios: the auditor can fake what a sub-agent returns and test whether the parent accepts a corrupted merge.

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Single target per audit; no population or network. Judge-model scoring inherits judge bias.
