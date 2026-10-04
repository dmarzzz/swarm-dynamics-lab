---
id: bisztray-2025-i
type: paper
title: "I Know Which LLM Wrote Your Code Last Summer: LLM generated Code Stylometry for Authorship Attribution"
authors: ["Tamas Bisztray", "Bilel Cherif", "Richard A. Dubniczky", "Nils Gruschka", "Bertalan Borsos", "Mohamed Amine Ferrag", "Attila Kovacs", "Vasileios Mavroeidis", "Norbert Tihanyi"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2506.17323
doi: null
arxiv: "2506.17323"
cite: "Bisztray, T., Cherif, B., Dubniczky, R. A., Gruschka, N., Borsos, B., Ferrag, M. A., Kovacs, A., Mavroeidis, V., & Tihanyi, N. (2025). I Know Which LLM Wrote Your Code Last Summer: LLM generated Code Stylometry for Authorship Attribution. arXiv:2506.17323."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

First systematic study of LLM authorship attribution for C programs. CodeT5-Authorship (encoder-only CodeT5 with a classification head) is evaluated on LLM-AuthorBench, 32,000 compilable C programs from eight LLMs. It reaches 97.56% binary accuracy between GPT-4.1 and GPT-4o and 95.40% five-way accuracy among Gemini 2.5 Flash, Claude 3.5 Haiku, GPT-4.1, Llama 3.3 and DeepSeek-V3.

## Contribution

Extends model attribution to code, relevant to agent swarms that open PRs or publish packages.

## Key results

- 97.56% binary accuracy GPT-4.1 vs GPT-4o (abstract).
- 95.40% five-way accuracy (abstract).

## Methods and models

LLM-AuthorBench of 32,000 C programs; comparison with seven classical and eight transformer classifiers.

## Limitations and open questions

C only; abstract-only reading.

## Relevance to us

Code-generating swarms (package spam, PR floods) could be attributed to a model this way. Connects to the code-and-data lane.
