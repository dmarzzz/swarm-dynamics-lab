---
id: guo-2017-calibration
type: paper
title: On Calibration of Modern Neural Networks
authors:
- Chuan Guo
- Geoff Pleiss
- Yu Sun
- Kilian Q. Weinberger
year: 2017
venue: ICML / PMLR 70
url: https://arxiv.org/abs/1706.04599
doi: null
arxiv: '1706.04599'
cite: Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger (2017). On Calibration
  of Modern Neural Networks. Proceedings of the 34th International Conference on Machine
  Learning, PMLR 70, 1321–1330.
read_depth: abstract
citations: null
code: []
topics:
- decision-models
- llm-agent-swarms
added_by: vishesh/codex-decision-models
accessed: '2026-10-04'
relevance: 5
---

## Summary

The authors distinguish classification accuracy from the reliability of predicted probabilities and evaluate post-processing calibration methods on image and text classifiers. Temperature scaling is an effective simple baseline in their evaluated settings.

## Contribution

Use Brier scores and reliability plots; do not treat a confidence number as an independently validated correctness probability.

## Key results

Published in ICML, PMLR 70, pages 1321–1330. No new benchmark numbers are reproduced here.

## Methods and models

See the source; this catalogue records an initial evidence screen, not a reproduction.

## Limitations and open questions

Abstract and publisher citation inspected. It neither evaluates Jev nor guarantees calibration under adaptive corruption or distribution shift.

## Relevance to us

Decision-model research area: researchers/vishesh/notes/decision-models/README.md.
