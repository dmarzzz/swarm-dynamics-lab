---
id: dugan-2024-raid
type: paper
title: 'RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors'
authors:
- Liam Dugan
- Alyssa Hwang
- Filip Trhlik
- Josh Magnus Ludan
- Andrew Zhu
- Hainiu Xu
- Daphne Ippolito
- Chris Callison-Burch
year: 2024
venue: ACL 2024
url: https://arxiv.org/abs/2405.07940
doi: null
arxiv: '2405.07940'
cite: 'Dugan, L., Hwang, A., Trhlik, F., Ludan, J. M., Zhu, A., Xu, H., Ippolito, D., & Callison-Burch, C. (2024). RAID: A Shared Benchmark for Robust Evaluation of Machine-Generated Text Detectors. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024). arXiv:2405.07940.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 225 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

RAID is a benchmark of over 6 million generations from 11 models across 8 domains, 11 adversarial attacks and 4 decoding strategies. Evaluating 8 open and 4 closed detectors, it finds they are easily fooled by adversarial attacks, sampling variations, repetition penalties and unseen generators, despite claims of 99% accuracy.

## Contribution

The standard robustness benchmark for machine-generated text detectors, with a leaderboard.

## Key results

- Measured (abstract): current detectors easily fooled by adversarial attacks, decoding changes, repetition penalties and unseen models.

## Methods and models

Large generated corpus with controlled attacks and decoding; detector evaluation. Abstract read only.

## Limitations and open questions

Lab-generated text, not in-the-wild. Abstract depth.

## Relevance to us

Benchmark to use if the hackathon builds any content-level component; it quantifies how cheaply a swarm operator can defeat item-level detection.
