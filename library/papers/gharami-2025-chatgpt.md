---
id: gharami-2025-chatgpt
type: paper
title: 'ChatGPT: Excellent Paper! Accept It. Editor: Imposter Found! Review Rejected'
authors:
- Kanchon Gharami
- Sanjiv Kumar Sarkar
- Safayat Bin Hakim
- Yongxin Liu
- Nahid Farhady Ghalaty
- Shafika Showkat Moni
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2512.20405
doi: null
arxiv: '2512.20405'
cite: 'Gharami, K., Sarkar, S. K., Hakim, S. B., Liu, Y., Ghalaty, N. F., & Moni, S. S. (2025). ChatGPT: Excellent Paper! Accept It. Editor: Imposter Found! Review Rejected. arXiv preprint arXiv:2512.20405.'
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

Shows both sides of hidden prompts in PDFs. Attack: authors inject prompts that push LLM reviewers to overly positive reviews. Defence: an 'inject-and-detect' strategy in which editors embed invisible trigger prompts in papers, so a review that repeats or reacts to the trigger reveals that it was LLM-generated. The paper outlines the design, expected model behaviours and ethical safeguards.

## Contribution

A design proposal for editor-side canaries; less rigorous than [[rao-2025-detecting]], which provides the statistics.

## Key results

- Proposal and expected behaviours; the abstract reports no measured detection rates.

## Methods and models

Design and demonstration. Abstract-level read.

## Limitations and open questions

Abstract only; no statistical error control described in the abstract.

## Relevance to us

Second independent proposal of the same inject-and-detect canary, which suggests the idea is converging. Related: [[lin-2025-hidden]], [[collu-2025-misleading]].
