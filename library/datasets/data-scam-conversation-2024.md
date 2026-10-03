---
id: data-scam-conversation-2024
type: dataset
title: 'Synthetic multi-turn scam and non-scam phone conversations between two AI agents, with 8 receiver personalities'
authors:
- BothBosu
year: 2024
url: https://huggingface.co/datasets/BothBosu/multi-agent-scam-conversation
license: Apache-2.0
size: 1,600 rows, 1,937,365 bytes
format: 'CSV with dialogue, personality, type, label'
topics:
- llm-agent-swarms
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 1
papers: []
---

## Summary

1,600 simulated phone dialogues generated with AutoGen and the Together inference API: one agent plays a scammer (SSN, refund, tech support, reward) or a legitimate caller (delivery, insurance, appointment, wrong number), the other an "innocent" receiver with a personality such as aggressive, anxious, confused, greedy or skeptical. Binary scam label plus scam type. No paper linked; the card does not name the underlying models.

## Access

Public on Hugging Face, not gated, Apache-2.0.

## Relevance to us

Two-agent role-play data for scam classification; marginal for swarm or sybil work and kept only as background.
