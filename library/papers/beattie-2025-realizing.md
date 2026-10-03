---
id: beattie-2025-realizing
type: paper
title: Realizing Emergent Collective Behaviors Through Robotic Swarmalators
authors: [Richard Beattie, Steven Ceron, Daniela Rus]
year: 2025
venue: 2025 IEEE International Conference on Robotics and Automation (ICRA)
url: https://doi.org/10.1109/icra55743.2025.11128695
doi: 10.1109/icra55743.2025.11128695
arxiv: null
cite: "Beattie, R., Ceron, S., & Rus, D. (2025). Realizing emergent collective behaviors through robotic swarmalators. In 2025 IEEE International Conference on Robotics and Automation (ICRA) (pp. 3065-3071). IEEE."
topics: [sync-consensus, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "3 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Realises in a 15-robot collective many of the swarmalator behaviours previously seen only in simulation,
including chiral and non-chiral agents, frequency coupling, and homogeneous and heterogeneous natural-frequency
distributions (the model family of [[ceron-2023-diverse]]). The paper presents the platform as a testbed and
discusses differences between simulation and experiment.

## Contribution

The largest robot validation of the 2D swarmalator state zoo found in this scan; moves the [[ceron-2023-diverse]]
predictions from simulation to hardware. [[sar-2026-interplay]] identifies the robots as Sphero BOLT units.

## Key results

- Abstract-level: 15 robots reproduce many predicted states for chiral, non-chiral and frequency-coupled
  swarmalators; simulation-experiment differences are reported (details not read).

## Methods and models

15-robot experimental platform (Sphero BOLT per [[sar-2026-interplay]]); swarmalator control law from
[[ceron-2023-diverse]]. Full text not accessible here (IEEE); abstract from OpenAlex.

## Limitations and open questions

Small N (15) relative to the N = 300 to 1000 simulations; which states fail to appear on hardware is the key
question to read for.

## Relevance to us

Direct precedent for a hackathon hardware demo with off-the-shelf toy robots. Any "first robot demo of state X"
claim must check this paper first.
