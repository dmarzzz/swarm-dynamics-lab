---
id: vallinder-2024-cultural
type: paper
title: Cultural Evolution of Cooperation among LLM Agents
authors:
- Aron Vallinder
- Edward Hughes
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2412.10270
doi: null
arxiv: '2412.10270'
cite: Vallinder, A., & Hughes, E. (2024). Cultural evolution of cooperation among LLM agents. arXiv preprint arXiv:2412.10270.
topics:
- llm-agent-swarms
- marl-emergence
added_by: dmarz/llm-agent-swarms
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "37 (Semantic Scholar, 2026-10-03); OpenAlex has no matching record for this arXiv DOI"
code: []
---

## Summary

Studies whether societies of LLM agents evolve indirect reciprocity across generations in an iterated Donor Game where agents can see peers' recent behaviour. Claude 3.5 Sonnet societies achieve significantly higher average scores than Gemini 1.5 Flash, which outperforms GPT-4o. Claude 3.5 Sonnet also exploits an optional costly-punishment mechanism to score higher, while the others do not. Outcomes vary across random seeds, suggesting sensitive dependence on initial conditions.

## Contribution

Applies cultural-evolution methodology (generational selection of strategies) to LLM populations and proposes cooperation-over-generations as a benchmark.

## Key results

- Model ranking for evolved cooperation: Claude 3.5 Sonnet > Gemini 1.5 Flash > GPT-4o (abstract).
- Seed-to-seed variation in emergent outcomes (abstract).

## Methods and models

Generational donor game with reputation information and optional punishment; strategies as natural-language descriptions passed between generations. Code not checked.

## Limitations and open questions

Few models and seeds; strategy space defined by prompts. Abstract-level read.

## Relevance to us

Evidence that LLM collectives are path-dependent and model-specific; relevant to marl-emergence comparisons with learned cooperation.
