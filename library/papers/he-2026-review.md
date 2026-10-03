---
id: he-2026-review
type: paper
title: 'A Review of Stop-and-Go Traffic Wave Suppression Strategies: Variable Speed Limit Versus Jam-Absorption Driving'
authors:
- Zhengbing He
- Jorge A. Laval
- Yu Han
- Andreas Hegyi
- Ryosuke Nishi
- Cathy Wu
year: 2026
venue: IEEE Transactions on Intelligent Transportation Systems
url: https://arxiv.org/abs/2504.11372
doi: 10.1109/tits.2026.3658644
arxiv: '2504.11372'
cite: 'He, Z., Laval, J. A., Han, Y., Hegyi, A., Nishi, R., & Wu, C. (2026). A Review of Stop-and-Go Traffic Wave Suppression Strategies: Variable Speed Limit Versus Jam-Absorption Driving. IEEE Transactions on Intelligent Transportation Systems, 27(5), 4986–5000. https://doi.org/10.1109/tits.2026.3658644'
topics:
- crowds-and-traffic
- sync-consensus
- swarm-robotics
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 10 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

Review of the two main families of control for already-formed freeway stop-and-go waves: variable speed limits (VSL) broadcast from roadside gantries, and jam-absorption driving (JAD), where a single dedicated vehicle slows early ("slow-in, fast-out") so that it and the vehicles behind it arrive after the jam has dissolved. The authors show the two literatures share goals, logic (reduce inflow to the jam) and open questions but barely cite each other, compare representative studies in a table, and set out research opportunities on fundamental diagrams, secondary waves, generalisability, state estimation, randomness, validation scenarios and field deployment.

## Contribution

Unifies the infrastructure-based (VSL, for example the SPECIALIST algorithm) and vehicle-based (JAD, closely related to the connected-vehicle wave dampening of [[stern-2018-dissipation]] and [[lee-2025-traffic]]) approaches to wave suppression, and flags the secondary-wave problem as the main unresolved issue for both. A recent, control-oriented complement to the physics reviews [[helbing-2001-traffic]] and [[chowdhury-2000-statistical]].

## Key results

Synthesis claims from the literature (not new experiments):
- Stop-and-go waves travel upstream at about 10–20 km/h, can persist for tens of kilometres (one example in the cited data spans 190 km of observation, another propagates about 50 km), and the jam discharge rate can be up to 25% below capacity (the paper also cites outflow reductions up to 30%).
- Citation analysis of the selected representative papers: VSL papers cite other VSL papers 29 times and JAD papers 0 times; JAD papers cite JAD 27 times and VSL 20 times. The fields also use different words ("shock wave" versus "stop-and-go wave" or "oscillation"), which hampers search.
- VSL studies are strong in kinematic-wave theory and have field tests (SPECIALIST on a 14 km Dutch freeway in 2010) but often neglect secondary waves triggered by the imposed lower speed; JAD studies are mostly microscopic and simulation-based with weak theory and few field tests.
- JAD need not require connected and automated vehicles: police "swerving" observed on California freeways is cited as a practical form of jam absorption.

## Methods and models

Structured literature review restricted to suppression of fully developed waves (bottleneck and ramp-metering approaches excluded), mostly post-2003. Organises VSL into model-predictive-control (METANET-based) and kinematic-wave-theory (SPECIALIST family) threads, and JAD into theory-based (Newell car-following, kinematic waves) and simulation-based studies, with a comparison table of model, fundamental diagram assumption, simulator and number of lanes.

## Limitations and open questions

- Narrow scope: only VSL and JAD; connected-vehicle and RL controllers are discussed only where they overlap ([[jang-2025-reinforcement]], [[wu-2022-flow]]).
- Secondary-wave triggering and robustness to driver randomness remain open; few JAD field tests exist.
- I read the introduction, motivation, scope and parts of sections II–III; detailed per-study comparisons were skimmed.

## Relevance to us

Frames jam suppression as two distinct swarm-control architectures: global broadcast from outside the collective (VSL) versus an embedded agent that steers the collective from inside (JAD). That distinction maps directly onto leader or shepherd agents in robot swarms and is a clean experimental axis for the hackathon on a ring-road model ([[sugiyama-2008-traffic]], [[treiber-2000-congested]]). Also a good example of vocabulary fragmentation across communities, worth noting for any survey.
