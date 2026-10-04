---
id: larooij-2025-do
type: paper
title: "Do Large Language Models Solve the Problems of Agent-Based Modeling? A Critical Review of Generative Social Simulations"
authors: ["Maik Larooij", "Petter Törnberg"]
year: 2025
venue: "arXiv"
url: https://arxiv.org/abs/2504.03274
doi: null
arxiv: "2504.03274"
cite: "Larooij, M., & Törnberg, P. (2025). Do Large Language Models Solve the Problems of Agent-Based Modeling? A Critical Review of Generative Social Simulations. arXiv preprint arXiv:2504.03274."
topics: [llm-agent-swarms, meta]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "45 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

A systematic review of 35 generative agent-based modelling papers (LLM agents that interact and are meant to represent human behaviour), classifying what each simulates and how it is validated. Fifteen of 35 are validated only subjectively and 22 use subjective validation as their only primary technique; most rely on a single model run and none performs a sensitivity analysis. The authors argue LLMs worsen rather than solve ABM's historical problems of calibration, validation, comparability and cost.

## Contribution

The first systematic audit of validation practice in LLM social simulation, framed against the older ABM validation literature (Sargent's operational validity, Windrum et al.). It turns diffuse scepticism into counts per paper and per technique.

## Key results

- 35 papers included (Scopus search on 2025-03-27 plus backward snowballing from five surveys).
- Most-simulated phenomena: conversations/content (10), social dynamics (10), profile alignment (8), network propagation (8).
- Validation: human-like judgement is the primary technique in 12 papers, well-known social patterns in 14, human-generated data in 12, internal consistency in 1.
- 15/35 validated only subjectively; 22/35 use only subjective primary validation.
- When synthetic and human data are compared quantitatively, LLM text is longer, more polite and more articulate than human text.
- OASIS's herd effect was stronger in LLM agents than in humans (reported via the reviewed paper).
- Most studies use a single run; none does sensitivity analysis, attributed to LLM cost.

## Methods and models

Qualitative systematic review. Inclusion: LLM-based agents, multiple interacting agents, intended to represent humans; excludes task-completion frameworks (CAMEL, MetaGPT, AutoGen). Each paper coded for target phenomenon (6 individual, 3 group categories) and validation technique on two axes (internal/external, subjective/objective) into five categories, primary vs. secondary.

## Limitations and open questions

Single-coder classification as far as the paper states; 35 papers is a small, early sample (cut-off March 2025). It critiques without offering a working validation protocol. It treats 'LLM as judge' as invalid by construction, which some benchmark authors dispute.

## Relevance to us

This is the checklist our sim work must pass: multiple seeds per condition, a sensitivity sweep over prompts and models, validation against an external macro pattern rather than 'believability', and a stated purpose (thought experiment vs. calibrated model). It covers [[gh-camel-ai-oasis]], [[gh-altera-al-project-sid]], [[park-2023-generative]], [[zhou-2023-sotopia]], [[chuang-2023-simulating]] and [[chen-2023-agentverse]]. Pair with [[zhou-2025-pimmur]] and [[ye-2026-stop]].
