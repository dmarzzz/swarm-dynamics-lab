---
id: mattson-2025-discovery
type: paper
title: "Discovery and Deployment of Emergent Robot Swarm Behaviors via Representation Learning and Real2Sim2Real Transfer"
authors: ["Connor Mattson", "Varun Raveendra", "Ricardo Vega", "Cameron Nowzari", "Daniel S. Drew", "Daniel S. Brown"]
year: 2025
venue: "AAMAS 2025 (24th International Conference on Autonomous Agents and Multiagent Systems)"
url: https://arxiv.org/abs/2502.15937
doi: null
arxiv: "2502.15937"
cite: "Mattson, C., Raveendra, V., Vega, R., Nowzari, C., Drew, D. S., & Brown, D. S. (2025). Discovery and Deployment of Emergent Robot Swarm Behaviors via Representation Learning and Real2Sim2Real Transfer. In Proceedings of the 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2025). arXiv:2502.15937."
topics: [swarm-robotics, marl-emergence, criticality-measurement]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---
## Summary

Asks how to automatically discover the set of emergent behaviours a swarm of limited robots can produce. Prior
behaviour discovery relied on human feedback or hand-crafted behaviour metrics and stayed in simulation. The
authors combine self-supervised representation learning with novelty search to explore behaviour space in
simulation, show the learned representation captures the space of emergent behaviours better than hand-crafted
metrics, and use sim2real techniques in a lightweight simulator so discovered behaviours deploy directly on an
open-source, low-cost robot platform.

## Contribution

Turns "what can this swarm do?" into an automated search with a learned behaviour metric, and closes the loop to
hardware.

## Key results

- Learned representation beats hand-crafted metrics at representing behaviour space (simulation); discovered
  behaviours deployed on real robots (from abstract).

## Methods and models

Self-supervised embeddings of swarm trajectories, novelty search over controller parameters, Real2Sim2Real
transfer. Abstract read on arXiv.

## Limitations and open questions

Preprint; scope of behaviours limited to the controller family searched.

## Relevance to us

Directly useful methodology for a hackathon: automatic exploration of a swarm model's behaviour space with a
learned behaviour descriptor. Pairs with criticality/measurement work on order parameters.

## Notes from dmarz/swarm-robotics-audit

The arXiv record says the paper is in the AAMAS 2025 proceedings. Updated venue and cite. No proceedings DOI found (DBLP blocked automated access).

## Notes from dmarz/swarm-robotics-recent

I read the arXiv v1 HTML in full (2026-10-03). Crossref has a proceedings DOI: 10.65109/qczn2589 (AAMAS 2025, pp. 1473-1482; 2 Crossref citations on 2026-10-03). Key numbers:

- Capability model: 8 differential-drive HeRo+ robots (about USD 80 each, open-source) with one binary line-of-sight sensor (VL53L1X time-of-flight, about 2 m range), in a 170 x 142 cm arena. The controller is a 4-tuple $(v_0,\omega_0,v_1,\omega_1)$ chosen by the sensor bit, the computation-free model of Gauci et al. Simulation is capped at 9 cm/s and 1.6 rad/s, where real sensing is reliable.
- Representation: SimCLR (ResNet18, 512-d embedding) trained on 6,000 random-controller videos (3 greyscale 64x64 frames from the last 300 of 600 steps), with no labels. Novelty search: population 50, 100 generations, k=15 nearest neighbours, crossover 0.7, mutation 0.15; then k-medoids with k=10.
- Representation quality (measured on 500 labelled held-out videos): versus the 5 hand-crafted Brown et al. (2018) metrics, triplet accuracy is +16% for cyclic pursuit, +0% for aggregation and +5% for dispersal. The hand-crafted metrics confuse dispersal with random behaviour 27% of the time. The learned model never found milling or wall-following in the RSRS simulator.
- Deployment (measured): of 30 non-random discovered controllers, 70% (20) reproduced on real robots on the first attempt and 90% (27) within 3 attempts, without controller tuning. Without Real2Sim2Real calibration (friction, sensing-limited speeds, bump shields), only 22% (4/18) reproduced first time and 27% (5/18) within 3. Milling and wall-following found in the uncalibrated simulator were simulator artefacts that depend on frictionless sliding.
- Takeaway for us: behaviour discovery is cheap, but the simulator's contact model decides which 'emergent behaviours' are real. Related: [[vega-2025-analytical]] (phase diagrams for the same capability model), [[jesus-2026-how]] (behaviour similarity metrics), [[kim-2025-commanding]] (inverse design of interaction rules).
