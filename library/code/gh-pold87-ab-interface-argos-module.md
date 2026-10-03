---
id: gh-pold87-ab-interface-argos-module
type: code
title: "AB-interface-ARGoS-module: ARGoS side of the ARGoS-Blockchain interface comparing consensus protocols under Byzantine robots (Strobel et al., Frontiers 2020)"
repo: Pold87/AB-interface-ARGoS-module
url: https://github.com/Pold87/AB-interface-ARGoS-module
authors: ["Volker Strobel", "Eduardo Castello Ferrer", "Marco Dorigo"]
year: 2018
language: "C++"
license: "none stated"
stars: 7
last_commit: 2020-09-22
topics: [sybil-resistance, swarm-robotics, collective-decision]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

ARGoS module for the simulations in "Blockchain Technology Secures Robot Swarms: A Comparison of Consensus Protocols and Their Resilience to Byzantine Robots" (Frontiers in Robotics and AI, 2020). Robots interact with dockerised Ethereum nodes through C++; companion repo Pold87/AB-interface-Blockchain-module holds the blockchain side. Experiments are launched with starter scripts (for example `bash starters/1_Plain.sh 3`) that source a general config.

## What it can do for us

Lets us compare how proof-of-work and proof-of-authority style consensus behave as Byzantine robot counts rise. Proof-of-work is itself a Sybil-resistance mechanism (influence costs compute), so this is the one robot-swarm codebase that measures a Sybil-resistance mechanism directly. Related: [[gh-pold87-blockchain-swarm-robotics]], [[strobel-2023-robot]].

## Run notes

Not run. Build with cmake; README contains hard-coded absolute paths from the author's machine that would need editing.

## Limitations

Last commit 2020; hard-coded paths; no licence stated.
