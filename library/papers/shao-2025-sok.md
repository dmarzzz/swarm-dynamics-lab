---
id: shao-2025-sok
type: paper
title: "SoK: Large Language Model Copyright Auditing via Fingerprinting"
authors: ["Shuo Shao", "Yiming Li", "Yu He", "Hongwei Yao", "Wenyuan Yang", "Dacheng Tao", "Zhan Qin"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2508.19843
doi: null
arxiv: "2508.19843"
cite: "Shao, S., Li, Y., He, Y., Yao, H., Yang, W., Tao, D., & Qin, Z. (2025). SoK: Large Language Model Copyright Auditing via Fingerprinting. arXiv:2508.19843."
topics: [swarm-detection, meta]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Systematisation of knowledge on LLM fingerprinting for copyright auditing. It classifies white-box methods by feature source (static, forward pass, backward pass) and black-box methods by query strategy (untargeted or targeted), and introduces LeaFBench: 7 foundation models, 149 model instances and 13 post-development techniques including fine-tuning, quantisation, system prompts and RAG, to compare methods under realistic deployment.

## Contribution

First benchmarked SoK of LLM fingerprinting; LeaFBench is the shared testbed later papers ([[wang-2026-who]]) cite.

## Key results

- Benchmarking on LeaFBench reveals strengths and weaknesses of existing methods (abstract; no numbers).

## Methods and models

Taxonomy plus benchmark over 149 instances with parameter-altering and parameter-independent modifications.

## Limitations and open questions

Ownership framing; does not cover agent behaviour or network side channels. Abstract-only reading.

## Relevance to us

Review article for the fingerprinting branch. Other reviews: [[liu-2026-implicit]], [[huang-2024-authorship]].
