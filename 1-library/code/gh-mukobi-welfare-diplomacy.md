---
id: gh-mukobi-welfare-diplomacy
type: code
title: "Welfare Diplomacy: general-sum Diplomacy variant plus LLM-agent scaffolding and exploiter agents for testing cooperative AI"
repo: mukobi/welfare-diplomacy
url: https://github.com/mukobi/welfare-diplomacy
authors: ["Gabriel Mukobi", "Hannah Erlebach", "Niklas Lauffer", "Lewis Hammond", "Alan Chan", "Jesse Clifton"]
year: 2023
language: Python
license: "AGPL-3.0"
stars: 38
last_commit: 2024-04-02
topics: [llm-agent-swarms, marl-emergence, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: [mukobi-2023-welfare]
---

## Summary

Simulates the board game Diplomacy (seven powers on a map of Europe) with a modified rule set in which powers can convert unused supply centres into permanent Welfare Points, the game ends after a fixed number of years, and there is no winner, so peace is rewarded; interaction is simultaneous-order turns with natural-language negotiation between powers. Seven agents; throughput is bound by LLM calls. Natively LLM-driven: the repo ships prompt scaffolding, OpenAI and Anthropic backends, local-model support, a random agent and a W&B experiment harness. Adversarial hooks are first-class: "exploiter" LLM agents prompted to exploit others, and "super exploiters" that play cooperatively and then switch to an RL policy, assignable to chosen powers (e.g. `--super_exploiter_powers France,Russia`). No variable N beyond the seven powers. Light (Python, an engine forked from the open-source diplomacy package) but token-costly.

## What it can do for us

The closest thing in this lane to a ready LLM-agent society with built-in adversaries: test whether cooperative LLM agents detect and punish a defector, and measure social welfare loss from a planted exploiter. The paper reports state-of-the-art LLM baselines reach high welfare but are exploitable [[mukobi-2023-welfare]].

## Run notes

Not run. README read via GitHub API on 2026-10-03. Documented smoke test: `python experiments/simulate_game.py --agent_model random --summarizer_model passthrough --disable_wandb`.

## Limitations

AGPL-3.0 (copyleft; matters if we fork into a shared tool). Seven fixed players. Unmaintained since April 2024. Super exploiters default to GPT-4 for their cooperative phase.
