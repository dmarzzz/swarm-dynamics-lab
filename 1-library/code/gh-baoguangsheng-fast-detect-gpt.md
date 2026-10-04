---
id: gh-baoguangsheng-fast-detect-gpt
type: code
title: "Fast-DetectGPT: zero-shot machine-text detection via conditional probability curvature"
repo: baoguangsheng/fast-detect-gpt
url: https://github.com/baoguangsheng/fast-detect-gpt
authors: ["baoguangsheng"]
year: 2023
language: Python
license: "MIT"
stars: 434
last_commit: 2026-02-07
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Code for 'Fast-DetectGPT: Efficient Zero-Shot Detection of Machine-Generated Text via Conditional Probability Curvature' (ICLR 2024, arXiv 2310.05130), extending DetectGPT. README table: AUROC 0.9887 versus DetectGPT 0.9554 on generations from five source models (white-box), and 0.9338 versus 0.7225 on ChatGPT and GPT-4 generations (black-box with surrogate models), with a 340x speedup measured on an A100. A January 2026 note says Llama3-8B and Llama3-8B-Instruct as sampling and scoring models substantially beat Falcon-7B, especially on text from reasoning models.

## What it can do for us

Cheap, well-benchmarked text signal; the hosted API (fastdetect.net) allows quick checks on scraped agent posts.

## Run notes

Not run.

## Limitations

Benchmarks are on curated corpora; robustness to paraphrase and adversarial edits is covered by [[gh-liamdugan-raid]], where detectors degrade.
