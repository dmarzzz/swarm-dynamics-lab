---
id: gh-cocacola-lab-mineland
type: code
title: "MineLand: multi-agent Minecraft simulator with limited multimodal senses and physical needs, up to 48 agents (archived)"
repo: cocacola-lab/MineLand
url: https://github.com/cocacola-lab/MineLand
authors: ["cocacola-lab"]
year: 2024
language: Python
license: "MIT"
stars: 113
last_commit: 2025-09-30
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Simulation model: embodied Minecraft world via Mineflayer; agents have limited visual and auditory senses and hunger/physical needs, act through code-like actions, and communicate in game chat; the bundled 'Alex' agent framework drives LLMs. Scale: README claims up to 48 agents. LLM-native: yes (multimodal). Adversarial hooks: none specific. Weight: heavy, Python 3.11 plus Node 18 plus Java 17, a Minecraft server, or Docker. Paper arXiv 2403.19267 (not catalogued here).

## What it can do for us

Only relevant if we want embodied, resource-constrained societies; compare with [[gh-altera-al-project-sid]], which has no released code.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code.

## Limitations

Archived (read-only). Heavy toolchain; slow per-step; 48-agent ceiling.
