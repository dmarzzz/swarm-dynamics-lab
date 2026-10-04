---
id: gh-stanfordhci-genagents
type: code
title: "genagents: Stanford code for interview- or survey-grounded generative agents of individuals, with a 3,000-agent GSS demographic bank"
repo: StanfordHCI/genagents
url: https://github.com/StanfordHCI/genagents
authors: ["Joon Sung Park", "Carolyn Q. Zou", "Michael S. Bernstein", "et al."]
year: 2024
language: Python
license: "MIT"
stars: 614
last_commit: 2024-11-18
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [park-2024-llm]
---

## Summary

Simulation model: not a world; single agents with memory-stream and reflection modules that answer categorical, numerical and open-ended questions as a specific person. Scale: ships a bank of 3,000+ agents seeded from General Social Survey demographics (fictional names); the 1,052 interview-based agents are only available through a restricted API. LLM-native: yes, OpenAI. Adversarial hooks: none. Weight: light Python plus OpenAI key.

## What it can do for us

Best open source of heterogeneous, empirically grounded personas to reduce the homogeneity of LLM swarms; we could seed agents in [[gh-ysocialtwin-ysocial]] or [[gh-camel-ai-oasis]] from this bank.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code.

## Limitations

No interaction environment. The validated interview agents are gated; the open bank is demographics-only, which the paper shows is the least accurate condition (74% vs. 86% normalised accuracy). No push since November 2024.
