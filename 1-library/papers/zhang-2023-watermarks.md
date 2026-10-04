---
id: zhang-2023-watermarks
type: paper
title: 'Watermarks in the Sand: Impossibility of Strong Watermarking for Generative Models'
authors:
- Hanlin Zhang
- Benjamin L. Edelman
- Danilo Francati
- Daniele Venturi
- Giuseppe Ateniese
- Boaz Barak
year: 2023
venue: ICML 2024
url: https://arxiv.org/abs/2311.04378
doi: null
arxiv: '2311.04378'
cite: 'Zhang, H., Edelman, B. L., Francati, D., Venturi, D., Ateniese, G., & Barak, B. (2023). Watermarks in the Sand: Impossibility of Strong Watermarking for Generative Models. In Proceedings of the 41st International Conference on Machine Learning (ICML 2024). arXiv:2311.04378.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 111 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Proves that strong watermarking (one a bounded attacker cannot remove without significant quality loss) is impossible under natural assumptions, even when detection uses a secret key. The attack needs only a quality oracle and a perturbation oracle that induces a mixing random walk over high-quality outputs, both plausible for an attacker weaker than the watermarked model. Instantiated, it removes the watermarks of Kirchenbauer et al., Kuditipudi et al. and Zhao et al. with minor quality loss.

## Contribution

Impossibility theorem for robust generative watermarks plus a generic, scheme-agnostic removal attack.

## Key results

- Proved (abstract): strong watermarking impossible under the stated assumptions.
- Measured (abstract): attack removes three LLM watermark schemes with minor quality degradation.

## Methods and models

Random-walk attack with quality and perturbation oracles; theoretical proof. Abstract read only.

## Limitations and open questions

Attack costs compute per output; at swarm volume the cost may matter (not quantified in abstract). Abstract depth.

## Relevance to us

Watermarks cannot be relied on to detect a motivated swarm operator; they only catch careless or cooperative use. Pairs with [[jovanovic-2024-watermark]] and [[dathathri-2024-scalable]].
