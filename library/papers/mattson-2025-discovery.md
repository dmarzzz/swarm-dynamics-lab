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
