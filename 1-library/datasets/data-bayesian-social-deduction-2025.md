---
id: data-bayesian-social-deduction-2025
type: dataset
title: 'Bayesian Social Deduction dataset: Avalon game logs between AI agents and humans (GRAIL)'
authors:
- Shahab Rahimirad
- Guven Gergerli
- Lucia Romero
- Angela Qian
- Matthew Lyle Olson
- Simon Stepputtis
- Joseph Campbell
year: 2025
url: https://huggingface.co/datasets/shahabrahimirad/bayesian-social-deduction
license: MIT
size: 100K-1M (HF size category; exact count not on card)
format: 'JSON game logs, one event per entry: quest, turn, failed_party_votes, name, role, team, type, message, proposed_party'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Game logs for "Bayesian Social Deduction with Graph-Informed Language Models" (Rahimirad et al., arXiv 2506.17788). Avalon games in three folders: agent_games (agent vs agent, one playing Good and the other Evil), human_experiments (humans against the GRAIL agent and an LRM agent) and model_ablation (DeepSeek and Llama at 8B and 70B, GRAIL vs reasoning agents). Agent types: GRAIL, Recon, random, OpenAI reasoning, DeepSeek-R1 reasoning, human. Each event carries role, team (good/evil), message and proposed party.

## Access

https://huggingface.co/datasets/shahabrahimirad/bayesian-social-deduction, gated (manual approval on HF). MIT.

## Relevance to us

Labelled hidden-adversary games with team ground truth and human-vs-agent play; a compact benchmark for inferring which members of a group are adversarial from their messages and votes. Compare [[data-werewolf-game-reasoning-2025]].
