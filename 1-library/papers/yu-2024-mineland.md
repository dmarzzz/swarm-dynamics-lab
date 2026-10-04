---
id: yu-2024-mineland
type: paper
title: "MineLand: Simulating Large-Scale Multi-Agent Interactions with Limited Multimodal Senses and Physical Needs"
authors: ["Xianhao Yu", "Jiaqi Fu", "Renjia Deng", "Wenjuan Han"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2403.19267
doi: null
arxiv: "2403.19267"
cite: "Yu, X., Fu, J., Deng, R., & Han, W. (2024). MineLand: Simulating Large-Scale Multi-Agent Interactions with Limited Multimodal Senses and Physical Needs. arXiv preprint arXiv:2403.19267."
topics: [llm-agent-swarms]
added_by: dmarz/factory-scan
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

MineLand is a multi-agent Minecraft simulator supporting 64 or more agents, with limited visual, auditory and environmental senses and physical needs (food, resources), so agents must communicate and collaborate. It ships an agent framework, Alex, inspired by multitasking theory for coordination and scheduling. The authors claim more ecological collective behaviour than prior simulators; the abstract gives no quantitative results.

## Contribution

A scalable Minecraft multi-agent simulator for LLM and VLM agents with resource needs, sitting between single-agent Minecraft benchmarks and [[al-2024-project]] (Project Sid).

## Key results

- Reported: supports 64+ agents; code at github.com/cocacola-lab/MineLand (113 stars, MIT, checked via GitHub API on 2026-10-03).

## Methods and models

Minecraft server with Mineflayer-style bots; VLM agents; abstract read only.

## Limitations and open questions

Abstract only. No market, pricing or firm structure noted.

## Relevance to us

Alternative crafting substrate with many agents. Weaker fit than [[hopkins-2025-factorio]] for production economics because Minecraft recipes are shallow and there is no endogenous price system.
