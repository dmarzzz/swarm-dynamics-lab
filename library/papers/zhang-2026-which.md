---
id: zhang-2026-which
type: paper
title: "Which Model Is Actually Serving You? IRIS: Budgeted Black-Box Auditing of Model Substitution and Routing Dilution in LLM Gateways"
authors: ["Yuewei Zhang", "Zhi-Hai Zhang", "Hanzhang Qin"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2607.20860
doi: null
arxiv: "2607.20860"
cite: "Zhang, Y., Zhang, Z. H., & Qin, H. (2026). Which Model Is Actually Serving You? IRIS: Budgeted Black-Box Auditing of Model Substitution and Routing Dilution in LLM Gateways. arXiv:2607.20860."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

IRIS audits LLM gateways that may substitute a cheaper backend on every request or route only a fraction epsilon of requests to it. Using only returned text from prompts asking for random numbers or strings, it verifies the backend (0.99 AUROC on an intra-family Qwen3 ladder), detects epsilon=0.3 dilution at 0.85 mean power with 0.017 false-positive rate on OpenRouter, recovers epsilon within 0.04, and in a live audit flags 14 of 15 same-model provider pairs via quantisation and kernel deviations.

## Contribution

Handles mixtures (partial routing), which is how an operator could blend models across a swarm.

## Key results

- 0.99 AUROC backend verification on Qwen3 ladder (abstract).
- epsilon=0.3 dilution caught at 0.85 mean power, 0.017 FPR; epsilon recovered within 0.04 (abstract).
- 14 of 15 same-model provider pairs flagged in a live cross-provider audit (abstract).
- Adaptive budget allocation lifts matched-budget target-hit rate from 73% to 87% (abstract).

## Methods and models

Random-number and random-string elicitation; text-only fingerprints; self-sized query budget fitted from a pilot.

## Limitations and open questions

Abstract-only reading. Targets gateways the auditor can query repeatedly.

## Relevance to us

Random-number prompts are cheap, innocuous probes; mixture estimation is relevant when a swarm is served by several models. See also [[bruckner-2026-one]], [[gao-2024-model]].
