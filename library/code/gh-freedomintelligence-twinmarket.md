---
id: gh-freedomintelligence-twinmarket
type: code
title: "TwinMarket: LLM-agent stock market simulation with social network, behavioural biases and order matching"
repo: FreedomIntelligence/TwinMarket
url: https://github.com/FreedomIntelligence/TwinMarket
authors: ["FreedomIntelligence"]
year: 2025
language: "Python"
license: "MIT"
stars: 221
last_commit: 2026-03-07
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulates: a stock market of LLM trading agents with personalised strategies, a forum-style social network, news and sentiment inputs, behavioural-finance traits (disposition effect, lottery preference) and a real-time matching engine. Interaction model: LLM agents trade and post in rounds. Scale: not stated in the README (the NeurIPS 2025 paper, arXiv 2502.01506, was not opened). LLM-driven: yes. Adversarial hooks: none native; coordinated rumour accounts would be added as agents. Weight: API and embedding-model config plus `bash script/run.sh`.

## What it can do for us

A substrate for "coordinated LLM accounts move a market through a social channel" experiments, the market-side analogue of [[gh-qqqqqqby-botsim]].

## Run notes

Not run. Stars, licence and last commit from the GitHub API on 2026-10-03; README read via the API.

## Limitations

Paper not read here; scale and validation unverified. API cost grows with agent count.
