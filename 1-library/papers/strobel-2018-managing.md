---
id: strobel-2018-managing
type: paper
title: "Managing Byzantine Robots via Blockchain Technology in a Swarm Robotics Collective Decision Making Scenario"
authors: ["Volker Strobel", "Eduardo Castelló Ferrer", "Marco Dorigo"]
year: 2018
venue: "Proceedings of the 17th International Conference on Autonomous Agents and MultiAgent Systems (AAMAS 2018)"
url: https://api.openalex.org/works/doi:10.65109/nlel1871
doi: "10.65109/nlel1871"
arxiv: null
cite: "Strobel, V., Castelló Ferrer, E., & Dorigo, M. (2018). Managing Byzantine Robots via Blockchain Technology in a Swarm Robotics Collective Decision Making Scenario. In Proceedings of the 17th International Conference on Autonomous Agents and MultiAgent Systems (AAMAS 2018), 541-549."
topics: [sybil-resistance, swarm-robotics, collective-decision]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "132 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Proof of concept that smart contracts executed on a blockchain maintained by the swarm can act as a secure coordination layer for a binary collective decision task (which tile colour is in the majority). The contract identifies and excludes Byzantine robots, defined as arbitrarily faulty or malicious, and the authors compare the result against an existing collective decision strategy with and without Byzantine robots present.

## Contribution

First paper to put blockchain smart contracts under a swarm robotics collective decision task and argue that swarm fault tolerance cannot be assumed once Byzantine robots are present. Predecessor of [[strobel-2020-blockchain]] and [[strobel-2023-robot]].

## Key results

- Abstract reports a clear advantage of the blockchain approach when Byzantine robots are part of the swarm; per [[strobel-2020-blockchain]] (which summarises it), the meta-controller excludes robots that deviate from agreed behaviour while prior collective decision algorithms failed to reach consensus with one or more Byzantine robots.

## Methods and models

ARGoS simulation with Ethereum; collective perception scenario of Valentini et al. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Binary decision only; Sybil attacks are treated in the 2020 follow-up rather than here (as stated in that follow-up). Simulation only.

## Relevance to us

Establishes the AAMAS-community lineage for ledger-mediated Byzantine resistance in swarms, which is the closest robotics precedent for putting an agent swarm's shared decisions on a ledger with exclusion rules. See [[strobel-2020-blockchain]] for the Sybil experiment.
