---
id: gh-giorgiopiatti-govsim
type: code
title: "GovSim: Governance of the Commons Simulation, LLM agent societies managing a shared renewable resource (fishery, pasture, pollution)"
repo: giorgiopiatti/GovSim
url: https://github.com/giorgiopiatti/GovSim
authors: ["Giorgio Piatti", "Zhijing Jin", "Max Kleiman-Weiner", "Bernhard Schölkopf", "Mrinmaya Sachan", "Rada Mihalcea"]
year: 2024
language: Python
license: "MIT"
stars: 85
last_commit: 2025-01-19
topics: [llm-agent-swarms, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: [piatti-2024-cooperate]
---

## Summary

Simulation model: repeated common-pool resource game; each month agents choose a harvest, then talk in a town-hall discussion phase, and the stock regrows; a run collapses when the resource drops below a threshold. Interaction: shared group conversation plus individual harvest actions, Hydra-configured. Scale: 5 agents per society in the paper, 45 runs (3 scenarios times 15 LLMs). LLM-native: yes, via the authors' `pathfinder` wrapper (OpenAI, Anthropic, vLLM, transformers). Adversarial hooks: yes, a 'greedy newcomer' perturbation (`fish_perturbation_outsider`) injects an exploitative agent, plus a no-language ablation and a multi-LLM config that assigns different models to different agents. Weight: conda plus GPU for open-weight models, or API keys.

## What it can do for us

Ready commons-dilemma testbed with an injected-defector experiment already defined, which is the shape of a Sybil or free-rider test. The universalization prompt intervention is a known lever to compare against. Mixed-model societies let us test whether one model family can be steered by another.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code. Commands from the README: `python3 -m simulation.main experiment=fish_baseline_concurrent llm.path=<model>`; multi-LLM: `--config-name=multiple_llm`.

## Limitations

Paper-companion code, last push January 2025; setup scripts assume conda and recursive submodules. Only 5 agents, so it says nothing about scale. Outcome is sensitive to model choice (2 of 45 runs survived per the README figure).
