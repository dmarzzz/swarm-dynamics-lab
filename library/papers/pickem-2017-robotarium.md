---
id: pickem-2017-robotarium
type: paper
title: "The Robotarium: A remotely accessible swarm robotics research testbed"
authors: ["Daniel Pickem", "Paul Glotfelter", "Li Wang", "Mark Mote", "Aaron Ames", "Eric Feron", "Magnus Egerstedt"]
year: 2017
venue: "2017 IEEE International Conference on Robotics and Automation (ICRA)"
url: https://arxiv.org/abs/1609.04730
doi: "10.1109/icra.2017.7989200"
arxiv: "1609.04730"
cite: "Pickem, D., Glotfelter, P., Wang, L., Mote, M., Ames, A., Feron, E., & Egerstedt, M. (2017). The Robotarium: A remotely accessible swarm robotics research testbed. 2017 IEEE International Conference on Robotics and Automation (ICRA), 1699–1706."
topics: ["swarm-robotics", "sync-consensus"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "373 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

Describes the Robotarium at Georgia Tech, a multi-robot lab that anyone can use remotely by uploading control
code. Its small differential-drive GRITSBots (about USD 60 in parts) charge wirelessly on base stations. Safety comes from control barrier certificates: user commands are projected minimally into a convex
set of safe inputs, giving provably collision-free execution whatever code is uploaded. User code is first
scored for safety in simulation. Demos include coverage control (13 robots), hexagon formation (6),
attitude synchronisation (9) and position swapping (10).

## Contribution

Made remote, shared swarm hardware a research instrument, and made barrier-certificate safety filters a
standard layer for multi-robot experiments.

## Key results

- Measured: decentralised safety barrier certificates compute in under 10 ms even for 100 robots, while the
  centralised version scales badly (Table I).
- Testbed footprint 130 x 90 x 180 cm; GRITSBot about USD 60 to build or USD 100 preassembled.
- Demonstrations of formation control, coverage control and synchronisation algorithms, which usually assume
  single-integrator points, run on unicycle robots through a mapping plus the barrier layer.

## Methods and models

Control barrier functions define forward-invariant safe sets; a QP projects commands onto them.
Single-integrator to unicycle mapping. WiFi command links. Read: arXiv preprint (ICRA
version), architecture and safety sections.

## Limitations and open questions

The arena is small with tens of robots, and robots rely on a central testbed infrastructure, so it suits
consensus and formation control more than local-sensing swarm dynamics. The 2020 IEEE Control Systems
follow-up (Wilson et al.) reports usage statistics and was not catalogued.

## Relevance to us

A possible route to running a hackathon controller on real robots without owning any. Barrier certificates
are a useful safety layer for any collision-avoidance study (compare [[soria-2021-predictive]]).
