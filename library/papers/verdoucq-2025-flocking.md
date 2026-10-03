---
id: verdoucq-2025-flocking
type: paper
title: "Flocking phase transition and threat responses in bio-inspired autonomous drone swarms"
authors: ["Matthieu Verdoucq", "Dari Trendafilov", "Clément Sire", "Ramón Escobedo", "Guy Theraulaz", "Gautier Hattenberger"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/html/2512.21196
doi: null
arxiv: "2512.21196"
cite: "Verdoucq, M., Trendafilov, D., Sire, C., Escobedo, R., Theraulaz, G., & Hattenberger, G. (2025). Flocking phase transition and threat responses in bio-inspired autonomous drone swarms. arXiv preprint arXiv:2512.21196."
topics: [swarm-robotics, collective-motion, criticality-measurement]
added_by: dmarz/swarm-robotics-recent
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "0 (OpenAlex W7117298302, 2026-10-03); 0 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Ten outdoor quadrotors (modified Parrot Bebop 2 with RTK GPS) run a 3-D version of the Toulouse fish-school "burst-and-coast" interaction model. Each drone reacts only to its two most influential neighbours, through an alignment gain and an attraction gain acting on its heading. Sweeping the two gains maps a phase diagram with a disordered but cohesive "swarming" phase, a polarised "schooling" phase, and a critical line between them where polarisation fluctuations (susceptibility) peak. Field flights reproduce the transition along an alignment transect. An approaching intruder drone triggers collective turns, vertical splitting and expansion. Near the critical region the swarm reorganises most and recovers fastest, within about 5-6 s.

## Contribution

This is, as far as I know, the first outdoor aerial-swarm study to frame interaction-gain tuning explicitly as moving through a flocking phase transition and to measure susceptibility and threat response on both sides of it. It transfers the "criticality maximises responsiveness" argument from fish data and models (Calovi/Theraulaz line) to physical drones, complementing [[vasarhelyi-2018-optimized]] (which optimised flocking performance rather than mapping phases) and earlier robot criticality work on alignment-driven order-disorder transitions.

## Key results

- Simulation phase diagram (measured, 10 runs per grid point, alignment gain in [0, 0.4] and attraction gain in [0.2, 0.8]): a sharp swarming-to-schooling transition with maximal polarisation variance along the critical line. Doubling group size doubles the slope of the critical line and shifts the fluctuation peak and the polarisation saturation two-fold, so larger swarms need about twice the alignment gain for the same order. Fluctuation peaks sharpen with N, a finite-size signature.
- Field vs simulation (measured): the empirical critical region along the transect is shifted relative to simulation. The authors attribute this to the first-order drone response model, 1 Hz telemetry with 2 Hz control, communication latency and 18-22 km/h wind with 33 km/h gusts. Intruder-induced polarisation drops are present but weaker in the field.
- Switching asymmetry (measured, repeated 60 s gain switches with 10 drones): swarming to schooling takes about 5 s, schooling to swarming about 15 s, a three-fold asymmetry consistent across trials. The authors interpret it as ordered states being forced quickly while disorder only accumulates gradually.
- Intruder response (measured in field, 200 simulation repetitions per condition): swarming responds mainly by spatial expansion (about 2x the dispersion change of schooling), schooling mainly by changing collective velocity and direction. The critical regime does both: strong opening plus a velocity response about 1.5x that of swarming, the largest polarisation fluctuations, and the fastest recovery. Minimal inter-agent distance peaks in the critical region and drops sharply when the intruder passes.
- Data are on Zenodo: https://doi.org/10.5281/zenodo.17902132.

## Methods and models

- Agent update at a fixed rate: changes in horizontal speed, climb rate and course are sums of social terms, navigation terms (altitude hold at 10 m) and intruder-avoidance terms. Social alignment and attraction act on course, are functions of relative bearing, heading difference, vertical separation and a vertically weighted distance, and are borrowed from the fish model of Calovi et al. and Lei et al. Attraction becomes repulsion below an equilibrium distance and is the only collision-avoidance mechanism.
- Neighbour selection: each agent interacts with the k=2 neighbours exerting the highest "influence" (an analytic function of the social terms), following the finding that fish attend to one or two neighbours.
- Order parameters: polarisation $P=\|\frac{1}{N}\sum_i \hat v_i\|$, dispersion about the barycentre, minimal inter-agent distance, and susceptibility taken as the variance of polarisation at fixed parameters.
- Platform: Bebop 2 drones adapted by Dronisos, ROS2 swarm controller, position setpoints with time-to-target, 50 m diameter virtual arena, 5-15 m altitude. Simulations use the same ROS2 stack with a first-order position-response model fitted from flights. Trajectories are resampled with Akima interpolation and smoothed with Savitzky-Golay filtering.
- Three field scenarios: alignment staircase, alignment switching every 60 s, and the staircase repeated with an autonomous intruder flying at the barycentre.

## Limitations and open questions

- Control is not fully on board: commands go through the Dronisos ground station with 1 Hz telemetry, so delays are large and only partly modelled.
- N=10 in the field is far from any thermodynamic limit. "Critical" here means the fluctuation maximum on a finite system, and no finite-size scaling exponents are extracted.
- Field sampling near the critical region is thin (the authors note an outlier attributed to limited data).
- The intruder is non-reactive. Adaptive predators, and adaptive gain control by the swarm itself, are left open.

## Relevance to us

This is the closest physical-robot analogue to the hackathon's core question of whether operating near an order-disorder transition buys responsiveness. It gives concrete observables (polarisation variance, recovery time, switching asymmetry) and an open dataset we could reanalyse. It links to criticality measurement in animal groups ([[cavagna-2010-scale]], [[attanasi-2014-collective]]), to the fish model it inherits from ([[calovi-2014-swarming]]), and to learned controllers that do not tune for criticality at all ([[choi-2026-communication]], [[zhang-2025-learning]]).

## Notes from dmarz/swarm-robotics-recent-audit

Audited 2026-10-03 against the arXiv HTML (2512.21196). Checked the two-fold slope shift of the critical line with doubled N, the 5 s vs 15 s switching asymmetry, 18-22 km/h wind with 33 km/h gusts, 1 Hz telemetry, two influential neighbours, the 50 m arena at 5-15 m altitude, 200 simulation repetitions per intruder condition, the about-twice dispersion change of swarming vs schooling and the 1.5x velocity response of the critical regime, and the Zenodo DOI. All match. No corrections needed. Citation count now from OpenAlex.
