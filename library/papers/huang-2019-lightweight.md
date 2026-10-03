---
id: huang-2019-lightweight
type: paper
title: "Lightweight Sybil-Resilient Multi-Robot Networks by Multipath Manipulation"
authors: ["Yong Huang", "Wei Wang", "Yiyuan Wang", "Tao Jiang", "Qian Zhang"]
year: 2019
venue: "arXiv preprint (IEEE INFOCOM 2020)"
url: https://arxiv.org/abs/1912.04613
doi: null
arxiv: "1912.04613"
cite: "Huang, Y., Wang, W., Wang, Y., Jiang, T., & Zhang, Q. (2019). Lightweight Sybil-Resilient Multi-Robot Networks by Multipath Manipulation. arXiv:1912.04613."
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "9 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

ScatterID attaches batteryless backscatter tags to single-antenna robots so the receiver actively creates rich multipath features instead of passively observing them with a bulky antenna array. The resulting profile identifies the true signal source even for mobile, power-scaling attackers. Implemented on iRobot Create in indoor and outdoor environments, reaching AUROC 0.988 and 96.4% identity-verification accuracy.

## Contribution

Makes physical-layer Sybil detection cheap enough for miniature robots; an extended version (arXiv:2012.14227, IEEE/ACM ToN) adds colluding and power-scaling attackers and a random forest classifier with AUROC 0.987, 96.1% fake robots detected and 5.7% legitimate rejected.

## Key results

- AUROC 0.988, accuracy 96.4% for identity verification (abstract, conference version).
- Extended version: 96.1% detection, 5.7% false rejection under basic and advanced Sybil attacks (abstract of arXiv:2012.14227).

## Methods and models

Backscatter-tag multipath manipulation, similarity vectors, classifier. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Still detects one-radio-many-identities, not many colluding physical robots.

## Relevance to us

Shows the physical identity route can be made lightweight; the analogue for software agents is a cheap but unforgeable per-instance signal. Builds on [[gil-2015-guaranteeing]]; cites [[xiao-2009-channel]] lineage.

## Notes from dmarz/sybil-foundations

Skimmed the arXiv PDF (abstract, introduction, conclusion) on 2026-10-03. The paper appeared at IEEE INFOCOM 2020, pp. 2185-2193, doi 10.1109/infocom41043.2020.9155244 (Crossref). Reported numbers on iRobot Create platforms, indoor and outdoor: AUROC 0.988, identity-verification accuracy 96.4%, 97.6% of fake robots detected with 5.1% of legitimate robots wrongly rejected (conclusion). Lineage back to the sensor-network radio resource test of [[newsome-2004-sybil]].
