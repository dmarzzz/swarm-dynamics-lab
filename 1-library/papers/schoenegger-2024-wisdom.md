---
id: schoenegger-2024-wisdom
type: paper
title: "Wisdom of the silicon crowd: LLM ensemble prediction capabilities rival human crowd accuracy"
authors:
- "Philipp Schoenegger"
- "Indre Tuminauskaite"
- "Peter S. Park"
- "Rafael Valdece Sousa Bastos"
- "Philip E. Tetlock"
year: 2024
venue: "Science Advances"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC11800985/
doi: 10.1126/sciadv.adp1528
arxiv: "2402.19379"
cite: "Schoenegger, P., Tuminauskaite, I., Park, P. S., Bastos, R. V. S., & Tetlock, P. E. (2024). Wisdom of the silicon crowd: LLM ensemble prediction capabilities rival human crowd accuracy. Science Advances, 10(45), eadp1528. https://doi.org/10.1126/sciadv.adp1528"
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: "46 (OpenAlex W4404166124, published version, 2026-10-03); 2 (OpenAlex W4392575219, arXiv record)"
code: []
---

## Summary

Tests whether the wisdom-of-crowds effect holds for a crowd of different LLMs, with no interaction between them. Twelve LLMs forecast 31 binary real-world questions during a three-month tournament; their median forecast per question is compared with the aggregate of 925 human forecasters. In a preregistered analysis the LLM crowd beats the 50% no-information baseline and is statistically indistinguishable from the human crowd. Study 2 shows that GPT-4 and Claude 2 improve when given the human median as input, though simple averaging of human and machine forecasts does better still.

## Contribution

The cleanest evidence that independent aggregation across heterogeneous models delivers crowd-level accuracy, i.e. a diversity-prediction-theorem result for LLMs. It is the non-interacting baseline against which interacting LLM swarms (debate, consensus) must be judged, complementing the same-model sampling result of [[li-2024-more]].

## Key results

- Brier score: LLM crowd 0.20 (SD 0.12) vs human crowd 0.19 (SD 0.19) vs 50% baseline 0.25; LLM vs human difference not significant (p = 0.850); equivalence within medium-effect bounds (exploratory). Measured, 1,007 forecasts.
- Acquiescence bias: mean LLM forecast 57.35% despite 14 of 31 questions resolving positive. Measured.
- Study 2: exposure to the human median improves Brier scores of GPT-4 (0.17 to 0.14) and Claude 2 (0.22 to 0.15), reported as 18% and 32% in the journal version (17-28% in the arXiv abstract). Measured.

## Methods and models

Models: GPT-4, GPT-4 with Bing, Claude 2, GPT-3.5-Turbo-Instruct, Solar-0-70B, Llama-2-70B, PaLM 2, Coral (Command), Mistral-7B-Instruct, Bard, Falcon-180B, Qwen-7B-Chat. Aggregation: median across models per question. Questions from a Metaculus tournament; analyses preregistered on OSF with Benjamini-Hochberg correction. I read the PMC full-text summary of results and methods, not every supplement.

## Limitations and open questions

Only 31 questions, so power is limited; equivalence claims are exploratory. Model errors are correlated (shared training data), which the diversity theorem says limits crowd gains; the paper does not measure error correlation directly. No interaction among models, so it says nothing about herding.

## Relevance to us

Gives the independent-aggregation baseline for any LLM-swarm decision experiment. Interaction can only help if it beats this; [[cho-2025-herd]], [[weng-2025-do]] and [[bellina-2026-conformity]] show how social influence erodes independence, the classical mechanism by which crowds lose their wisdom (Lorenz et al. 2011). Related: [[burton-2024-how]].
