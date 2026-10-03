---
id: sadasivan-2023-can
type: paper
title: Can AI-Generated Text be Reliably Detected?
authors:
- Vinu Sankar Sadasivan
- Aounon Kumar
- Sriram Balasubramanian
- Wenxiao Wang
- Soheil Feizi
year: 2023
venue: Transactions on Machine Learning Research (per arXiv comments)
url: https://arxiv.org/abs/2303.11156
doi: null
arxiv: '2303.11156'
cite: Sadasivan, V. S., Kumar, A., Balasubramanian, S., Wang, W., & Feizi, S. (2023). Can AI-Generated Text be Reliably Detected?. Transactions on Machine Learning Research. arXiv:2303.11156.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 660 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Stress-tests AI-text detectors (watermarking, trained classifiers, zero-shot and retrieval-based) with a recursive paraphrasing attack on passages of about 300 tokens, which sharply cuts detection rates with only slight quality loss in many cases. Shows watermarks can be spoofed so human text is labelled as AI, and gives a theoretical bound tying the best possible detector's AUROC to the total variation distance between human and AI text distributions.

## Contribution

The canonical impossibility-leaning result for per-item detection: as model and human distributions converge, any detector's ceiling falls.

## Key results

- Measured (abstract): recursive paraphrasing significantly reduces detection rates across detector families with modest quality loss.
- Shown (abstract): spoofing attacks on watermarks without white-box access.
- Theory (abstract): best-detector AUROC bounded by a function of total variation distance between human and AI distributions.

## Methods and models

Recursive paraphrasing attack; evaluation across detector families; TV-distance bound. Code: github.com/vinusankars/Reliability-of-AI-text-detectors. Abstract read only.

## Limitations and open questions

Bound is per sample; [[chakraborty-2023-possibilities]] argues that many samples restore detectability, which is the population-level escape. Abstract depth.

## Relevance to us

Main reason to work at population or account level rather than per post: per-item detection has a theoretical ceiling and practical evasions ([[krishna-2023-paraphrasing]]), while aggregating many samples from one source ([[chen-2024-online]], [[he-2026-degentweb]]) or one corpus ([[liang-2024-monitoring]]) does not hit the same wall.
