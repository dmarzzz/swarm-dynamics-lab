---
id: yang-2025-challenge
type: paper
title: "The Challenge of Identifying the Origin of Black-Box Large Language Models"
authors: ["Ziqing Yang", "Yixin Wu", "Yun Shen", "Wei Dai", "Michael Backes", "Yang Zhang"]
year: 2025
venue: "Findings of the Association for Computational Linguistics: EMNLP 2026 (per arXiv comment); arXiv preprint"
url: https://arxiv.org/abs/2503.04332
doi: null
arxiv: "2503.04332"
cite: "Yang, Z., Wu, Y., Shen, Y., Dai, W., Backes, M., & Zhang, Y. (2025). The Challenge of Identifying the Origin of Black-Box Large Language Models. arXiv:2503.04332."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "12 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Addresses identifying the origin model of a black-box LLM that a third party may have fine-tuned and exposed only via API. PlugAE optimises adversarial token embeddings in continuous space and plugs them into the LLM as customisable copyright tokens on a target query set, so that derivatives can later be traced. Experiments report better accuracy and robustness than state-of-the-art watermarking and fingerprinting for identifying fine-tuned derivatives.

## Contribution

A proactive, owner-side fingerprint for tracing fine-tuned derivatives.

## Key results

- Outperforms model watermarking and fingerprinting baselines in accuracy and robustness for identifying fine-tuned derivatives (abstract; no numbers given).

## Methods and models

Optimised adversarial embeddings inserted by the model owner before release; query-based verification.

## Limitations and open questions

Requires the model owner to act before release; does not help with arbitrary open-weight models already in circulation.

## Relevance to us

Background for the ownership-fingerprinting branch. Relevant to swarms only if the base-model owner cooperates, as in the vendor-side route of [[chocron-2026-who]].
