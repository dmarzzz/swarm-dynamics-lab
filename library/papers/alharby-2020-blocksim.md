---
id: alharby-2020-blocksim
type: paper
title: "BlockSim: An Extensible Simulation Tool for Blockchain Systems"
authors: ["Maher Alharby", "Aad van Moorsel"]
year: 2020
venue: "Frontiers in Blockchain"
url: https://arxiv.org/abs/2004.13438
doi: "10.3389/fbloc.2020.00028"
arxiv: "2004.13438"
cite: "Alharby, M., & van Moorsel, A. (2020). BlockSim: An Extensible Simulation Tool for Blockchain Systems. Frontiers in Blockchain, 3, 28. https://doi.org/10.3389/fbloc.2020.00028"
topics: [sync-consensus]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "91 (Semantic Scholar, 2026-10-03)"
code: [gh-maher243-blocksim]
---

## Summary

Presents BlockSim, a framework and Python tool for discrete-event simulation of blockchain systems organised in network, consensus and incentive layers around a reusable Base Model, applied to Bitcoin, Ethereum and other consensus algorithms. Results are validated against measurements of real systems and earlier studies, and a closing study examines how uncle-block rewards affect mining decentralisation.

## Contribution

A layered, extensible blockchain simulation model in Python, positioned as general across blockchain designs.

## Key results

- Validation against real-system performance results and literature (abstract; numbers not read).
- Uncle-block rewards studied as a lever on mining decentralisation (abstract).

## Methods and models

Not read beyond the abstract.

## Limitations and open questions

Only the abstract was read. The code's last commit is 2022-03-26.

## Relevance to us

Background only; the layered model (network, consensus, incentives) is a reasonable outline for an agent-economy simulator.
