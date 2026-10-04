---
id: rai-2026-when
type: paper
title: 'When Too Many Cooks Spoil the Broth: Three Failure Modes of Multi-Agent LLM Reliability'
authors: [Aradhana Rai, Vijay K. Madisetti]
year: 2026
venue: ACM AI Letters
url: https://api.crossref.org/works/10.1145/3847307
doi: 10.1145/3847307
arxiv: null
cite: 'Rai, A., & Madisetti, V. K. (2026). When Too Many Cooks Spoil the Broth: Three Failure Modes of Multi-Agent LLM Reliability. ACM AI Letters. https://doi.org/10.1145/3847307'
topics: [llm-agent-swarms]
added_by: shadow/sol-1
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Tests three assumptions of multi-agent LLM systems on GPT-4o, Claude Sonnet 4.6 and Llama-3.3-70B. Self-confidence and peer resistance dissociate: Claude shows the strongest self-confidence signal yet accepts every deliberately wrong peer output. Four independent GPT-4o instances agree on the same wrong answer 56% of the time on obscure factual queries, against 0.4% expected under independence (140 times). A preregistered cross-family replication (N = 200 queries, three architecturally distinct families) gives 55% three-way wrong agreement, statistically indistinguishable from the same-family baseline (one-sided binomial p = 0.41). Verifier choice changes error propagation by 42 points. The authors name query-inherent rarity, not shared training, as the main driver of correlated failure.

## Contribution

A preregistered negative result for the cross-family lever on rare factual queries: family diversification did not reduce correlated hallucination.

## Key results

- Same-model wrong-answer agreement 56% vs 0.4% under independence (measured).
- Cross-family three-way wrong agreement 55%, not different from same-family (measured, preregistered, N = 200).

## Methods and models

GPT-4o, Claude Sonnet 4.6, Llama-3.3-70B; obscure factual queries; deliberately wrong peer outputs. Abstract read via the Crossref record; full text not opened.

## Limitations and open questions

Abstract only; obscure factual recall is the setting where shared ignorance is most likely, so the result may not transfer to reasoning tasks where cross-family mixing helps ([[liu-2026-llms]], [[begin-2026-preference]]).

## Relevance to us

The strongest counter-evidence to "cross-family diversity lowers the ceiling": whether diversity helps depends on whether the error source is the item (rarity) or the model. A board N_eff experiment should vary item difficulty as well as model mix.
