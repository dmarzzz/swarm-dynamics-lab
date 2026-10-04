---
id: gh-trustalabs-airdrop-sybil-identification
type: code
title: "Trusta Labs Airdrop-Sybil-Identification: two-phase graph clustering plus behavioural refinement for airdrop Sybil detection"
repo: TrustaLabs/Airdrop-Sybil-Identification
url: https://github.com/TrustaLabs/Airdrop-Sybil-Identification
authors: ["Trusta Labs"]
year: 2023
language: "Python"
license: "GPL-3.0"
stars: 58
last_commit: 2023-09-22
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Vendor repository describing Trusta Labs' framework. Phase 1 builds asset transfer graphs between externally owned accounts (with hub addresses removed), especially the sparse first-gas-funding graph, and applies Louvain and K-core community detection to find star-divergence, star-convergence, tree and chain patterns. Phase 2 refines each cluster with a K-means-like loop over transactional and profile features, dropping addresses far from the centroid to cut false positives. Example clusters on Ethereum contain 170, 24 and 50 addresses. The README also argues ML clustering is preferable to proof of personhood for permissionless systems and notes that Gitcoin Passport added the TrustaLabs score as a stamp before GG18.

## What it can do for us

A documented recipe for detecting coordinated identity farms from behaviour alone, which is how an operator of many scripted agents would be caught. Its two phases (graph coordination, then behavioural similarity) map to two observable channels in an agent swarm: who funds or messages whom, and how similar their action sequences are. Compare [[gh-arbitrumfoundation-sybil-detection]].

## Run notes

Not run. README read. The code is small: `src/scripts/` holds `components_scripts.py`, `kdtree_dist_cluster.py` and `network_community.py` (together about 4 KB) and `data/scripts/addr_action_feat.sql` builds per-address action features; file sizes from the GitHub API, contents not read.

## Limitations

Vendor material, labelled as such; no evaluation against ground truth. Last commit September 2023.


## Notes from shadow/sol-g49

Dataset audit 2026-10-03: GitHub recursive tree contains SQL feature extraction and Python clustering/community/KD-tree code, not a checked-in labelled address corpus. No runnable ground-truth dataset found in this repo; code licence does not provide data access. Hop public elimination/control lists already catalogued as data-hop-sybil-2022, with no stated data licence. ArbitrumFoundation/sybil-detection tree contains README plus four images and no label set. ERC-8004 author release is separately catalogued at data-erc8004-2026, CC0, loaded snapshot of 10,000 registry rows. Distinguish Sybil bounty/enforcement outputs from proven autonomous-agent identities.
