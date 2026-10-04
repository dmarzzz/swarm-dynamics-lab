---
id: hu-2026-jevadvbench
type: paper
title: 'JevAdvBench: A Benchmark and Black-Box Attacks for Reinforcement Learning
  for Calibrated Decisions Models'
authors:
- Jianyi Hu
- Hangtao Zhang
- Yi Liu
- Yeqi Zeng
- Li Zeng
- Xianlong Wang
- Rui Wang
- Leo Yu Zhang
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.31142
doi: null
arxiv: '2609.31142'
cite: 'Jianyi Hu, Hangtao Zhang, Yi Liu, Yeqi Zeng, Li Zeng, Xianlong Wang, Rui Wang,
  Leo Yu Zhang (2026). JevAdvBench: A Benchmark and Black-Box Attacks for Reinforcement
  Learning for Calibrated Decisions Models. arXiv:2609.31142.'
read_depth: abstract
citations: null
code:
- gh-jevadvbench-jevadvbench
topics:
- decision-models
- llm-agent-swarms
added_by: vishesh/codex-decision-models
accessed: '2026-10-04'
relevance: 5
---

## Summary

A single-model adversarial benchmark compares typed decisions before and after controlled request edits, with identical reruns establishing a noise floor. Appended opinions can change valid decisions and increase review demand. Most labels are model-derived, so a flip is not necessarily a newly wrong answer.

## Contribution

Use as closest prior for collective propagation and finite-review-capacity extensions, not as evidence that merely fooling Jev is novel.

## Key results

812 questions; 66 scenarios; 9,744 variants. The reported opinion-append flip rate is 12.1%. No independent replication was performed here.

## Methods and models

See the source; this catalogue records an initial evidence screen, not a reproduction.

## Limitations and open questions

Read abstract, introduction, threat-model framing and selected limitations; not full methods. Single-version, mostly self-labelled, single-edit results do not establish multi-round swarm effects.

## Relevance to us

Decision-model research area: 5-experiments/studies/vishesh/decision-models/README.md.
