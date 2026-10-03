---
id: beren-2023-scaffolded
type: blog
title: "Scaffolded LLMs as natural language computers"
authors: ["Beren Millidge (beren)"]
year: 2023
url: https://www.lesswrong.com/posts/43C3igfmMrE9Qoyfe/scaffolded-llms-as-natural-language-computers
site: LessWrong (crosspost from beren.io)
topics: [llm-agent-swarms]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 2
---

## Summary

April 2023 post (98 points, 10 comments), written in the AutoGPT moment, proposing that a scaffolded LLM system is a von Neumann computer operating on text. The mapping: LLM as CPU (type signature strings to strings rather than bits to bits), prompt and context as RAM, vector database as disk with retrieval heuristics as the memory controller, plugins as drivers, and the scaffolding code (ReAct loops, recursive summarisers) as the programs. From this he defines performance units: context length as RAM (GPT-4's 8k tokens compared to a Commodore 64) and a "natural language operation" (NLOP, roughly one 100-token generation), giving about 1 NLOP/s for GPT-4 and 10 for GPT-3.5, with latency rather than cost as the binding constraint. He predicts continued exponential improvement for a few years, then a cap around $10B per training run after which efficiency dominates. Two sections matter for us: "programming languages" (chain of thought, selection-inference, reflection as assembly-level primitives, with higher abstractions blocked by NLOP scarcity because abstractions cost overhead), and "execution model", where he observes that since an LLM can be called arbitrarily many times in parallel, the natural execution model is an expanding DAG of parallel NLOPs constrained only by the program's seriality, not the hardware. The post truncates in our fetch at that point; later sections were not read. Conceptual essay, no experiments.

## Key claims

- Scaffolded LLM systems have converged on the von Neumann architecture, with text as the data type.
- Useful performance metrics are context length (RAM) and NLOPs per second; in 2023 latency, not price, limited what scaffolds could do.
- The native execution model of LLM systems is parallel: a DAG of calls bounded by task seriality, which is where multi-agent fan-out comes from.

## Evidence quality

Analogy-driven essay with back-of-envelope numbers (NLOP rates, context sizes, training-run costs circa 2023), no measurements. Many specifics are dated; the framing has held up.

## Relevance to us

Background for llm-agent-swarms. The execution-model point anticipates the swarm-as-parallel-inference framing that Ord quantifies in [[ord-2026-swarm]]: if the program is a DAG of NLOPs, a swarm is the parallel schedule of that DAG, and the stepping-on-toes exponent λ is the measure of how much seriality the task imposes. Also relevant to Soto's blurry single/multi-agent boundary in [[soto-2024-need]]. Not a citation for any current number.
