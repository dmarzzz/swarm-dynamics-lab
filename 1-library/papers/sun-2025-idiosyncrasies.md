---
id: sun-2025-idiosyncrasies
type: paper
title: "Idiosyncrasies in Large Language Models"
authors: ["Mingjie Sun", "Yida Yin", "Zhiqiu Xu", "J. Zico Kolter", "Zhuang Liu"]
year: 2025
venue: "Proceedings of the 42nd International Conference on Machine Learning (ICML 2025); arXiv preprint"
url: https://arxiv.org/abs/2502.12150
doi: null
arxiv: "2502.12150"
cite: "Sun, M., Yin, Y., Xu, Z., Kolter, J. Z., & Liu, Z. (2025). Idiosyncrasies in Large Language Models. ICML 2025. arXiv:2502.12150."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Shows that the source LLM of a piece of text can be predicted from the text alone. Fine-tuning a text embedding model on outputs from ChatGPT, Claude, Grok, Gemini and DeepSeek gives 97.1% five-way accuracy on held-out data. The idiosyncrasies sit largely in word-level distributions and survive rewriting, translation or summarisation by another LLM, which suggests they are also carried in semantic content.

## Contribution

Clean demonstration that passive text-only attribution between frontier chat models is near-trivial, with an LLM-judge description of each model's quirks.

## Key results

- 97.1% accuracy on the five-way task (ChatGPT, Claude, Grok, Gemini, DeepSeek), chance 20% (abstract).
- Patterns persist after the text is rewritten, translated or summarised by an external LLM (abstract).

## Methods and models

Classification of LLM-generated responses with a fine-tuned text embedding model; analysis of word-level distributions; LLM-as-judge descriptions of idiosyncrasies. Read from abstract only; secondary pages report binary within-family accuracy up to 85.5% for Qwen-2.5 sizes, not checked against the paper.

## Limitations and open questions

Prompts and outputs come from benchmark-style instructions; social-media length posts and system-prompted personas were not tested per the abstract. Targeted rewriting attacks such as [[yuan-2026-forging]] were not in scope.

## Relevance to us

Passive attribution of posts to a model family is cheap, so a cluster of accounts that all classify to one model is a usable weak signal of shared operation. Contrast with targeted forging [[yuan-2026-forging]] and the older stylometry line [[kumarage-2023-neural]], [[huang-2024-authorship]].
