---
id: barcis-2020-sandsbots
type: paper
title: "Sandsbots: Robots That Sync and Swarm"
authors: [Agata Barcis, Christian Bettstetter]
year: 2020
venue: IEEE Access
url: https://doi.org/10.1109/access.2020.3041393
doi: 10.1109/access.2020.3041393
arxiv: null
cite: "Barciś, A., & Bettstetter, C. (2020). Sandsbots: Robots that sync and swarm. IEEE Access, 8, 218752-218764."
topics: [sync-consensus, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "74 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Builds a multi-robot system that forms emergent space-time patterns using swarmalator ideas. The authors propose
a robot-suitable model: a time-discrete swarm aggregation model that works with low update rates and
communication delays, coupled through specific functions to a discrete temporal (phase) coordination model. The
approach is evaluated in simulation and demonstrated as a proof of concept on small wheeled robots and drones.

## Contribution

The first journal-length hardware implementation of swarmalators, following the same group's ROS 2 proof of
concept (Barciś, Barciś & Bettstetter, MRS 2019). It shows the continuous, all-to-all model of
[[okeeffe-2017-oscillators]] has to be discretised and made delay-tolerant before it runs on real robots.

## Key results

- Abstract-level: a discrete spatio-temporal coordination model that is robust to low update rates and delays;
  patterns demonstrated on robots and drones.
- According to [[sar-2026-interplay]] (Section 6.4), this work and the 2019 paper produced static phase waves on
  wheeled robots and swarmalator behaviour on Crazyflie quadcopters; [[quinn-2025-decentralised]] notes the
  Crazyflie demo used a base station for control rather than full decentralisation. Not verified in this paper's
  full text.

## Methods and models

Discrete-time swarmalator variant with aggregation and phase coupling functions; simulations plus small robots
and drones. The publisher page and open-access PDF could not be fetched from this machine (IEEE blocks
automated access); metadata and abstract read from the OpenAlex record.

## Limitations and open questions

Proof of concept only; scale of the robot experiments not checked. Later work by the same group studies
stochastic coupling, message loss and step-size choice (cited in [[sar-2026-interplay]]).

## Relevance to us

The reference implementation to copy if we put swarmalators on hardware. Read it with [[quinn-2025-decentralised]]
(decentralised Crazyflie variant) and [[beattie-2025-realizing]] (15-robot platform). Follow-up: open the full
text from a browser and extract the update-rate and delay numbers.
