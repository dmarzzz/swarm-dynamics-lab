---
id: data-c2c-ai-vs-ai-2026
type: dataset
title: 'C2C (Cooperate to Compete) AI-vs-AI games: 972 logged four-player LLM conquest-and-negotiation games under six prompt interventions'
authors:
- Abigail O'Neill
- Alan Zhu
- Mihran Miroyan
- Narges Norouzi
- Joseph E. Gonzalez
year: 2026
url: https://huggingface.co/datasets/negotiation-games/c2c-ai-vs-ai
license: CC-BY-4.0
size: 972 games (6 conditions x 162 matched games), about 23 GB
format: 'Nested JSON per game: manifest.json, game_logs/, game_states/turn_<T>_player_<P>/game_state.json, deal_summaries/ (deal text, parties, kept/broken)'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Raw logs from the Cooperate to Compete benchmark (O'Neill et al., arXiv 2604.25088): a four-player conquest game with private regional objectives, fog of war and non-binding cheap-talk negotiation. Six conditions of 162 games each on matched boards: baseline, plus one target agent prompted to deceive, negotiate aggressively, ask for support, talk to one partner only, or stay silent. Seats are filled by GPT-5.2, GPT-4.1-mini, Gemini 3.1 Pro/Flash-Lite previews and Grok 4.1 fast (reasoning and non-reasoning). Deal summaries record whether each deal was kept or broken.

## Access

https://huggingface.co/datasets/negotiation-games/c2c-ai-vs-ai, not gated, CC-BY-4.0. Viewer disabled; download by folder with huggingface_hub. No human games released.

## Relevance to us

Labelled LLM deception (an instructed deceiver seat) plus kept/broken deal outcomes in a mixed-motive multi-agent setting: a ready testbed for detecting a covert or misbehaving agent among LLM peers. Compare with the human baseline [[data-diplomacy-deception-2020]].
