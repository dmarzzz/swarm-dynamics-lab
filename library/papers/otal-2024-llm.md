---
id: otal-2024-llm
type: paper
title: 'LLM Honeypot: Leveraging Large Language Models as Advanced Interactive Honeypot Systems'
authors:
- Hakan T. Otal
- M. Abdullah Canbaz
year: 2024
venue: 2024 IEEE Conference on Communications and Network Security (CNS)
url: https://arxiv.org/abs/2409.08234
doi: 10.1109/CNS62487.2024.10735607
arxiv: '2409.08234'
cite: 'Otal, H. T., & Canbaz, M. A. (2024). LLM Honeypot: Leveraging Large Language Models as Advanced Interactive Honeypot Systems. In 2024 IEEE Conference on Communications and Network Security (CNS), pp. 1–6. https://doi.org/10.1109/CNS62487.2024.10735607'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Fine-tunes a pre-trained open-source language model on a dataset of attacker commands and the corresponding system responses so that it can act as an interactive SSH honeypot. Evaluation used similarity metrics against real responses plus a live deployment, and the authors report accurate and informative responses.

## Contribution

Shows the self-hosted, fine-tuned route to LLM honeypots (no cloud API), one of the architectural directions [[bridges-2025-sok]] recommends.

## Key results

- Fine-tuned model generates responses close to real system output by similarity metrics; live deployment reported (abstract; no numbers in abstract).

## Methods and models

Data collection, prompt engineering, model selection, supervised fine-tuning. Abstract-level read. Venue and pages confirmed via the Crossref record for the DOI.

## Limitations and open questions

Abstract only; evaluated mostly by text similarity rather than by attacker engagement.

## Relevance to us

Background for building local decoys at swarm scale without per-call API cost. Related: [[sladic-2023-llm]].
