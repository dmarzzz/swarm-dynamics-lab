---
id: schilling-2021-vision
type: paper
title: "Vision-Based Drone Flocking in Outdoor Environments"
authors: ["Fabian Schilling", "Fabrizio Schiano", "Dario Floreano"]
year: 2021
venue: "IEEE Robotics and Automation Letters"
url: https://arxiv.org/abs/2012.01245
doi: "10.1109/lra.2021.3062298"
arxiv: "2012.01245"
cite: "Schilling, F., Schiano, F., & Floreano, D. (2021). Vision-Based Drone Flocking in Outdoor Environments. IEEE Robotics and Automation Letters, 6(2), 2954–2961."
topics: ["swarm-robotics", "collective-motion"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "102 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Most drone flocks share positions by radio, which saturates as the swarm grows. This letter removes both
communication and visual markers: each quadcopter carries four cameras for omnidirectional vision, a CNN
detects neighbouring drones and estimates range and bearing from their known size, a multi-target tracker
(Gaussian-mixture filter with egomotion compensation) estimates neighbours' relative positions and
velocities, and a Reynolds-style potential-field controller (separation, cohesion, migration) flies the
group. The detector is trained on images labelled automatically by background subtraction. Three real
quadcopters fly outdoor migration tasks without collisions.

## Contribution

The first outdoor demonstration of a drone flock that uses only onboard vision to perceive neighbours, with
no communication of state. It complements radio-based flocking ([[vasarhelyi-2018-optimized]]) and
predictive aerial swarms ([[soria-2021-predictive]]), and precedes purely visual flocking models such as
[[mezey-2025-purely]].

## Key results

- Measured: detector average precision (AP@0.5) of 98.9% on the hold-out set after 77 epochs; inference at
  512 x 384 pixels (batches of four, one per camera) runs at about 5 Hz onboard.
- Measured: in the circular migration flight (about 5 min) the agents stay collision-free with minimum
  inter-agent distance 1.37 m and mean distance 2.32 m; the paper reports 30 min of collision-free recordings
  in total.
- Controller settings: v_max = 0.5 m/s, gains k_sep = 7, k_coh = 1, k_mig = 1, equilibrium spacing about 2 m;
  bearing noise sigma = 3 degrees.
- Observed: false positives arise in line-like background regions but do not destabilise the flock.

## Methods and models

Quadcopters with four cameras (720 x 540 binned, 10 Hz, grayscale) and onboard inference.
RTK-GNSS used only for ground truth. Detection, then tracking with a linearised range-bearing observation
model, then potential-field flocking. Code, dataset and trained model: https://github.com/lis-epfl/vswarm.

## Limitations and open questions

Only three drones, slow speeds (0.5 m/s), and short flights; the authors call these "minimal validation
conditions". The approach still needs the known physical size of the drones for range estimation.
Scaling to dense flocks with occlusion is untested. Read: abstract, method overview, experiment results and
conclusions.

## Relevance to us

The real-robot reference for vision-only (topological, perception-limited) flocking, which links the
collective-motion models in the library to hardware. Sensor noise and 5 Hz perception are realistic
parameters to inject into a hackathon flocking simulation.
