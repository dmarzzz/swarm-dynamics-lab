---
id: amala-arokia-nathan-2025-autonomous
type: paper
title: "An autonomous drone swarm for detecting and tracking anomalies among dense vegetation"
authors: ["Rakesh John Amala Arokia Nathan", "Sigrid Strand", "Daniel Mehrwald", "Dmitriy Shutin", "Oliver Bimber"]
year: 2025
venue: "Communications Engineering"
url: https://doi.org/10.1038/s44172-025-00546-8
doi: "10.1038/s44172-025-00546-8"
arxiv: null
cite: "Amala Arokia Nathan, R. J., Strand, S., Mehrwald, D., Shutin, D., & Bimber, O. (2025). An autonomous drone swarm for detecting and tracking anomalies among dense vegetation. Communications Engineering, 4(1), 205. https://doi.org/10.1038/s44172-025-00546-8"
topics: [swarm-robotics, swarm-intelligence]
added_by: dmarz/swarm-robotics-recent-audit
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "6 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex search budget exhausted during this audit)"
code: []
---

## Summary

Six drones act as one wide synthetic-aperture camera: integrating their images defocuses foliage so that heavily occluded targets in a forest become visible. Instead of class-based object detection, the system runs anomaly detection on the integral images and uses an adapted particle swarm optimisation (PSO) to move the drones, adapting the sampling pattern to local occlusion and viewing angle while tracking targets. Field experiments with DJI Mavic 3T drones track moving targets from sparse to dense vegetation.

## Contribution

A real-world case where a swarm algorithm (PSO) steers physical drones and where the swarm's spatial spread is the sensor, a different use of collectives from flocking. The paper claims the first fully autonomous drone swarm that detects and tracks general anomalous targets under dense, realistic occlusion.

## Key results

- Average positional accuracy 0.39 m, average precision 93.2% and average recall 95.9% (measured, field experiments).
- Processing time about 600 ms per PSO iteration for six drones, plus about 80 ms round-trip for waypoint upload and video/telemetry download.
- A confidence metric for ranking the most abnormal targets, and inclusion of sensor noise in the synthetic-aperture process, removing costly high-dimensional parameter optimisation (claimed).

## Methods and models

6 DJI Mavic 3T with RTK at 45-55 m above ground; centralised processing on a ground station (the "swarm" is centrally coordinated). PSO hyperparameters include exploration and exploitation radii of 1 m and 2 m and a 4.2 m minimum horizontal spacing. Code: https://github.com/JKU-ICG/AOS (from the code-availability statement; not opened). I skimmed the abstract, results and methods.

## Limitations and open questions

Centralised control and only six drones; the authors expect larger and faster swarms with better hardware. PSO here is an optimiser over drone positions, not a model of collective motion.

## Relevance to us

A rare real-world deployment of a swarm-intelligence algorithm on drones; useful as a counterpoint in swarm-intelligence (topic) discussions about whether such algorithms earn their place. Compare with emergent-flocking drones in [[verdoucq-2025-flocking]].
