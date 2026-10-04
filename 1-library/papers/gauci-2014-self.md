---
id: gauci-2014-self
type: paper
title: "Self-organized aggregation without computation"
authors: ["Melvin Gauci", "Jianing Chen", "Wei Li", "Tony J. Dodd", "Roderich Groß"]
year: 2014
venue: "The International Journal of Robotics Research"
url: https://eprints.staffs.ac.uk/6245/1/eprint6245.pdf
doi: "10.1177/0278364914525244"
arxiv: null
cite: "Gauci, M., Chen, J., Li, W., Dodd, T. J., & Groß, R. (2014). Self-organized aggregation without computation. The International Journal of Robotics Research, 33(8), 1145–1161."
topics: [swarm-robotics, active-matter]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "162 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Robots with no memory, no arithmetic and a single binary line-of-sight sensor (is another robot in front of me?)
can aggregate into one cluster. A grid search over all such reactive controllers finds the optimum: rotate on
the spot when a robot is seen, otherwise move backwards along a circular arc. The authors prove that the sensor
range must be long enough or aggregation cannot be guaranteed for any controller, and prove that the optimal
controller aggregates two moving robots in finite time with an upper bound.

## Contribution

A minimal, provable swarm behaviour: shows how far "computation-free" control can go, foreshadowing robotic
active matter where physics replaces computation ([[li-2021-programming]], [[ben-zion-2023-morphological]]).

## Key results

- Simulation: consistently aggregates at least 1000 robots into a single cluster.
- Measured: 30 experiments with 40 physical e-pucks, 98.6% of robots aggregated into one cluster.
- Proven: necessary sensor-range condition; finite-time aggregation for two robots.

## Methods and models

e-puck robots with a single binary line-of-sight sensor; grid search over all reactive controllers (wheel
commands for each sensor reading). Read the abstract and opening of the author PDF.

## Limitations and open questions

Proofs cover two robots; large-N behaviour is empirical. Sensitive to sensor range and arena geometry.

## Relevance to us

A perfect minimal model to simulate and analyse as a dynamical system; the controller has 4 numbers.
Follow-up: consensus without computation (Gauci et al. 2018, not catalogued).
