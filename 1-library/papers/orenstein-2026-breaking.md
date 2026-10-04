---
id: orenstein-2026-breaking
type: paper
title: Breaking and Defending LLM-Powered Social Media Bot Detection Systems
authors:
- Nof Orenstein
- Yoni Birman
year: 2026
venue: Pragmatic Cybersecurity; ACISP 2026
url: https://arxiv.org/abs/2608.15893
doi: 10.53941/pc.2026.100010
arxiv: '2608.15893'
cite: Orenstein, N., & Birman, Y. (2026). Breaking and Defending LLM-Powered Social Media Bot Detection Systems. Pragmatic Cybersecurity, 1(2), 10. https://doi.org/10.53941/pc.2026.100010 (also ACISP 2026; arXiv:2608.15893).
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Studies attacks on bot detectors that use LLMs as classifiers. Two adversarial strategies that exploit the semantic and contextual reasoning of LLM-based classifiers cut detection accuracy by up to 48%. The proposed defence, LSABRE, is a multi-LLM ensemble that keeps 86% accuracy under strong adaptive attack.

## Contribution

Shows that LLM-based detectors add a new attack surface (manipulating the detector's reasoning), not only a stronger classifier.

## Key results

- Two attacks reduce LLM-based bot detection accuracy by up to 48% (abstract).
- LSABRE multi-LLM ensemble keeps 86% accuracy under adaptive adversarial pressure.

## Methods and models

LLM classifiers for bot detection; adversarial prompt and content attacks; ensemble defence. Abstract-level read.

## Limitations and open questions

Benchmarks and threat models not recorded here; numbers are from the authors' own setup.

## Relevance to us

If we use LLMs to judge whether accounts are agents, the agents can target the judge. Compare [[feng-2024-what]] (LLM detectors up to 9.1% better, LLM evasion up to 29.6% worse).
