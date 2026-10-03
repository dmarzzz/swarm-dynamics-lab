---
id: phurtivilai-2026-trackfish3d
type: paper
title: "TrackFish3D: Self-Supervised 3D Tracking of Schooling Fish from Multi-view Videos"
authors: ["Patt Phurtivilai", "Zhiyang Dou", "Yifan Wu", "Kinfung Chu", "Yuan Liu", "Lei Yang", "Wenping Wang", "Taku Komura"]
year: 2026
venue: "arXiv preprint (to appear at NeurIPS 2026)"
url: https://arxiv.org/abs/2609.38347
doi: null
arxiv: "2609.38347"
cite: "Phurtivilai, P., Dou, Z., Wu, Y., Chu, K., Liu, Y., Yang, L., Wang, W., & Komura, T. (2026). TrackFish3D: Self-Supervised 3D Tracking of Schooling Fish from Multi-view Videos. arXiv preprint arXiv:2609.38347. To be published at NeurIPS 2026."
topics: [collective-motion, meta]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null  # arXiv-only; OpenAlex budget exhausted and Semantic Scholar rate-limited on 2026-10-03
code: []
---
## Summary

Geometry-driven self-supervised multi-camera 3D tracking of schooling fish. Triangulation and reprojection consistency supply pseudo-associations; a geometric encoder and global association transformer learn cross-view correspondence; a contrastive objective separates co-visible individuals and a temporal predictor keeps identities through short occlusions. Trained once on unlabelled footage, it needs no identity labels, 3D ground truth or appearance features. 3D MOTA rises from 87.7% (best baseline) to 95.8% on the authors' benchmark and reaches 81.1% vs 77.4% on 3D-ZeF zebrafish; it also works on real bird tracking.

## Contribution

Removes the annotation bottleneck for 3D multi-animal tracking.

## Key results

- Measured (abstract): 3D MOTA 95.8% vs 87.7%; 81.1% vs 77.4% on 3D-ZeF.

## Methods and models

Multi-view geometry, transformer association, contrastive and temporal self-supervision.

## Limitations and open questions

Abstract only; group sizes and frame rates not checked.

## Relevance to us

Likely the strongest 3D fish tracker as of this scan; for the code and dataset scans. Same group: [[wu-2024-cbil]]. Compare [[waldmann-2024-3d]], [[itoh-2024-fish]], [[ko-2025-beyond]].
