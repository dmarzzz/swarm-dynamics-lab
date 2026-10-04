---
id: li-2025-systematic
type: paper
title: "Systematic Failures in Collective Reasoning under Distributed Information in Multi-Agent LLMs"
authors:
- "Yuxuan Li"
- "Aoi Naito"
- "Hirokazu Shirado"
year: 2025
venue: "International Conference on Machine Learning (ICML 2026), per arXiv comments"
url: https://arxiv.org/abs/2505.11556
doi: null
arxiv: "2505.11556"
cite: "Li, Y., Naito, A., & Shirado, H. (2025). Systematic failures in collective reasoning under distributed information in multi-agent LLMs. arXiv preprint arXiv:2505.11556 (accepted to ICML 2026)."
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: "0 (OpenAlex W6929584630, arXiv record, 2026-10-03); Semantic Scholar 16 same day"
code: []
---

## Summary

Builds HiddenBench, 65 tasks based on the Hidden Profile paradigm from social psychology: shared information points to a wrong option, and each agent privately holds a piece of the evidence that reveals the right one. Each task is solvable by a single agent given all the information, so the benchmark separates collective information pooling from individual reasoning. Across 15 frontier LLMs, groups reach only 30.1% accuracy under distributed information versus 80.7% for a single agent with complete information. Agents can integrate information once it is disclosed but fail to recognise latent information asymmetry, so they converge prematurely on shared evidence.

## Contribution

Imports a canonical human group-decision failure (shared-information bias, Stasser and Titus 1985) into LLM collectives with a controlled benchmark, showing that collective failure is not explained by individual capability. It sits next to [[cemri-2025-why]] (failure taxonomy) and [[kim-2025-towards]] (scaling costs) as a mechanism-level failure result.

## Key results

- 30.1% (multi-agent, distributed information) vs 80.7% (single agent, full information), across 15 models. Measured.
- The gap persists across prompting strategies, communication depths and group sizes, and worsens as groups grow. Measured (direction; exact curves not copied).
- Neither model scale nor individual reasoning accuracy predicts collective performance; Gemini-2.5-Flash/Pro do best. Measured.
- Forced disclosure nearly removes the failure; passive summarisation helps unevenly (GPT-4.1 0.241 vs Gemini-2.5-Flash 0.713). Measured.
- A two-stage Exchange-then-Decide protocol (share 1-2 facts and one reason the front-runner may be wrong, then summarise and vote) on 18 tasks with 4 agents: GPT-4.1 0.037 to 0.800, Gemini-2.5-Flash 0.173 to 0.727, Gemini-2.5-Flash-Lite 0.043 to 0.743. Measured.

## Methods and models

Hidden Profile task generation pipeline with validity checks, multi-round group discussion followed by a decision, 15 frontier models; ablations on prompting, rounds, group size and disclosure. Skimmed introduction, ablations and conclusion of arXiv HTML; no code repository found in the text.

## Limitations and open questions

Text-only decision tasks with a single correct option; small groups. Open: how the failure scales with N and network topology, and whether exploration incentives (as in animal collective search) fix it.

## Relevance to us

Shows that LLM groups behave like human groups that over-weight shared information, the opposite of the ideal swarm that pools distributed sensing. Directly relevant to collective-decision designs and to [[riedl-2025-emergent]] (synergy), [[cho-2025-herd]] and [[bellina-2026-conformity]] (conformity), and [[schoenegger-2024-wisdom]] (independent aggregation as a baseline).
