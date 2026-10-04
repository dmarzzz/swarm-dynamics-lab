---
id: gh-google-werewolf-arena
type: code
title: "Werewolf Arena: Google framework for evaluating LLM social deduction in the game Werewolf with a bidding turn-taking mechanism"
repo: google/werewolf_arena
url: https://github.com/google/werewolf_arena
authors: ["Suma Bailis", "Jane Friedhoff", "Feiyang Chen"]
year: 2024
language: Python
license: "Apache-2.0"
stars: 48
last_commit: 2024-07-22
topics: [llm-agent-swarms, swarm-detection]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulation model: a Werewolf game master runs night/day phases; villager and werewolf seats are LLMs that bid to speak, debate and vote; logs include private reasoning, bids, votes and prompts, viewable in a web viewer. Scale: one table (8 players). LLM-native: yes, Gemini via GCP and OpenAI models, and model pairs can be pitted (`--v_models`, `--w_models`). Adversarial hooks: deception is the game (werewolves are the hidden adversary coalition); no identity layer. Weight: small Python repo plus npm viewer. Accompanies arXiv 2407.13943 (not catalogued here).

## What it can do for us

A clean 'hidden coalition among honest agents' setting, structurally the same as a small sybil group trying to steer a vote. The saved private reasoning versus public speech is useful ground truth for deception-detection features.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code. README commands: `python3 main.py --run --v_models=pro1.5 --w_models=gpt4`; batch: `--eval --num_games=5`.

## Limitations

Archived by Google (read-only). Model names are 2024-era; adding providers means editing the code.
