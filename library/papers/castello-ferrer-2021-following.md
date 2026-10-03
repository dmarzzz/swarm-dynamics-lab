---
id: castello-ferrer-2021-following
type: paper
title: "Following Leaders in Byzantine Multirobot Systems by Using Blockchain Technology"
authors: ["Eduardo Castelló Ferrer", "Ernesto Jiménez", "José Luis López-Presa", "Javier Martín-Rueda"]
year: 2021
venue: "IEEE Transactions on Robotics"
url: https://api.openalex.org/works/doi:10.1109/tro.2021.3104243
doi: "10.1109/tro.2021.3104243"
arxiv: null
cite: "Castelló Ferrer, E., Jiménez, E., López-Presa, J. L., & Martín-Rueda, J. (2021). Following Leaders in Byzantine Multirobot Systems by Using Blockchain Technology. IEEE Transactions on Robotics, 38(2), 1101-1117."
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "45 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Defines Byzantine Follow The Leader problems: leaders discover routes and broadcast directions while Byzantine robots try to hinder leaders and mislead followers. A blockchain serves as the broadcast medium. The authors give algorithms with correctness proofs, simulated validation in realistic scenarios, and bounds on robots reaching destination, steps taken and chain weight requirements.

## Contribution

Formal Byzantine problem definitions plus proofs for blockchain-mediated leader following, complementing the empirical work of [[strobel-2020-blockchain]].

## Key results

- Algorithms mitigate Byzantine impact in BFTL missions; min and max bounds on arrivals, steps and chain weight (abstract).

## Methods and models

Distributed algorithms over a blockchain broadcast layer; simulation. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Assumes the blockchain layer itself is secure, which shifts the Sybil question to the chain's admission rule.

## Relevance to us

Leader-follower is a common LLM orchestration pattern; using a ledger so followers can verify leader directives is a direct analogue.
