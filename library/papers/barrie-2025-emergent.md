---
id: barrie-2025-emergent
type: paper
title: Emergent LLM behaviors are observationally equivalent to data leakage
authors:
- Christopher Barrie
- Petter Törnberg
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2505.23796
doi: null
arxiv: '2505.23796'
cite: Barrie, C., & Törnberg, P. (2025). Emergent LLM behaviors are observationally equivalent to data leakage. arXiv preprint arXiv:2505.23796.
topics:
- llm-agent-swarms
- meta
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 0 (OpenAlex, 2026-10-03); 14 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

A direct critique of [[ashery-2024-emergent]], which reported that LLMs paired in a naming game spontaneously develop shared conventions and collective biases. Barrie and Törnberg argue the results are better explained by data leakage: the models recognise the structure of the coordination game, which is widely described in their training data, and recall its typical outcomes, rather than exhibiting emergent conventions. Despite the original authors' mitigations, they present several analyses showing models identify the game and recall outcomes, so the observed behaviour is indistinguishable from memorisation. They close with alternative strategies and a broader reflection on using LLMs in social-science models.

## Contribution

The main negative/critical result against "emergent social conventions" in LLM populations, and a general warning for any LLM-swarm study that uses well-known paradigms. Read with [[zhou-2025-pimmur]] (Unawareness criterion).

## Key results

- Claimed: models can identify the naming game and recall its outcomes; observed "emergence" is observationally equivalent to memorisation.

## Methods and models

Probing analyses of the LLMs used by Ashery et al. for recognition of the game and recall of outcomes. Details not checked.

## Limitations and open questions

Abstract-level read. Observational equivalence does not prove memorisation is the cause; later work with arbitrary labels, logit-level policies and mean-field fits ([[flint-2026-group]], [[de-nobili-2026-microscopic]]) partly answers the critique. Whether the original authors replied is not checked.

## Relevance to us

Any hackathon experiment on LLM consensus must use disguised tasks or novel games and test for recognition. Related: [[de-marzo-2024-ai]], [[tanaka-2026-when]].
