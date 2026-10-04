---
id: pacheco-2024-toychain
type: paper
title: "Toychain: A Simple Blockchain for Research in Swarm Robotics"
authors: ["Alexandre Pacheco", "Ulysse Denis", "Raina Zakir", "Volker Strobel", "Andreagiovanni Reina", "Marco Dorigo"]
year: 2024
venue: "arXiv preprint (technical report)"
url: https://arxiv.org/abs/2407.06630
doi: null
arxiv: "2407.06630"
cite: "Pacheco, A., Denis, U., Zakir, R., Strobel, V., Reina, A., & Dorigo, M. (2024). Toychain: A Simple Blockchain for Research in Swarm Robotics. arXiv:2407.06630."
topics: [sybil-resistance, swarm-robotics, meta]
added_by: dmarz/sybil-robotics
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "1 (OpenAlex, 2026-10-03)"
code: [gh-teksander-toychain]
---

## Summary

Technical report describing Toychain, a lightweight Python blockchain for robotics research that integrates with ARGoS, Gazebo and ROS 2 and runs on real Wi-Fi robots. Supports Python smart contracts and pluggable consensus protocols, currently proof of work and proof of authority.

## Contribution

Lowers the barrier to ledger-coordinated swarm experiments relative to the Ethereum/Docker stack of [[strobel-2020-blockchain]].

## Key results

- Tool description; no benchmark numbers in the abstract.

## Methods and models

Software description. Abstract read only; details beyond the abstract not checked.

## Limitations and open questions

Research tool, not hardened; proof of authority hands Sybil resistance to an authority list.

## Relevance to us

If we want to run a stake-to-speak or deposit-and-slash experiment on simulated agents quickly, this is the lightest available codebase. Code: [[gh-teksander-toychain]].
