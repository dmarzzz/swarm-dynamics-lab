---
id: tran-2026-single
type: paper
title: Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets
authors:
- Dat Tran
- Douwe Kiela
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2604.02460
doi: null
arxiv: '2604.02460'
cite: Tran, D., & Kiela, D. (2026). Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets. arXiv preprint arXiv:2604.02460.
topics:
- llm-agent-swarms
- agent-budgets
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 0 (OpenAlex, 2026-10-03); 31 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Argues, from the data processing inequality, that with a fixed reasoning-token budget and perfect context use a single agent is more information-efficient than a multi-agent system, and predicts MAS become competitive only when a single agent's effective context use degrades or more compute is spent. In a controlled study with Qwen3, DeepSeek-R1-Distill-Llama and Gemini 2.5, single-agent systems match or beat several multi-agent architectures on multi-hop reasoning when thinking tokens are equalised. The authors also find artefacts in API-based budget control (notably Gemini 2.5) and in standard benchmarks that can inflate apparent MAS gains.

## Contribution

A theory-plus-experiment negative result: many reported MAS advantages on reasoning are unaccounted compute. Complements [[kim-2025-towards]] (agentic tasks) and [[zhang-2025-stop]] (debate).

## Key results

- Measured: SAS >= MAS on multi-hop reasoning at equal thinking-token budgets across three model families.
- Measured: budget-control and benchmark artefacts inflate MAS gains.
- Theory: DPI argument for SAS information efficiency under perfect context utilisation.

## Methods and models

Matched-budget comparison of SAS vs several MAS architectures; diagnostic analysis of budget enforcement.

## Limitations and open questions

Abstract-level read; restricted to multi-hop reasoning, not spatial or embodied coordination where information is inherently distributed.

## Relevance to us

Every LLM-swarm claim at the hackathon should report matched-compute baselines. Related: [[chen-2024-are]], [[bertalanic-2026-ringelmann]].
