---
id: graphite-2026-ai
type: blog
title: AI Now Writes as Many Online Articles as Humans
authors:
- Jose Luis Paredes
- Gregory Druck
- Bevin Benson
- Ethan Smith
year: 2026
url: https://graphite.io/five-percent/research/ai-now-writes-as-many-online-articles-as-humans-do
site: Graphite Five Percent
topics:
- swarm-detection
read_depth: full
relevance: 5
added_by: shadow/sol-g49
accessed: '2026-10-03'
---

## Summary

Graphite estimates article-level AI prevalence from a filtered Common Crawl sample and three commercial detectors. Its updated analysis supersedes a widely repeated 'more AI than human' headline and shows a roughly half-and-half plateau, not equivalent shares of reader exposure or autonomous authors.

## Key claims

- Research dated May 2026, covering publication January 2020 to March 2026. Primarily AI shares: Q1 2025 49.6%, Q4 2025 50.9%, Q1 2026 49.9%. Updated estimate averages 3.3 percentage points below its October 2025 single-detector report.
- Method: randomly selected 55.4k Common Crawl URLs, English, article schema, >=100 words, classified article/listicle and dated in the window. Average outputs of Pangram, Copyleaks and GPTZero after conversion to binary labels; GPTZero Mixed counts as primarily AI and Pangram AI-assisted can contribute to the threshold.
- FPR on 15.7k pre-ChatGPT articles: Pangram 1.844%, Copyleaks 1.836%, GPTZero 1.355%. False-negative tests use 2,000 generated articles per model from GPT-5, Gemini 3.1 Pro and Claude Opus 4.6. Report says average FNRs below 2%.
- Google Sheets source data are linked; redistribution licence not established. Counts do not weight actual views and do not independently identify operators.

## Evidence quality

Primary vendor study with explicit sampling and detector calibration. Pre-ChatGPT text is assumed human; generated benchmarks cannot cover every real-world editing strategy. Detector-defined prevalence is not direct ground truth.

## Relevance to us

Documents threshold and version sensitivity in prevalence estimates. Evaluate detector calibration and operator overlap, not just accuracy on one generator.
