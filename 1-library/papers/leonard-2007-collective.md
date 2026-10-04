---
id: leonard-2007-collective
type: paper
title: Collective Motion, Sensor Networks, and Ocean Sampling
authors: [Naomi Ehrich Leonard, Derek A. Paley, Francois Lekien, Rodolphe Sepulchre, David M. Fratantoni, Russ E. Davis]
year: 2007
venue: Proceedings of the IEEE
url: https://doi.org/10.1109/jproc.2006.887295
doi: 10.1109/jproc.2006.887295
arxiv: null
cite: "Leonard, N. E., Paley, D. A., Lekien, F., Sepulchre, R., Fratantoni, D. M., & Davis, R. E. (2007). Collective motion, sensor networks, and ocean sampling. Proceedings of the IEEE, 95(1), 48-74."
topics: [sync-consensus, swarm-robotics, collective-motion]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "962 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Designs mobile sensor networks for optimal data collection, motivated by adaptive ocean sampling with
autonomous underwater gliders. A performance metric defines the best data set as the one minimising the error of
a model estimate of the sampled field (an objective-analysis / mapping error); optimal paths for the sensor
fleet are derived from it. Feedback control laws, built on the oscillator-model collective-motion framework,
stably coordinate vehicles on structured tracks optimised over a few parameters, and robustness to a steady
background flow acting on slow vehicles is examined.

## Contribution

The flagship application paper of the Leonard-Sepulchre-Paley collective-motion programme: it links the
phase-oscillator steering laws ([[sepulchre-2007-stabilization]], [[sepulchre-2008-stabilization]]) to a concrete
sensing objective and a real fleet, in the same Proceedings of the IEEE special issue as
[[olfati-saber-2007-consensus]].

## Key results

- Abstract-level: optimal closed-loop solutions are computed in several low-dimensional cases; performance is
  robust to a steady flow field. Field-experiment numbers (Monterey Bay glider deployment) not read.

## Methods and models

Particle model of constant-speed steered vehicles with Kuramoto-style phase coupling; mapping-error (objective
analysis) metric for sampling quality; numerical optimisation of track parameters. Only the abstract was read
(OpenAlex record); IEEE full text not accessible from this machine.

## Limitations and open questions

- Not verified here: experimental details, how communication delays and surfacing intervals of gliders were
  handled (see Section VII of [[sepulchre-2008-stabilization]], which describes asynchronous, satellite-relayed
  communication in this application).

## Relevance to us

The clearest real-world case where synchronising phases of moving agents is the point (spreading sensors
evenly in time and space). A template for a hackathon "useful sync" demo: coordinate a drone or rover fleet to
sample a field, score it by mapping error, and compare controllers. Read with [[okeeffe-2017-oscillators]] and
[[sar-2026-interplay]].
