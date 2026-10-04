---
id: gao-2024-model
type: paper
title: "Model Equality Testing: Which Model Is This API Serving?"
authors: ["Irena Gao", "Percy Liang", "Carlos Guestrin"]
year: 2024
venue: "International Conference on Learning Representations (ICLR 2025); arXiv preprint"
url: https://arxiv.org/abs/2410.20247
doi: null
arxiv: "2410.20247"
cite: "Gao, I., Liang, P., & Guestrin, C. (2024). Model Equality Testing: Which Model Is This API Serving?. ICLR 2025. arXiv:2410.20247."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "56 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Formalises Model Equality Testing: a two-sample test of whether a black-box API samples from the same distribution as a reference model. An MMD test with a simple Hamming string kernel reaches a median 77.4% power against quantisation, watermarking and fine-tuning distortions with about 10 samples per prompt. Applied to commercial endpoints for four Llama models in summer 2024, 11 of 31 endpoints served distributions different from Meta's reference weights.

## Contribution

Statistical framing (two-sample testing) for "is this the model it claims to be", with an in-the-wild measurement of endpoint deviation.

## Key results

- Median 77.4% power against a range of distortions with an average of 10 samples per prompt (abstract).
- 11 of 31 commercial Llama endpoints deviated from reference weights (abstract).

## Methods and models

Kernel two-sample tests (MMD) over sampled completions; string kernel related to Hamming distance. Code: github.com/i-gao/model-equality-testing (not catalogued here).

## Limitations and open questions

Needs a reference model to sample from and repeated queries per prompt; [[white-2026-black]] found it weak (AUC 0.604) for covert conversational linking, and [[wang-2026-who]] found text-level tests degrade inside agent harnesses.

## Relevance to us

Gives a principled test for "do these two accounts sample from the same model distribution", the statistical core of model-level linking. Follow-ups: [[zhu-2025-auditing]], [[zhang-2026-which]], [[cai-2025-are]].
