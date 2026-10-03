---
id: rubenstein-2012-kilobot
type: paper
title: "Kilobot: A low cost scalable robot system for collective behaviors"
authors: ["Michael Rubenstein", "Christian Ahler", "Radhika Nagpal"]
year: 2012
venue: "2012 IEEE International Conference on Robotics and Automation (ICRA)"
url: https://doi.org/10.1109/icra.2012.6224638
doi: "10.1109/icra.2012.6224638"
arxiv: null
cite: "Rubenstein, M., Ahler, C., & Nagpal, R. (2012). Kilobot: A low cost scalable robot system for collective behaviors. 2012 IEEE International Conference on Robotics and Automation, 3293–3298."
topics: [swarm-robotics]
added_by: dmarz/swarm-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "681 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Introduces the Kilobot, a low-cost robot designed so that collective algorithms meant for hundreds or
thousands of robots can be tested in hardware rather than only in simulation or on a few tens of robots. Each
robot uses about US$14 of parts and takes about 5 minutes to assemble, and the design lets a single user
program, power on and charge a whole collective at once. Locomotion is by two vibration motors on three rigid
legs; communication and distance sensing use infrared reflected off the table.

## Contribution

The hardware enabler behind [[rubenstein-2014-programmable]] and a large share of experimental swarm studies
(collective decision-making with 100 robots, morphogenesis [[slavkov-2018-morphogenesis]], Morphobots
[[ben-zion-2023-morphological]]).

## Key results

- Reported: about $14 parts cost, about 5 min assembly per robot; collective-scale operation (programming,
  charging) by one user.
- Per [[ben-zion-2023-morphological]] (measured there): bare Kilobot speed about 0.53 cm/s after calibration,
  IR range about 7 cm.

## Methods and models

Hardware design paper; abstract read. A journal version appeared in Robotics and Autonomous Systems (2014).

## Limitations and open questions

Very slow, imprecise motion requiring per-robot calibration; short communication range; these constrain which
dynamics can be studied.

## Relevance to us

The default physical platform for large-N swarm dynamics; its limits (slow, noisy, short range) should inform
what a simulation should model if we want results that transfer.
