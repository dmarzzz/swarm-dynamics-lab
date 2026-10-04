---
id: kirchenbauer-2023-reliability
type: paper
title: On the Reliability of Watermarks for Large Language Models
authors:
- John Kirchenbauer
- Jonas Geiping
- Yuxin Wen
- Manli Shu
- Khalid Saifullah
- Kezhi Kong
- Kasun Fernando
- Aniruddha Saha
- Micah Goldblum
- Tom Goldstein
year: 2023
venue: ICLR 2024
url: https://arxiv.org/abs/2306.04634
doi: null
arxiv: '2306.04634'
cite: Kirchenbauer, J., Geiping, J., Wen, Y., Shu, M., Saifullah, K., Kong, K., Fernando, K., Saha, A., Goldblum, M., & Goldstein, T. (2023). On the Reliability of Watermarks for Large Language Models. In International Conference on Learning Representations (ICLR 2024). arXiv:2306.04634.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 243 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Tests whether watermarked text stays detectable after human rewriting, paraphrasing by a non-watermarked LLM, or mixing into longer human documents. Watermarks survive: paraphrases leak n-grams of the original, so detection succeeds given enough tokens; after strong human paraphrasing about 800 tokens suffice at a 1e-5 false-positive rate. Introduces detectors for short watermarked spans inside long documents.

## Contribution

Shows watermark evidence accumulates with token count, a sample-size argument like [[chakraborty-2023-possibilities]].

## Key results

- Measured (abstract): after strong human paraphrasing the watermark is detectable after about 800 tokens on average at FPR 1e-5.

## Methods and models

Human and machine paraphrase attacks; copy-paste mixing; windowed detection schemes. Abstract read only.

## Limitations and open questions

Assumes the original was watermarked by a cooperating provider. Abstract depth.

## Relevance to us

Pooling tokens across many posts from one account would accumulate watermark evidence, a possible account-level test for swarms built on watermarked APIs.
