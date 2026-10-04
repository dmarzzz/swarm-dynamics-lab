---
id: gh-ruc-gsai-yulan-onesim
type: code
title: "YuLan-OneSim: LLM social simulator with code-free scenario building, 50+ default scenarios and a distributed runtime claimed to reach 100,000 agents"
repo: RUC-GSAI/YuLan-OneSim
url: https://github.com/RUC-GSAI/YuLan-OneSim
authors: ["Lei Wang", "Heyang Gao", "Xiaohe Bo", "Xu Chen", "Ji-Rong Wen"]
year: 2025
language: Python
license: "Apache-2.0"
stars: 245
last_commit: 2026-02-02
topics: [llm-agent-swarms, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulation model: event-driven multi-agent social scenarios generated from natural-language descriptions (an LLM writes the scenario code), across 8 social-science domains with 50+ defaults; includes an 'AI social researcher' that proposes topics and writes reports. Scale: the README claims a distributed architecture supporting up to 100,000 agents (not verified here). LLM-native: yes, configured in `config/model_config.json`. Adversarial hooks: none specific. Weight: Docker image `ptss/yulan-onesim` with web UI on port 8000, or source install. Paper arXiv 2505.07581 (not catalogued here).

## What it can do for us

If we need a large population quickly without writing scenario code, this is the most turnkey of the Chinese-lab simulators; the distributed runtime is worth reading if we scale our own sim.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code.

## Limitations

LLM-generated scenario code is hard to audit, which worsens the validation problem in [[larooij-2025-do]]. Scale claim unverified. Last push February 2026.
