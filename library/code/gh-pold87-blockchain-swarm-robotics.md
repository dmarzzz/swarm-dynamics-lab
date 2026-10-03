---
id: gh-pold87-blockchain-swarm-robotics
type: code
title: "blockchain-swarm-robotics: ARGoS plus Ethereum code for managing Byzantine robots in a collective decision task (Strobel et al., AAMAS 2018)"
repo: Pold87/blockchain-swarm-robotics
url: https://github.com/Pold87/blockchain-swarm-robotics
authors: ["Volker Strobel", "Eduardo Castello Ferrer", "Marco Dorigo"]
year: 2017
language: "C++"
license: "none stated"
stars: 37
last_commit: 2018-06-11
topics: [sybil-resistance, swarm-robotics, collective-decision]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Code for "Managing Byzantine Robots via Blockchain Technology in a Swarm Robotics Collective Decision Making Scenario" (Strobel, Castello Ferrer, Dorigo, AAMAS 2018). In ARGoS 3 with e-puck robots, the swarm solves a best-of-2 problem (which tile colour is more frequent on a black and white grid) following Valentini et al.; each robot runs its own geth Ethereum node and opinions are aggregated through smart contracts, which adds a security layer against Byzantine robots and a tamper-proof log for forensics. The README offers a VM image, a video tutorial, and build steps (ARGoS, ARGoS-epuck, Go 1.7.3, solc, cmake).

## What it can do for us

The earliest public testbed for Byzantine (and by extension Sybil) robots in a swarm consensus task, and the precursor of the token-economy result in [[strobel-2023-robot]]. Reusable as a baseline when testing whether an LLM-agent swarm's collective decision survives injected faulty agents. The newer modular version is [[gh-pold87-ab-interface-argos-module]].

## Run notes

Not run. Per README: install ARGoS and the e-puck plugin via `install_argos.sh`, run `create_geths.sh`, build with cmake, then `bash start_experiment1.sh 0 0 1`.

## Limitations

Unmaintained since 2018; the README says a cleaned-up version was in progress. Depends on Go 1.7-era geth. Byzantine robots here are a fixed fraction of identities; the setup does not let an attacker create new identities, so it tests Byzantine tolerance rather than Sybil resistance proper.
