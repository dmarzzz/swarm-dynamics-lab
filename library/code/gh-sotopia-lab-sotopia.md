---
id: gh-sotopia-lab-sotopia
type: code
title: "Sotopia: open-ended social role-play environment with private goals and the SOTOPIA-Eval multi-dimensional judge"
repo: sotopia-lab/sotopia
url: https://github.com/sotopia-lab/sotopia
authors: ["Xuhui Zhou", "Hao Zhu", "Leena Mathur", "Ruohong Zhang", "Haofei Yu", "Zhengyang Qi", "Louis-Philippe Morency", "Yonatan Bisk", "Daniel Fried", "Graham Neubig", "Maarten Sap"]
year: 2023
language: Python
license: "MIT"
stars: 335
last_commit: 2026-06-05
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [zhou-2023-sotopia, zhou-2024-is]
---

## Summary

Simulation model: two (optionally more) characters with profiles, relationships, secrets and private social goals interact turn by turn in a scenario (negotiation, persuasion, cooperation); an environment/judge LLM scores goal completion, believability, knowledge, secret keeping, relationship, social rules and material benefit. Scale: dyads in the benchmark (90 scenarios, 40 characters). LLM-native: yes, litellm-style model strings. Adversarial hooks: private goals and secrets give built-in information asymmetry and deception; no identity layer. Weight: `uv sync`, Redis by default (a local JSON backend exists for development), OpenAI key.

## What it can do for us

Good source of scenario and judge design for deception and secret-keeping between agents, and the Agents-vs-Script distinction from [[zhou-2024-is]] is a design rule we should copy. Less useful for swarms because it is built around dyads.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code.

## Limitations

Dyadic focus; Redis dependency for experimental features; scoring depends on a GPT-4-class judge, which [[larooij-2025-do]] flags as a weak validation method.
