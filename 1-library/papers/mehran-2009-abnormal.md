---
id: mehran-2009-abnormal
type: paper
title: "Abnormal crowd behavior detection using social force model"
authors: [Ramin Mehran, Alexis Oyama, Mubarak Shah]
year: 2009
venue: "2009 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)"
url: https://ieeexplore.ieee.org/document/5206641
doi: 10.1109/CVPR.2009.5206641
arxiv: null
cite: "Mehran, R., Oyama, A., & Shah, M. (2009). Abnormal crowd behavior detection using social force model. In 2009 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 935-942. https://doi.org/10.1109/CVPR.2009.5206641"
topics: [crowds-and-traffic, swarm-detection]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "1840 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Uses the pedestrian social force model as a feature extractor for anomaly detection in crowd video. A grid of particles is laid over each frame and advected by the space-time averaged optical flow; treating each particle as an individual, the interaction force is computed with the social force model and mapped back onto the image as a per-pixel "Force Flow". Randomly sampled spatio-temporal volumes of Force Flow from normal footage form a bag-of-words model of normal behaviour; frames are classified normal or abnormal, and anomalies are localised by where interaction force is high. Evaluated on the University of Minnesota (UMN) escape-panic dataset and a set of web crowd videos. Only the IEEE abstract was read (the author PDF link did not download from this host).

## Contribution

First widely cited use of a behavioural crowd model, rather than raw motion, as the representation for detecting abnormal collective behaviour; one of the most cited crowd-anomaly papers (about 1.8k citations).

## Key results

- Abstract claims the social force features capture crowd dynamics and outperform comparable approaches based on pure optical flow on the UMN panic and web datasets. Specific AUC numbers are in the paper and were not read.

## Methods and models

Optical flow, particle advection, social force interaction term ([[helbing-1995-social]]), bag-of-words over spatio-temporal Force Flow cuboids, normal-only training (one-class style), localisation by force magnitude.

## Limitations and open questions

Not assessed beyond the abstract. Known general weakness of this line: UMN panic scenes are staged and easy, so near-ceiling performance there says little about subtle anomalies. A YouTube presentation of this paper was in pipeline batch #29 (video 24-tLb8ITq0, uploader unknown, no transcript); the paper is catalogued instead.

## Relevance to us

A template for swarm detection: fit an interaction model of normal collective behaviour, then flag segments whose inferred interaction forces deviate. The same idea could apply to detecting coordinated agent swarms from traces, with the social force model replaced by an inferred interaction model of normal user activity. Crowd-disaster dynamics that such detectors try to catch: [[helbing-2000-simulating]], [[helbing-2007-dynamics]], [[moussaid-2011-simple]].
