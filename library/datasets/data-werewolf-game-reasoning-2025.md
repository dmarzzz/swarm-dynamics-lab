---
id: data-werewolf-game-reasoning-2025
type: dataset
title: 'Werewolf game dataset: raw 7- and 9-player game records with thinking-process notes, plus SFT instruction sets (Multi-agent KTO)'
authors:
- Rong Ye
- Yongxin Zhang
- Yikai Zhang
- Haoyu Kuang
- Zhongyu Wei
- Peng Sun
year: 2025
url: https://huggingface.co/datasets/ReneeYe/werewolf_game_reasoning
license: MIT
size: 35,642 rows, 42,556,683 bytes (datasets-server)
format: 'raw/: per game event_{zh,en}.json and note_{zh,en}.json; processed action/speech/vote CSV and parquet'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Data for "Multi-agent KTO: Reinforcing Strategic Interactions of Large Language Model in Language Game" (Ye et al., arXiv 2501.14225). Raw Werewolf games in 7-player (seer_guard, seer_witch) and 9-player (guard_witch_seer, hunter_witch_seer) setups record night actions, day speeches, votes and a game review, plus thinking-process notes: speech summaries with intended labels for other players, voting rationale and future strategy. Originals are Chinese; English is a Claude-3.5-Sonnet-V2 translation. Processed SFT sets cover jargon, strategy and think-before-respond behaviour with a per-day role-prediction task.

## Access

https://huggingface.co/datasets/ReneeYe/werewolf_game_reasoning, not gated, MIT. The card does not say who played the raw games.

## Relevance to us

Hidden-role deception with labelled roles and per-day role-prediction targets, a small-scale analogue of spotting adversarial agents inside a group. Compare [[data-bayesian-social-deduction-2025]].
