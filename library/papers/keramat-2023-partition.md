---
id: keramat-2023-partition
type: paper
title: "Partition-Tolerant and Byzantine-Tolerant Decision Making for Distributed Robotic Systems With IOTA and ROS2"
authors: ["Farhad Keramat", "Jorge Peña Queralta", "Tomi Westerlund"]
year: 2023
venue: "IEEE Internet of Things Journal"
url: https://api.openalex.org/works/doi:10.1109/jiot.2023.3257984
doi: "10.1109/jiot.2023.3257984"
arxiv: null
cite: "Keramat, F., Peña Queralta, J., & Westerlund, T. (2023). Partition-Tolerant and Byzantine-Tolerant Decision Making for Distributed Robotic Systems With IOTA and ROS2. IEEE Internet of Things Journal, 10(14), 12985-12998."
topics: [sybil-resistance, swarm-robotics]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "31 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Integrates IOTA smart contracts with ROS 2 to give robot teams decision processes that tolerate network partitions and inherit Byzantine tolerance from the ledger. Demonstrated on cooperative mapping with intermittent connectivity, outperforming Ethereum under partitions with low computational overhead.

## Contribution

First IOTA plus ROS 2 integration for robots, addressing the partition problem that proof-of-work chains face in mobile swarms ([[strobel-2020-blockchain]] lists it as a limitation).

## Key results

- Better performance than Ethereum in the presence of network partitions and low resource use (abstract).

## Methods and models

IOTA DAG ledger with smart contracts, ROS 2. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Byzantine tolerance is inherited from the ledger rather than analysed; Sybil admission depends on IOTA's network configuration.

## Relevance to us

Shows the practical engineering path for ledger-coordinated agents under intermittent connectivity.
