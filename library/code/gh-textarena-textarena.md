---
id: gh-textarena-textarena
type: code
title: "TextArena: gym-style suite of 100+ single, two and multi-player text games for evaluating and training LLM agents"
repo: TextArena/TextArena
url: https://github.com/TextArena/TextArena
authors: ["Leon Guertler", "Bobby Cheng", "Simon Yu", "Bo Liu", "Leshem Choshen", "Cheston Tan"]
year: 2024
language: Python
license: "MIT"
stars: 430
last_commit: 2026-10-03
topics: [llm-agent-swarms, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: ran
relevance: 5
papers: [guertler-2025-textarena]
---

## Summary

Simulation model: turn-based text games behind a Gym-like loop (`env.get_observation()` returns (player_id, observation string), `env.step(action)`), with a game engine that parses bracketed actions and keeps per-player private observations; interaction is broadcast chat plus private moves. Scale: 2 to roughly 15 players per game (social deduction, public goods, iterated PD, stag hunt, negotiation, Catan, Diplomacy-style games); the installed 0.7.4 registry lists 712 environment ids (including wrapper variants). LLM-native: yes, an agent is any `__call__(str) -> str`, with built-in OpenAI, Anthropic, OpenRouter, Gemini, Ollama, llama.cpp and HF agents. Adversarial hooks: no identity layer, but any seat can be a scripted or adversarial callable, so injected liars and free-riders are one line. Weight: pure Python, `pip install textarena`, runs on a laptop against a local Ollama model. Maintained by Guertler et al.; underpins the MindGames NeurIPS 2025 competition and the SPIRAL self-play paper.

## What it can do for us

Cheapest bootstrap for small-group LLM game experiments: public goods, IPD, stag hunt, Secret Mafia, Codenames, negotiation and auctions already implemented with scoring. Swapping one seat for a scripted adversary (sybil, free-rider, colluder) needs no framework change. Good for 'cheap talk vs. action' and deception-detection probes with exact payoffs.

## Run notes

Installed and ran on 2026-10-03 (Apple Silicon, no API key; local Ollama `llama3.1` 8B).

```
uv venv -p 3.11 venv-ta && VIRTUAL_ENV=venv-ta uv pip install textarena ollama   # textarena 0.7.4
```

Script (`ta_pgg.py`): `PublicGoodsGame-v0`, `env.reset(num_players=4, seed=1)`, seats 0 to 2 are `ta.agents.OllamaAgent(model_name="llama3.1", options={"num_predict": 200})`, seat 3 is a scripted adversary that always says "I fully agree, let's all contribute everything for the common good. I will contribute [0]." Default config: 3 rounds, 3 communication turns per round, endowment 20, multiplier 1.5.

Result: 48 turns in 274 s, no invalid moves. Final scores: LLM players 71.2, 65.2, 62.2; scripted free-rider 116.2 (wins). The LLM agents never sanctioned or called out the defector in chat; their visible contributions stayed in the 12 to 20 range across rounds (e.g. [12], [15], [17], [19], [20]) after the defector had publicly contributed [0]. One game, one seed, one model, so this is a smoke test, not a finding. Python 3.9 also installs (textarena 0.6.1) but use 3.11.

## Limitations

Single-threaded turn loop, so not for hundreds of agents. Game rules live in each env's code, so outcomes depend on regex action parsing (format failures count as invalid moves). No network topology, no persistent identities across games, no built-in transcript store beyond what you log. The 192-language localisation is mostly machine-translated.
