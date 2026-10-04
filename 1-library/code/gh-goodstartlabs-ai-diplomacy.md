---
id: gh-goodstartlabs-ai-diplomacy
type: code
title: "AI Diplomacy: frontier LLMs as stateful agents playing full-press Diplomacy with negotiation, diaries and betrayal detection"
repo: GoodStartLabs/AI_Diplomacy
url: https://github.com/GoodStartLabs/AI_Diplomacy
authors: ["Alex Duffy", "Tyler Marques"]
year: 2025
language: Python
license: "Good Start Labs Non-Commercial License"
stars: 707
last_commit: 2026-06-01
topics: [llm-agent-swarms, collective-decision]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Simulation model: the open-source `diplomacy` engine adjudicates orders; seven LLM powers run multi-round private and global negotiation, keep relationship states (enemy to ally), goals and a diary memory with yearly consolidation, then submit orders; analysis compares messages against orders to flag betrayals. Scale: 7 agents per game, with an `experiment_runner.py` to run many games in parallel. LLM-native: yes, OpenAI, Anthropic, Gemini, DeepSeek, OpenRouter and any OpenAI-compatible local endpoint per seat. Adversarial hooks: deception and betrayal are native; per-seat model assignment allows mixed populations. Weight: Python, but long games mean many calls per run.

## What it can do for us

Best existing pipeline for measuring promise-versus-action divergence (stated intent in negotiation vs. submitted orders) across mixed model populations, which is directly a deception metric. Diary logs give per-agent private state to compare with public messages.

## Run notes

Not run. Stars, licence and last push from the GitHub API on 2026-10-03; README read via the API. I did not read the source code. README commands: `python lm_game.py --max_year 1910 --num_negotiation_rounds 3`, `--models` takes a comma-separated list of 7 models.

## Limitations

Non-commercial licence, so we can study but not ship derivatives commercially. Seven fixed seats; cost per game is high with frontier models. Related academic variant: [[gh-mukobi-welfare-diplomacy]].
