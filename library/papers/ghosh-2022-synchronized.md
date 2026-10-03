---
id: ghosh-2022-synchronized
type: paper
title: The synchronized dynamics of time-varying networks
authors: [Dibakar Ghosh, Mattia Frasca, Alessandro Rizzo, Soumen Majhi, Sarbendu Rakshit, Karin Alfaro-Bittner, Stefano Boccaletti]
year: 2022
venue: Physics Reports
url: https://arxiv.org/abs/2109.07618
doi: 10.1016/j.physrep.2021.10.006
arxiv: '2109.07618'
cite: "Ghosh, D., Frasca, M., Rizzo, A., Majhi, S., Rakshit, S., Alfaro-Bittner, K., & Boccaletti, S. (2022). The synchronized dynamics of time-varying networks. Physics Reports, 949, 1-63."
topics: [sync-consensus, collective-motion]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "173 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Reviews synchronisation when the network itself changes in time. Two frameworks are covered in detail: (1)
networks whose links change through adaptation, external forcing or other link-level processes, and (2) networks
whose structure changes because the nodes are agents moving in physical space, with interactions switched on and
off by space-dependent rules (mobile oscillators, "moving agents"). The report ends with open problems.

## Contribution

The most complete review of synchronisation among moving agents short of swarmalators. In the mobile-oscillator
models it covers, motion shapes the graph; [[okeeffe-2017-oscillators]] characterises that earlier literature as
lacking feedback from phase to motion, the gap swarmalators fill. Also a highly cited forward citation of the swarmalator paper.

## Key results

- Abstract-level: review of adaptive/forced time-varying networks and of motion-induced time-varying networks;
  open problems.

## Methods and models

Review (76 pages, 34 figures per the arXiv record). Abstract read on arXiv.

## Limitations and open questions

Pre-dates most 2022-2026 swarmalator theory ([[sar-2026-interplay]]).

## Relevance to us

Background for drones whose communication graph changes with their positions (range-limited radios): when does
sync still happen? Pairs with [[jadbabaie-2003-coordination]] (consensus under switching) and
[[dorfler-2014-synchronization]].
