---
id: gh-jwkirchenbauer-lm-watermarking
type: code
title: "lm-watermarking: green-list watermark for LLM text and its detector (Kirchenbauer et al.)"
repo: jwkirchenbauer/lm-watermarking
url: https://github.com/jwkirchenbauer/lm-watermarking
authors: ["John Kirchenbauer", "Jonas Geiping", "Yuxin Wen", "Jonathan Katz", "Ian Miers", "Tom Goldstein"]
year: 2023
language: Python
license: "Apache-2.0"
stars: 700
last_commit: 2025-09-17
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 2
papers: []
---

## Summary

Official code for 'A Watermark for Large Language Models' (arXiv 2301.10226) and 'On the Reliability of Watermarks for Large Language Models' (arXiv 2306.04634, ICLR 2024). A WatermarkLogitsProcessor works with any Hugging Face generate model; the WatermarkDetector computes a z-score from the fraction of 'green-list' tokens, with homoglyph and normalisation handling.

## What it can do for us

Open baseline for key-based provenance, with a statistical test whose false-positive rate is explicit, unlike classifier detectors.

## Run notes

Not run.

## Limitations

Requires the generator to embed the watermark. The reliability paper studies removal by paraphrasing; not checked here in detail.
