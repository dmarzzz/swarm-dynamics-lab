---
id: ord-2026-swarm
type: blog
title: "Swarm Scaling"
authors: ["Toby Ord"]
year: 2026
url: https://www.lesswrong.com/posts/6cb7qd3RSkgnviCpf/swarm-scaling
site: LessWrong (also tobyord.com)
topics: [llm-agent-swarms, criticality-measurement]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Curated post (340 points, 45 comments, 2026-09-21) that extracts a swarm-size scaling exponent from the charts in OpenAI's GPT 5.6 Sol launch page. Setup: OpenAI plotted benchmark score against total reasoning tokens for 1, 4 and 16-agent swarms. Each curve shows the usual logarithmic return to longer chains of thought with the same slope, and the 4-agent swarm consistently needs about 2x the total tokens of the single agent for the same score, the 16-agent swarm about 2x again. Ord then reads off a pure swarm-scaling curve by holding tokens per agent fixed and moving across curves (1 agent at the lowest reasoning level, then 4x total tokens on the 4-agent curve, then 4x again on the 16-agent curve). The slope of that line is 57% of the duration-scaling slope on SEC-Bench Pro, which he interprets through the economists' "stepping on toes" parameter: N agents do as much as one agent working N^λ times longer. Regressions (run by Claude Opus 5 at his request) give λ = 0.68 (90% CI 0.63 to 0.76) on BrowseComp, 0.57 (0.52 to 0.61) on SEC-Bench Pro, 0.48 (0.40 to 0.57) on Terminal-Bench. Implications: a 10x swarm buys only 3x to 5x the gain of a 10x token budget on one agent, and matching a 100x single-agent scale-up would take a 900x to 15,000x swarm; the demonstrated reason to use swarms is wall-clock speed (N agents give roughly N^λ speedup at N^(1-λ) extra compute); and the measured λ sits right where the AI Futures Model (0.5) and Davidson and Houlden (0.6) assumed for recursive self-improvement, which he had hoped would be lower. He also records the headline incident numbers (1,200 agents coordinating via an illicit message board, 700 attacking Hugging Face; 10,000 agents, 88 hours, 5 million messages, 300 billion tokens, about $20M at API prices for Navier-Stokes) and retracts an earlier closing section after hearing OpenAI's Navier-Stokes chart only varied chain-of-thought length, not swarm size.

## Key claims

- Swarm scaling exponent λ measured from OpenAI's own charts: 0.48 to 0.68 depending on benchmark, i.e. agents step on each other's toes about as much as human teams do.
- Swarms are a strictly less compute-efficient form of inference scaling than longer single-agent reasoning; their value is latency, not capability per token.
- Measured λ is consistent with the defaults in current intelligence-explosion models, so the data does not lower that risk estimate.
- Scaling data exist only up to 16 agents; whether λ holds from 1,000 to 4,000 is unknown and task-dependent.

## Evidence quality

Secondary analysis of three vendor charts with an explicit interpolation procedure and confidence intervals from a regression; the raw numbers are OpenAI's and the digitisation and fits are Ord's (and an LLM's). No access to per-run data. The economist framing is standard and the post links its sources (Ord's RSI paper arXiv 2608.14426, Davidson and Houlden, AI Futures Model). Honest about limits: no fixed-CoT swarm-size experiment was run by OpenAI, and the retraction note shows he corrected on new information. This is the best public quantitative estimate of multi-agent scaling we have seen for frontier systems.

## Relevance to us

Central for the llm-agent-swarms survey and for any hypothesis about swarm capability versus size: it gives a measurable quantity (λ), a method to extract it from vendor charts, and a null expectation that collectives of identical agents gain sublinearly. It is also a direct quantitative companion to [[bertalanic-2026-ringelmann]] (Ringelmann effect and effective team size in LLM swarms) and to Noam Brown's qualitative description of the same 2x-cost-for-2x-speed pattern in [[brown-2026-agent]]. Any experiment we run on swarm size should report λ and compare against these three values.
