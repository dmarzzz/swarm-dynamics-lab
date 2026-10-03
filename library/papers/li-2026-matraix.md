---
id: li-2026-matraix
type: paper
title: "MatrAIx: Simulating the World with 8.3 Billion Persona Agents"
authors: ["Xiaomin Li", "Yuexing Hao", "Jianheng Hou", "Jintao Huang", "Qianfeng Wen", "Shirley Huang", "Yifan Liu", "Xiaoyi Liu", "Yilan Fan", "Yijun Wang", "et al."]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.04205
doi: null
arxiv: '2608.04205'
cite: "Li, X., Hao, Y., Hou, J., Huang, J., Wen, Q., Huang, S., Liu, Y., Liu, X., Fan, Y., Wang, Y., et al. (2026). MatrAIx: Simulating the world with 8.3 billion persona agents. arXiv:2608.04205."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "7 (Semantic Scholar, 2026-10-03)"
code: [gh-matraix-ai-matraix-persona-8b]
---

## Summary

Population-scale simulated-user evaluation infrastructure. 'Persona 8B' is 8.3 billion persona records over 1,290 categorical dimensions, sampled from an attribute dependency graph or derived from human-authored profiles; a quality-filtered coreset of about 1M personas (599,847 human-grounded, 400,000 synthetic) is released. A Playground runs persona agents through four environments (Survey, AI Chatbot, Web, App) on 1,010 application tasks across 25+ domains; 18,189 trials were run across eight tasks with Claude Opus 4.8, GPT 5.5 and Claude Haiku 4.5 as backbones.

## Contribution

Scales persona conditioning (silicon sampling) to a schema-backed population with released personas and task verifiers; it is a product-evaluation harness rather than an interacting society.

## Key results

- Persona adherence: declared behaviour expressed or correctly suppressed in 366/400 controlled trials (91.5%).
- 18,189 evaluation trials across eight representative tasks (numbers from the abstract).

## Methods and models

LLM agents instantiated from persona records act one at a time in Docker-backed Web/App environments or survey/chat interfaces; task-owned verifiers score trajectories; telemetry aggregates by subgroup.

## Limitations and open questions

Agents do not interact with each other, so no emergent collective dynamics. Validation is adherence to declared attributes, not agreement with real population behaviour. Abstract only; the 8.3B figure is generated records, not distinct real people.

## Relevance to us

Borrow idea: the 1M persona coreset and its 1,290-dimension schema could seed heterogeneous agents in a social sim. Not a multi-agent environment. Sibling instrument from the same group: [[ng-2026-microverse]]. Compare [[gh-fudandisc-socioverse]].
