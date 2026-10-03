---
id: quinn-2025-decentralised
type: paper
title: Decentralised, Self-Organising Drone Swarms using Coupled Oscillators
authors: [Kevin Quinn, Cormac Molloy, Harun Siljak]
year: 2025
venue: 2025 8th International Balkan Conference on Communications and Networking (Balkancom)
url: https://arxiv.org/abs/2505.00442
doi: 10.1109/balkancom65827.2025.11185990
arxiv: '2505.00442'
cite: "Quinn, K., Molloy, C., & Šiljak, H. (2025). Decentralised, self-organising drone swarms using coupled oscillators. In 2025 8th International Balkan Conference on Communications and Networking (Balkancom) (pp. 1-6). IEEE."
topics: [sync-consensus, swarm-robotics]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "1 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Implements decentralised swarmalator-style syncing and swarming on Bitcraze Crazyflie 2.1 drones with
Lighthouse positioning. Starting from Mirollo-Strogatz pulse coupling and the [[okeeffe-2017-oscillators]]
model in simulation (N = 9 and N = 20), the authors replace continuous all-to-all coupling with pulse-based
peer-to-peer broadcasts: each drone updates its phase and position from only the most recent broadcaster,
theta_i <- theta_i + K_C sin(theta_j - theta_i), with moving-average or exponential smoothing to suppress jitter. A
second "hidden" phase driven to desynchronisation schedules broadcasts so messages do not collide.

## Contribution

A practical recipe for running swarmalators on small drones without a base station, solving radio
interference with a desynchronising oscillator (a TDMA-like slotting that emerges from negative coupling).
Contrasts itself with [[barcis-2020-sandsbots]], which it says used a base station for the Crazyflie demo.

## Key results

- Measured (qualitative, small groups): five drones phase-synchronised in under a couple of seconds; very high
  K_C makes the whole swarm jump to a newcomer's phase instead of converging mutually (Fig. 4); a removed and
  re-added drone re-merged quickly; slight frequency differences synchronised given high K_C.
- Swarming trajectories with no smoothing show "shuffling"; exponential smoothing (alpha = 0.8) and moving
  averages (N = 10, 20) were compared visually (Fig. 5). No quantitative order-parameter results.

## Methods and models

Crazyflie 2.1, HTC Vive Lighthouse positioning with onboard Kalman filter; Python simulations of pulse-coupled
oscillators and swarmalators (parameters K_C = +/-0.7, J = 0.8, B = 3, A = 1, N = 20). Read the arXiv version
through the results section. No code link found.

## Limitations and open questions

Small group sizes, no statistics, results mostly shown as plots; pairwise last-broadcaster updates change the
model's mean-field character and its states are not characterised.

## Relevance to us

The most hackathon-ready recipe found: cheap drones, decentralised, with a trick (hidden desync phase) for
channel access that is itself a sync-consensus idea. A natural baseline for any drone demo; compare with
[[barcis-2020-sandsbots]] and [[trianni-2009-self]].
