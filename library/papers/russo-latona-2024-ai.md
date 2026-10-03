---
id: russo-latona-2024-ai
type: paper
title: 'The AI Review Lottery: Widespread AI-Assisted Peer Reviews Boost Paper Scores and Acceptance Rates'
authors:
- Giuseppe Russo Latona
- Manoel Horta Ribeiro
- Tim R. Davidson
- Veniamin Veselovsky
- Robert West
year: 2024
venue: Proceedings of the ACM on Human-Computer Interaction 9 (2025)
url: https://arxiv.org/abs/2405.02150
doi: 10.1145/3757667
arxiv: '2405.02150'
cite: 'Latona, G. R., Ribeiro, M. H., Davidson, T. R., Veselovsky, V., & West, R. (2024). The AI Review Lottery: Widespread AI-Assisted Peer Reviews Boost Paper Scores and Acceptance Rates. Proceedings of the ACM on Human-Computer Interaction, 9, 1-28. https://doi.org/10.1145/3757667. arXiv:2405.02150.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 109 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Quasi-experimental study of ICLR 2024 peer reviews. GPTZero gives a lower bound of 15.8% of reviews written with AI assistance. In pairs of reviews of the same paper with different scores, the AI-assisted review scores higher 53.4% of the time, and borderline papers that received an AI-assisted review were 4.9 percentage points more likely to be accepted.

## Contribution

Moves from prevalence to consequence: per-item detector flags, used as a lower bound, linked to measurable effects on outcomes.

## Key results

- Measured (abstract): at least 15.8% of ICLR 2024 reviews AI-assisted (GPTZero).
- Measured (abstract): AI-assisted review scores higher in 53.4% of discordant pairs (p = 0.002).
- Measured (abstract): +4.9 percentage points acceptance for near-threshold papers with an AI-assisted review (p = 0.024).

## Methods and models

GPTZero detection on OpenReview data; paired comparisons within papers; matched study near the acceptance threshold. Abstract read only.

## Limitations and open questions

Commercial detector with undisclosed internals; lower-bound framing depends on its false-positive rate. Abstract depth.

## Relevance to us

Independent estimate for the same corpus as [[liang-2024-monitoring]] (about 10.6% of sentences vs at least 15.8% of reviews), showing how unit of analysis changes the number.
