---
id: werner-allen-2005-firefly
type: paper
title: Firefly-inspired sensor network synchronicity with realistic radio effects
authors: [Geoffrey Werner-Allen, Geetika Tewari, Ankit Patel, Matt Welsh, Radhika Nagpal]
year: 2005
venue: "Proceedings of the 3rd International Conference on Embedded Networked Sensor Systems (SenSys '05)"
url: https://mdw.la/papers/firefly-sensys05.pdf
doi: 10.1145/1098918.1098934
arxiv: null
cite: "Werner-Allen, G., Tewari, G., Patel, A., Welsh, M., & Nagpal, R. (2005). Firefly-inspired sensor network synchronicity with realistic radio effects. In Proceedings of the 3rd International Conference on Embedded Networked Sensor Systems (SenSys '05) (pp. 142-153). ACM."
topics: [sync-consensus, swarm-robotics]
added_by: dmarz/sync-consensus-audit
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "316 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Implements Mirollo-Strogatz pulse-coupled synchronisation ([[mirollo-1990-synchronization]]) on real wireless
sensor motes, where radio messages are delayed and lost. The Reachback Firefly Algorithm (RFA) has each node
timestamp away the MAC delay, queue the firing messages it hears during a cycle, and apply all the phase jumps at
the start of its next cycle ("reachback") instead of instantaneously. The authors analyse convergence in simple
cases, explore parameters in the TOSSIM simulator, and run RFA on a 24-node MicaZ multi-hop testbed, reaching
group firing spreads of about 100 microseconds.

## Contribution

The landmark demonstration that the firefly/pulse-coupled oscillator model survives realistic communication
(non-zero, variable delay, message loss, asymmetric links, clock skew) on hardware, turning a biological
synchrony model into a leaderless networking primitive. It distinguishes synchronicity (agreeing on firing
phase) from time synchronisation (agreeing on a global clock).

## Key results

- Theory: for two nodes the reachback response still converges; time to synchrony is inversely proportional to the
  coupling strength epsilon (firing function constant FFC = 1/epsilon caps each jump at T/FFC).
- Simulation (TOSSIM, all-to-all and grid topologies, 10 seeds per setting, 3600 s runs): small FFC (e.g. 10,
  20, 50, 150) mostly failed to synchronise in all-to-all networks; on grids, very small (10) or very large (> 500) FFC
  failed; group spread grows with network diameter.
- Testbed (measured): 24 MicaZ motes over a building floor, multi-hop, links of varying quality, global reference
  from FTSP. All four runs (FFC 100, 250, 500, 1000) synchronised; FFC 100 synchronised in 284 s with 50th
  percentile group spread 131 us and 90th percentile 4664 us; FFC 250 took 344 s (128 us / 3605 us). Time to sync
  grows with FFC; the spread distribution is nearly independent of FFC, with an apparent floor near 100 us that the
  authors attribute to FTSP timestamp accuracy and clock skew.
- Comparison: unlike RBS, TPSN or FTSP there is no root, no per-neighbour state and no spanning tree, so the
  method is implicitly robust to node and link loss, but it does not provide a global clock.

## Methods and models

Discrete pulse-coupled oscillators with a simplified (linearised) firing function, phase period T = 100 units in
the analysis; MAC-delay timestamping; random application-level transmission delay to avoid the CSMA worst case;
TOSSIM simulation; TinyOS implementation on MicaZ (7.3 MHz) motes; firing groups identified by clustering
firing events; metrics: time to sync, 50th/90th percentile group spread. Read: abstract, Sections 1-3, the
simulation and testbed results and comparison; the convergence proof skimmed.

## Limitations and open questions

- Theory covers simple (two-node) cases; multi-hop convergence is empirical.
- Clock skew is not modelled by the M&S framework and limits accuracy; the evaluation's precision is bounded by
  FTSP.
- 90th-percentile spreads are milliseconds, much larger than the median, and some behaviour is left unexplained.

## Relevance to us

The most directly reusable sync primitive for a robot or drone swarm with cheap radios: leaderless, stateless,
tolerant of loss and delay, with measured numbers to beat. It is the hardware precedent for
[[barcis-2020-sandsbots]] and [[quinn-2025-decentralised]] and the engineering counterpart of
[[sarfati-2021-self]] (real fireflies) and [[yeung-1999-time]] (delay theory).
