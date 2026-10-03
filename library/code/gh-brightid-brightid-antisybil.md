---
id: gh-brightid-brightid-antisybil
type: code
title: "BrightID-AntiSybil: framework that simulates Sybil attacks on the BrightID social graph and compares anti-Sybil ranking algorithms"
repo: BrightID/BrightID-AntiSybil
url: https://github.com/BrightID/BrightID-AntiSybil
authors: ["BrightID contributors"]
year: 2018
language: "Python"
license: "ISC"
stars: 46
last_commit: 2021-11-13
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Evaluation package for the anti-Sybil algorithms used or considered by BrightID, a social-graph proof-of-uniqueness system. It implements SybilRank and several variants (GroupSybilRank on a graph of groups, WeightedSybilRank using common-neighbour edge weights, LandingProbability, NormalizedSybilRank with degree caps toward seeds), ClusterRank, SeednessScore and Yekta (a 1 to 5 rank from cluster-adjusted weighted degree). It then injects scripted attacks into the real BrightID graph: lone attackers targeting seeds, top-ranked nodes or random honest nodes; collaborative groups of attackers; seed nodes or honest nodes that turn and create Sybils; many-small-groups and multi-cluster attacks; plus a manual attack config.

## What it can do for us

The attack catalogue is the most useful part: it is a taxonomy of how colluding insiders and compromised seeds manufacture trusted identities, which is the threat model for any reputation layer over an agent swarm. The code can be pointed at a synthetic agent endorsement graph to compare SybilRank-family scores with the C++ detectors in [[gh-binghuiwang-sybildetection]].

## Run notes

Not run. Install per README: `git clone https://github.com/BrightID/BrightID-AntiSybil.git && cd BrightID-AntiSybil && pip3 install .`; attacks are configured in `anti_sybil/tests/attacks/config.py`. Running against the live graph needs a BrightID graph dump.

## Limitations

Last commit 2021. Results are reported on a wiki page and graph explorer hosted by BrightID rather than in a paper; we did not verify them. Seed-node trust is assumed; the attacks where seeds defect show that the whole scheme rests on seed honesty.
