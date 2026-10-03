---
id: waldmann-2024-3d
type: paper
title: "3D-MuPPET: 3D Multi-Pigeon Pose Estimation and Tracking"
authors: ["Urs Waldmann", "Alex Hoi Hang Chan", "Hemal Naik", "Máté Nagy", "Iain D. Couzin", "Oliver Deussen", "Bastian Goldluecke", "Fumihiro Kano"]
year: 2024
venue: "International Journal of Computer Vision"
url: https://api.crossref.org/works/10.1007/s11263-024-02074-y
doi: "10.1007/s11263-024-02074-y"
arxiv: null
cite: "Waldmann, U., Chan, A. H. H., Naik, H., Nagy, M., Couzin, I. D., Deussen, O., Goldluecke, B., & Kano, F. (2024). 3D-MuPPET: 3D Multi-Pigeon Pose Estimation and Tracking. International Journal of Computer Vision, 132(10), 4235-4252."
topics: [collective-motion, meta]
added_by: dmarz/collective-motion-recent
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 22  # (Crossref is-referenced-by-count, 2026-10-03; OpenAlex daily budget exhausted for this IP)
code: []
---
## Summary

A framework to estimate and track 3D poses of up to 10 pigeons from multiple camera views at interactive speed: a 2D keypoint and box estimator, triangulation to 3D, and identity matching across views (global IDs in the first frame, then a 2D tracker). Accuracy is comparable to a state-of-the-art 3D pose estimator (median error, PCK); speed up to 9.45 fps in 2D and 1.89 fps in 3D. A model trained on single pigeons works for up to 5, and the system works outdoors without extra annotation.

## Contribution

One of the first markerless 3D multi-animal posture trackers usable indoors and outdoors, enabling gaze- and posture-aware collective behaviour studies.

## Key results

- Measured (abstract): 9.45 fps (2D), 1.89 fps (3D); comparable accuracy to a 3D baseline; transfer from single-pigeon training to 5 birds.

## Methods and models

Multi-view deep pose estimation and tracking, trained on the 3D-POP dataset (not checked). Code: https://github.com/alexhang212/3D-MuPPET (seen in search results, not opened).

## Limitations and open questions

Abstract only; 10 individuals maximum, so not yet flock-scale.

## Relevance to us

Tooling for 3D data collection; for the code/dataset scans. Related 3D tracking: [[phurtivilai-2026-trackfish3d]], [[itoh-2024-fish]]; application: [[delacoux-2024-fine]].
