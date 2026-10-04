---
id: wimbauer-2026-fingerprinting
type: paper
title: "Fingerprinting Inference Systems of Large Language Models"
authors: ["Anna Wimbauer", "Jonas Möller", "Erik Imgrund", "Konrad Rieck"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.29979
doi: null
arxiv: "2605.29979"
cite: "Wimbauer, A., Möller, J., Imgrund, E., & Rieck, K. (2026). Fingerprinting Inference Systems of Large Language Models. arXiv:2605.29979."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Shows that the inference system around an LLM (inference engine, attention backend, hardware platform) induces small numerical deviations that propagate into observable text. A prompt-response fingerprinting method identifies these components reliably, even at non-zero temperature. Preventing it would require eliminating numerical differences across hardware and software stacks, so the authors propose only partial mitigations.

## Contribution

Extends attribution below the model to the serving stack, a possible handle for linking agents that share infrastructure.

## Key results

- Inference engine, attention backend and hardware identified reliably from outputs, including at non-zero temperature (abstract; no numbers).

## Methods and models

Query-response analysis of numerical deviation signatures across stacks.

## Limitations and open questions

Abstract-only reading; precision on cloud APIs with mixed hardware unknown.

## Relevance to us

If two swarm agents share both model and serving stack, they likely share an operator or provider. Speculative for social bots, more practical for self-hosted swarms. Related: [[ellis-2026-black]].
