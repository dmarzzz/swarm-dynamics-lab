---
id: chupilkin-2026-artificial
type: paper
title: "Artificial Institutions: How Institutional Design Shapes LLM Simulations"
authors: ["Maxim Chupilkin"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.04020
doi: null
arxiv: '2608.04020'
cite: "Chupilkin, M. (2026). Artificial institutions: How institutional design shapes LLM simulations. arXiv:2608.04020."
topics: [llm-agent-swarms, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "2 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Small repeated induced-value market experiment with LLM traders. Holding agents, private values, costs and payoff-framed instructions fixed, only the exchange rules vary across five institutions: call market, posted-offer, posted-bid, continuous double auction (CDA) and bilateral bargaining. Four model families (gpt-5-mini, gpt-5, claude-sonnet-4-5, gemini-2.5-flash), 10 independent markets x 5 periods per model-institution cell. Efficiency, trade quantity, price distance from equilibrium and surplus split all change with the institution.

## Contribution

Argues, with a controlled design, that the interaction protocol of an LLM simulation is a treatment variable as consequential as the agent architecture.

## Key results

- Pooled efficiency: call market 88.6%, posted-offer and posted-bid about 66%, CDA 71.5%, bilateral bargaining 56.4%.
- Model x institution interaction: Gemini reaches 100.0% in the call market and 81.0% in bargaining but 35.2% in the CDA; Claude Sonnet shows the opposite pattern (stronger in CDA, weaker in call market).
- 95% bootstrap CIs from 2,000 resamples of independent markets, stratified by model.

## Methods and models

Python implementation calling provider APIs (OpenAI Responses, Anthropic Messages, Gemini); one demand and one supply schedule; sparse prompts; no monetary incentives.

## Limitations and open questions

Author lists: one demand/supply schedule, five periods, four models, no training; results are about these rules, not general market competence. No code repository found.

## Relevance to us

Lesson for any sim we bootstrap: report and vary the interaction protocol (who sees what, ordering, clearing rule) as a first-class factor, and never rank models from a single institution. Pairs with [[larooij-2025-do]] on validation and with market sims such as [[gh-freedomintelligence-twinmarket]].
