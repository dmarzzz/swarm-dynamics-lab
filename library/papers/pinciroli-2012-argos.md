---
id: pinciroli-2012-argos
type: paper
title: "ARGoS: a modular, parallel, multi-engine simulator for multi-robot systems"
authors: ["Carlo Pinciroli", "Vito Trianni", "Rehan O’Grady", "Giovanni Pini", "Arne Brutschy", "Manuele Brambilla", "Nithin Mathews", "Eliseo Ferrante", "Gianni Di Caro", "Frederick Ducatelle", "Mauro Birattari", "Luca Maria Gambardella", "Marco Dorigo"]
year: 2012
venue: "Swarm Intelligence"
url: http://bio.kuleuven.be/ento/ferrante/papers/2012_SwarmIntelligence_Argos.pdf
doi: "10.1007/s11721-012-0072-5"
arxiv: null
cite: "Pinciroli, C., Trianni, V., O’Grady, R., Pini, G., Brutschy, A., Brambilla, M., Mathews, N., Ferrante, E., Di Caro, G., Ducatelle, F., et al. (2012). ARGoS: a modular, parallel, multi-engine simulator for multi-robot systems. Swarm Intelligence, 6(4), 271–295."
topics: ["swarm-robotics", "meta"]
added_by: dmarz/swarm-robotics-audit
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "548 (OpenAlex, 2026-10-03)"
code: []
---
## Summary

ARGoS is a robot-swarm simulator designed to be fast with many robots and flexible for custom experiments at
the same time. Its two key design choices are partitioning the simulated space into regions, each run by a
different physics engine (2D kinematics, 2D dynamics, 3D dynamics) in parallel, and a multi-threaded
master/slave architecture that spreads sensing, control and actuation across CPU cores. Everything (robots,
sensors, actuators, engines, visualisations) is a plugin. Benchmarks show that run time grows linearly with the
number of robots, and a 2D-dynamics simulation of 10 000 e-pucks runs in 60% of real time.

## Contribution

The standard simulator for swarm-robotics research, with native e-puck, foot-bot and eye-bot models and later
Kilobot support. It is the platform behind much of the IRIDIA work in this library ([[francesca-2014-automode]],
[[ferrante-2012-self]], [[valentini-2016-collective]]) and the tool [[dorigo-2021-swarm]] singles out as the
best available.

## Key results

- Measured: wall-clock time scales linearly with the number of robots; threading hurts for N < 100 robots
  and helps for N > 100, with the best speedup at P = 16 threads.
- Measured: a 2D-dynamics simulation of 10 000 e-pucks runs at 60% of real time (abstract).
- Space partitions A1-A16 (up to 16 engines) further improve efficiency.
- A case study with six foot-bots shows how to add a custom dead-reckoning sensor model to match a real
  motor asymmetry (the foot-bot trajectory slants left at equal treel speeds).

## Methods and models

C++ core, discrete-time loop of sense, control and act phases dispatched to P slave threads by a master
thread. Physics engines are swappable per region of space; robots are composable entities (foot-bot, eye-bot,
e-puck). Benchmarks varied N, threads and partitions. Code: https://github.com/ilpincy/argos3 (not catalogued
here; flag for the code scan).

## Limitations and open questions

Skimmed (abstract, architecture, benchmark figure captions and case study). The benchmarks are from 2012
hardware. The physics fidelity of the dynamics engines for contact-rich robotic active matter (bristle-bots,
Hexbugs; [[baconnier-2022-selective]]) is not addressed. GPU-vectorised simulators for learning (e.g. VMAS)
are a newer alternative.

## Relevance to us

A ready simulator for any hackathon experiment on Kilobot- or e-puck-style swarms, and the reference to cite
for scalable swarm simulation. Compare with the custom flocking simulator of [[vasarhelyi-2018-optimized]]
(robotsim) for drone flocks.
