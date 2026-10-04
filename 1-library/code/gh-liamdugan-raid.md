---
id: gh-liamdugan-raid
type: code
title: "RAID: 10M-document benchmark and leaderboard for robustness of AI-generated text detectors"
repo: liamdugan/raid
url: https://github.com/liamdugan/raid
authors: ["liamdugan"]
year: 2024
language: Python
license: "MIT"
stars: 217
last_commit: 2026-10-02
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Code and pip package (`raid-bench`) for 'RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors' (ACL 2024, arXiv 2405.07940). Over 10 million generations from 11 models (ChatGPT, GPT-4, GPT-3, GPT-2 XL, Llama 2 70B Chat, Cohere, MPT-30B, Mistral 7B and chat variants), 11 domains, 4 decoding strategies and 11 adversarial attacks (paraphrase, homoglyph, synonym swap, zero-width space and others). Train split 11.8 GB with attacks. The README says current detectors are easily fooled by adversarial attacks, sampling changes and unseen generators; a COLING 2025 shared task (arXiv 2501.08913) used it.

## What it can do for us

The reference stress test: any claim that we can spot agent-written text should be checked against RAID's attacked splits. Its finding that detectors break under simple attacks is a negative result for content-based swarm detection.

## Run notes

Not run (dataset download is gigabytes).

## Limitations

Models in the benchmark are 2023-era; today's agents use newer models. Document-level, not account- or swarm-level.
