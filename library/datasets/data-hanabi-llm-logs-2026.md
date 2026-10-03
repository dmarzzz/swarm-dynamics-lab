---
id: data-hanabi-llm-logs-2026
type: dataset
title: 'HanabiLogs and HanabiRewards: 92,923 turn-level logs of 17 LLMs playing cooperative Hanabi (2-5 players) under three scaffolds, with LLM-judge move ratings'
authors:
- Mahesh Ramesh
- Kaousheik Jayakumar
- Aswinkumar Ramkumar
- Pavan Thodima
- Aniket Rege
- Emmanouil-Vasileios Vlatakis-Gkaragkounis
year: 2026
url: https://huggingface.co/datasets/Mahesh111000/Hanabi_data
license: MIT
size: 92,923 turns across five JSONL files (30,635 / 16,322 / 12,170 / 21,464 / 12,332)
format: JSONL, one row per turn (model_name, players, seed, game state, prompt, response, legal moves; move_ratings in reasoning files)
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Released with "Sparks of Cooperative Reasoning: LLMs as Strategic Hanabi Agents" (Ramesh et al., arXiv 2601.18077). Each row is one turn of a 2-5 player cooperative Hanabi game with fixed seeds, played by one of 17 LLMs (GPT-4o/4.1, o3, o4-mini, Grok-3, Gemini 2.0-2.5, DeepSeek R1/V3, Llama 4 Maverick, Qwen3, Claude 3.7 Sonnet and others) under the Watson, Sherlock or Mycroft scaffolds. The three reasoning files add dense LLM-as-judge ratings for every candidate move (HanabiRewards).

## Access

https://huggingface.co/datasets/Mahesh111000/Hanabi_data, not gated, MIT. Streams with the `datasets` JSON loader.

## Relevance to us

Background on LLM cooperation under partial information (theory of mind between teammates). No adversarial or identity element, so mainly a coordination baseline.
