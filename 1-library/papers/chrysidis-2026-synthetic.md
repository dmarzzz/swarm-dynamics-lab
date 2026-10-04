---
id: chrysidis-2026-synthetic
type: paper
title: 'The Synthetic Media Shift: Tracking the Rise, Virality, and Detectability of AI-Generated Multimodal Misinformation'
authors:
- Zacharias Chrysidis
- Stefanos-Iordanis Papadopoulos
- Symeon Papadopoulos
year: 2026
venue: CVPR 2026 Workshops (per arXiv journal reference)
url: https://arxiv.org/abs/2604.15372
doi: null
arxiv: '2604.15372'
cite: 'Chrysidis, Z., Papadopoulos, S.-I., & Papadopoulos, S. (2026). The Synthetic Media Shift: Tracking the Rise, Virality, and Detectability of AI-Generated Multimodal Misinformation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops. arXiv:2604.15372.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 1 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Builds CONVEX, over 150K multimodal posts with Community Notes and engagement data from X, covering miscaptioned, edited and AI-generated visuals. AI-generated content achieves disproportionate virality, driven mostly by passive engagement; it is reported more slowly but reaches note consensus faster once flagged. Specialised detectors and vision-language models lose accuracy over time at telling synthetic from authentic images as generators evolve.

## Contribution

A longitudinal measurement of detector decay in the wild for synthetic images, alongside spread dynamics.

## Key results

- Measured (abstract): disproportionate virality of AI-generated visual misinformation, mostly passive engagement.
- Measured (abstract): consistent decline over time in detector and VLM accuracy on synthetic vs authentic images.

## Methods and models

Community Notes-derived dataset; engagement and consensus dynamics; detector evaluation over time. Abstract read only.

## Limitations and open questions

Restricted to noted posts. Abstract depth.

## Relevance to us

Direct evidence of the detector-decay problem for content-level detection, which is why swarm detection cannot lean on media classifiers alone. See [[drolsbach-2025-characterizing]].
