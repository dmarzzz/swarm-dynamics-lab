---
id: stern-2018-dissipation
type: paper
title: 'Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments'
authors:
- Raphael E. Stern
- Shumo Cui
- Maria Laura Delle Monache
- Rahul Bhadani
- Matt Bunting
- Miles Churchill
- Nathaniel Hamilton
- R’mani Haulcy
- Hannah Pohlmann
- Fangyu Wu
- Benedetto Piccoli
- Benjamin Seibold
- Jonathan Sprinkle
- Daniel B. Work
year: 2018
venue: 'Transportation Research Part C: Emerging Technologies'
url: https://arxiv.org/abs/1705.01693
doi: 10.1016/j.trc.2018.02.005
arxiv: '1705.01693'
cite: 'Stern, R. E., Cui, S., Delle Monache, M. L., Bhadani, R., Bunting, M., Churchill, M., Hamilton, N., Haulcy, R., Pohlmann, H., Wu, F., et al. (2018). Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments. Transportation Research Part C: Emerging Technologies, 89, 205–221. https://doi.org/10.1016/j.trc.2018.02.005'
topics:
- crowds-and-traffic
- sync-consensus
- swarm-robotics
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 746 (Crossref, 2026-10-03)
code: []
---

## Summary

Replicates the Sugiyama ring-road experiment in Arizona with 21–22 instrumented cars on a 260 m track and shows that a single automated vehicle, running a simple velocity controller, dissipates the human-generated stop-and-go wave. Three experiments compare an automated "FollowerStopper" tracking a set speed, a trained human driver doing the same by hand, and a fully local proportional-integral controller with saturation that estimates the average speed from its own history.

## Contribution

First field demonstration that Lagrangian control by a very small fraction of vehicles (about 5%) can stabilise collective traffic dynamics, shifting traffic control from fixed infrastructure (ramp metering, variable speed limits) to mobile actuators embedded in the flow. It is the experimental anchor for the mixed-autonomy research programme that followed (deep RL in [[wu-2022-flow]], the 100-car CIRCLES deployment in [[lee-2025-traffic]] and [[jang-2025-reinforcement]]).

## Key results

All numbers are measured, comparing the first wave interval (human control) with the best controlled interval (table 3):
- Experiment A (21 cars, FollowerStopper, best set point U = 7.5 m/s): velocity s.d. −80.8%, fuel consumption −42.5% (lowest 14.13 l/100 km), excessive braking from 8.58 to 0.12 events/vehicle/km (−98.6%), throughput +14.1%. Raising U to 8.0 m/s (faster than the traffic average) re-created the wave.
- Experiment B (21 cars, trained human following the same rule): velocity s.d. −49.5%, fuel −22.1%, braking −76.2%, throughput +9.8% (2008 vs 1828 veh/h).
- Experiment C (22 cars, PI with saturation, no external input): velocity s.d. −54.7%, fuel −28.1%, braking −74.4%, throughput −2.5%; a second wave appeared during control and was also damped.
- Waves appeared in every run without bottlenecks, 55–161 s after start.

## Methods and models

Track radius 41.4 m (260 m circumference); one University of Arizona CAT Vehicle with longitudinal control and a human steering; others are employees instructed to drive normally, close gaps, not tailgate. 360-degree camera at centre plus OBD-II loggers for speed and fuel. FollowerStopper: piecewise command v_cmd between 0 and U depending on gap Δx and closing speed relative to quadratic boundaries Δx_k = Δx_k^0 + (Δv_−)^2/(2 d_k). PI with saturation: U is the running average of the AV's own speed, target speed rises by up to v_catch = 1 m/s for gaps between g_l = 7 m and g_u = 30 m, and v_cmd is a gap-dependent weighted average of previous command, target and lead speed. Low-level multi-mode PID (separate throttle and brake controllers, 20 Hz). Metrics: velocity s.d., fuel (l/100 km), braking-event rate with a data-defined threshold, throughput q = (n/L) v̄. Data and plotting code: https://uofi.box.com/v/trajectoryPaperData (as cited by the paper, not checked).

## Limitations and open questions

- Single-lane ring; the authors note multi-lane freeways add lane changes that can both trigger waves and fill the gaps controllers open. Only three experiments, one run each; no replication statistics.
- FollowerStopper needs an externally supplied set speed; the fully local controller left a smaller benefit and slightly reduced throughput.
- Human drivers knew an AV was present and were told not to smooth waves themselves; behavioural adaptation over longer horizons is untested.

## Relevance to us

The clearest evidence that a sparse set of controlled agents can stabilise an unstable human swarm: a direct template for "leader" or "shepherd" agents in swarm control and for testing whether a learned policy beats a two-line hand controller. Measured baselines (−40% fuel, −80% speed variance) give us concrete numbers to beat in simulation. Builds on [[sugiyama-2008-traffic]]; scaled up in [[lee-2025-traffic]]; RL framing in [[wu-2022-flow]]. Related consensus and string-stability control: [[olfati-saber-2007-consensus]].
