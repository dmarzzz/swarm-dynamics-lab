---
id: he-2025-learning
type: paper
title: Learning Extremely High Density Crowds as Active Matters
authors:
- Feixiang He
- Jiangbei Yue
- Jialin Zhu
- Armin Seyfried
- Dan Casas
- Julien Pettré
- He Wang
year: 2025
venue: 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)
url: https://arxiv.org/abs/2503.12168
doi: 10.1109/cvpr52734.2025.00059
arxiv: '2503.12168'
cite: He, F., Yue, J., Zhu, J., Seyfried, A., Casas, D., Pettré, J., & Wang, H. (2025). Learning Extremely High Density Crowds as Active Matters. 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 540–550. https://doi.org/10.1109/cvpr52734.2025.00059
topics:
- crowds-and-traffic
- active-matter
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 3 (Crossref, 2026-10-03)
code: []
---

## Summary

Learns the dynamics of extremely dense crowds from low-quality in-the-wild videos where individuals cannot be tracked. The crowd is modelled as "crowd material", an active-matter continuum of particles subject to stochastic forces, combined with neural networks into a neural stochastic differential equation. It outperforms adapted baselines in analysing and forecasting extremely high-density crowds and remains interpretable as a continuous-time physics model.

## Contribution

A physics-informed ML approach that carries the active-matter view of crowds ([[bain-2019-dynamic]], [[gu-2025-emergence]]) into computer vision.

## Key results

- Reported (abstract): better analysis and forecasting than adapted existing methods on high-density crowd videos.

## Methods and models

Neural SDE with an active-matter continuum prior; CVPR 2025, 540–550.

## Limitations and open questions

Abstract only; benchmark construction and metrics not checked.

## Relevance to us

Example of learning continuum swarm dynamics from video without individual tracking, relevant if we have only coarse observations of a swarm. Contrast with [[alahi-2016-social]].
