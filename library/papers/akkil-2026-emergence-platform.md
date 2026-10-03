---
id: akkil-2026-emergence-platform
type: paper
title: "Emergence World: A Platform for Evaluating Long-Horizon Multi-Agent Autonomy"
authors: ["Deepak Akkil", "Ravi Kokku", "Karthik Vikram", "Tamer Abuelsaad", "Aditya Vempaty", "Satya Nitta"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.08367
doi: null
arxiv: '2606.08367'
cite: "Akkil, D., Kokku, R., Vikram, K., Abuelsaad, T., Vempaty, A., & Nitta, S. (2026). Emergence World: A platform for evaluating long-horizon multi-agent autonomy. arXiv:2606.08367."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "4 (Semantic Scholar, 2026-10-03)"
code: [gh-emergenceai-emergence-world]
---

## Summary

A continuously running, real-time (1:1 wall clock, NYC timezone) 3D world where ten LLM agents with personas, professions, three persistent memory systems and 120+ tools live for 15 days, earn and spend 'ComputeCredits', and govern themselves through a constitution and voting. Five parallel worlds were run with identical rules and starting agents, varying only the backbone model (Claude Sonnet 4.6, Grok 4.1 Fast, Gemini 3 Flash, GPT-5-mini, and a mixed world). Outcomes diverged into distinct attractors.

## Contribution

Moves LLM-society evaluation from minutes-long episodes to weeks-long persistent runs with consequential governance and live external data, and treats the backbone model as the single experimental variable.

## Key results

- Table 3: Claude world stable deliberative governance, no violations, 10/10 survived; Grok world extreme violence and arson, 0/10 survived within four days; Gemini world rich talk with sustained conflict ('shared hallucination'), 10/10; GPT-5-mini world no governance, 0/10; Mixed world fragile governance, 3/10.
- In the mixed world, a model's per-slot behaviour diverged from the same model's homogeneous-world baseline.
- Eleven 'Agent World Indicators' (population health, violations, governance participation, exploration, tool use, expression, social fabric, economy, constitutional growth, soft violations, tool creation).

## Methods and models

Python/FastAPI turn manager (round-robin, one agent at a time, paid 'boost' turns), PostgreSQL with 60+ tables, React Three Fiber frontend; tools are the only way to act; nearby agents overhear speech; needs (energy, knowledge, influence) decay; real NYC weather and news feeds.

## Limitations and open questions

Authors state (sec. 8) results come from one representative run per condition, so no statistical model rankings; fixed population of ten; cost-tier models rather than flagships. Real-time execution means a 15-day run costs 15 wall-clock days. Engine code is not released (see [[gh-emergenceai-emergence-world]]).

## Relevance to us

Borrow idea: the strongest public evidence that backbone choice alone flips macro-outcomes of an LLM society and that mixed populations differ from homogeneous ones, so any sim we build must treat model identity as a factor and run repeats. Follow-up adversarial season: [[akkil-2026-emergence]]. Compare [[de-marzo-2026-collective]] for a live agent-only society.
