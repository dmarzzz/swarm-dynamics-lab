---
id: ren-2025-simworld
type: paper
title: "SimWorld: An Open-ended Realistic Simulator for Autonomous Agents in Physical and Social Worlds"
authors: ["Jiawei Ren", "Yan Zhuang", "Xiaokang Ye", "Lingjun Mao", "Xuhong He", "Jianzhi Shen", "Mrinaal Dogra", "Yiming Liang", "Ruixuan Zhang", "Tianai Yue", "et al."]
year: 2025
venue: "NeurIPS 2025 (spotlight, per repo); arXiv preprint"
url: https://arxiv.org/abs/2512.01078
doi: null
arxiv: '2512.01078'
cite: "Ren, J., Zhuang, Y., Ye, X., Mao, L., He, X., Shen, J., Dogra, M., Liang, Y., Zhang, R., Yue, T., et al. (2025). SimWorld: An open-ended realistic simulator for autonomous agents in physical and social worlds. arXiv:2512.01078."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "10 (Semantic Scholar, 2026-10-03)"
code: [gh-simworld-ai-simworld]
---

## Summary

Unreal Engine 5 simulator for LLM/VLM agents with realistic physics and social rules, language-driven procedural city generation, multimodal observations and open-vocabulary actions at several abstraction levels, plus customisable physical and social reasoning scenarios. Demonstrated with frontier LLM agents on long-horizon multi-agent delivery tasks involving cooperation and competition.

## Contribution

A photorealistic embodied city world with native LLM-agent interfaces, positioned against hand-crafted, game-like sims.

## Key results

- Models show distinct reasoning patterns and limitations on multi-agent delivery (abstract gives no numbers).

## Methods and models

UE5 server + Python client with gym-like API; base package with two city scenes, 100+ optional maps (README).

## Limitations and open questions

Abstract only. Heavy: UE5 server binaries and GPU rendering; few agents per scene compared with ABM scales.

## Relevance to us

Skip as a base for swarm-scale work (too heavy for our disk/GPU budget); relevant only if we need embodied visual agents. Compare lighter LLM-society sims [[gh-google-deepmind-concordia]].
