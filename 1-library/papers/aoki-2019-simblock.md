---
id: aoki-2019-simblock
type: paper
title: "SimBlock: A Blockchain Network Simulator"
authors: ["Yusuke Aoki", "Kai Otsuki", "Takeshi Kaneko", "Ryohei Banno", "Kazuyuki Shudo"]
year: 2019
venue: "IEEE INFOCOM 2019 Workshops (INFOCOM WKSHPS)"
url: https://doi.org/10.1109/infcomw.2019.8845253
doi: "10.1109/infcomw.2019.8845253"
arxiv: null
cite: "Aoki, Y., Otsuki, K., Kaneko, T., Banno, R., & Shudo, K. (2019). SimBlock: A Blockchain Network Simulator. In IEEE INFOCOM 2019 - IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS), 325\u2013329."
topics: [sync-consensus]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "162 (Semantic Scholar, 2026-10-03)"
code: [gh-dsg-titech-simblock]
---

## Summary

Introduces SimBlock, a blockchain network simulator built because experiments on real blockchains need many nodes across wide areas. Unlike earlier simulators it makes node behaviour easy to change. The authors compare simulated results with measurements from real blockchains to argue validity, then study how neighbour-selection algorithms and relay networks affect block propagation time.

## Contribution

An open, behaviour-modifiable block propagation simulator, validated against measured block propagation.

## Key results

- Simulated values compared with real blockchain measurements (abstract; numbers not read).
- Neighbour selection and relay networks shown to change block propagation time (abstract).

## Methods and models

Not read beyond the abstract (fetched from Semantic Scholar).

## Limitations and open questions

Only the abstract was read. Proof-of-work propagation focus.

## Relevance to us

Background for block propagation modelling; low priority for the lab.
