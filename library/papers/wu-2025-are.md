---
id: wu-2025-are
type: paper
title: 'Are Large Language Models Sensitive to the Motives Behind Communication?'
authors: [Addison J. Wu, Ryan Liu, Kerem Oktar, Theodore R. Sumers, Thomas L. Griffiths]
year: 2025
venue: Advances in Neural Information Processing Systems (NeurIPS 2025)
url: https://arxiv.org/abs/2510.19687
doi: null
arxiv: '2510.19687'
cite: 'Wu, A. J., Liu, R., Oktar, K., Sumers, T. R., & Griffiths, T. L. (2025). Are Large Language Models Sensitive to the Motives Behind Communication? Advances in Neural Information Processing Systems (NeurIPS 2025). arXiv:2510.19687.'
topics: [llm-agent-swarms]
added_by: dmarz/honeypot-vigilance
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Tests "motivational vigilance" in LLMs: whether they discount testimony according to the speaker's incentives. In controlled cognitive-science paradigms, LLM judgements track a rational model of learning from motivated testimony and discount biased sources much as humans do. In a more naturalistic setting with sponsored online adverts, the fit to the rational model is much weaker, partly because extra information distracts from incentives; a steering prompt that makes intentions and incentives salient substantially restores the fit.

## Contribution

Ties LLM source-discounting to a Bayesian model of testimony from cognitive science, showing the capacity exists but is fragile outside clean paradigms.

## Key results

- Controlled paradigms: LLM inferences consistent with rational models of motivated testimony (measured).
- Sponsored adverts: correspondence with the rational model drops (measured); salience steering raises it substantially (measured; abstract gives no numbers).

## Methods and models

Experiments adapted from human cognitive-science studies of testimony, then advert-based vignettes. Abstract only.

## Limitations and open questions

Single-shot judgements, not multi-turn agents; no peer-agent warnings.

## Relevance to us

V3: when a peer says "that endpoint is a honeypot", the hearer should weigh the peer's incentives and evidence. This paper suggests LLMs can do that in clean settings but not reliably in cluttered ones, so a bare rumour may move the hearer's criterion without moving discrimination, which is what V3 predicts. Related: [[robinson-2026-under]].
