---
id: gunter-2021-commercially
type: paper
title: Are Commercially Implemented Adaptive Cruise Control Systems String Stable?
authors:
- George Gunter
- Derek Gloudemans
- Raphael E. Stern
- Sean McQuade
- Rahul Bhadani
- Matt Bunting
- Maria Laura Delle Monache
- Roman Lysecky
- Benjamin Seibold
- Jonathan Sprinkle
- Benedetto Piccoli
- Daniel B. Work
year: 2021
venue: IEEE Transactions on Intelligent Transportation Systems
url: https://arxiv.org/abs/1905.02108
doi: 10.1109/tits.2020.3000682
arxiv: '1905.02108'
cite: Gunter, G., Gloudemans, D., Stern, R. E., McQuade, S., Bhadani, R., Bunting, M., Delle Monache, M. L., Lysecky, R., Seibold, B., Sprinkle, J., et al. (2021). Are Commercially Implemented Adaptive Cruise Control Systems String Stable?. IEEE Transactions on Intelligent Transportation Systems, 22(11), 6992–7003. https://doi.org/10.1109/tits.2020.3000682
topics:
- crowds-and-traffic
- sync-consensus
added_by: dmarz/crowds-and-traffic
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 247 (Crossref, 2026-10-03)
code: []
---

## Summary

Tests the string stability of seven 2018 model-year adaptive cruise control (ACC) systems from two makes using more than 1,200 miles of car-following data. Fitting a linear second-order delay differential equation to each black-box ACC, all seven are string unstable. A platoon experiment with identical vehicles confirms it: a 6 mph disturbance grows to 25 mph, at which point the last vehicle's ACC disengages. The data are released as the largest public comparative ACC dataset.

## Contribution

Shows that the automation already on the road amplifies, rather than damps, traffic waves, a key negative result for "automation will fix jams" claims and context for controller design in [[stern-2018-dissipation]].

## Key results

- Measured (abstract): 7/7 ACC models string unstable; 6 mph disturbance amplified to 25 mph in a same-model platoon.

## Methods and models

Car-following experiments; system identification of a linear second-order delay model; string-stability analysis. IEEE T-ITS 22(11), 6992–7003.

## Limitations and open questions

2018 model-year systems from two makes; firmware changes since then unknown. Abstract only.

## Relevance to us

A concrete example of locally reasonable controllers producing a collectively unstable swarm, and a public dataset for fitting agent models. Related: [[sugiyama-2008-traffic]], [[lee-2025-traffic]].
