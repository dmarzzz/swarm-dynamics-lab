---
id: cholez-2024-sybil
type: paper
title: "Sybil Attack Strikes Again: Denying Content Access in IPFS with a Single Computer"
authors: [Thibault Cholez, Claudia-Lavinia Ignat]
year: 2024
venue: ARES 2024, The 19th International Conference on Availability, Reliability and Security, Vienna, article 11, pp. 1-7
url: https://inria.hal.science/hal-04666290/document
doi: 10.1145/3664476.3664482
arxiv: null
cite: "Cholez, T., & Ignat, C.-L. (2024). Sybil Attack Strikes Again: Denying Content Access in IPFS with a Single Computer. In Proceedings of the 19th International Conference on Availability, Reliability and Security (ARES 2024), pp. 1-7. ACM. https://doi.org/10.1145/3664476.3664482"
topics: [sybil-resistance]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: full
relevance: 3
citations: "not checked (OpenAlex budget exhausted 2026-10-03)"
code: []
---

## Summary

Re-runs the classic localised Sybil attack from the 2000s P2P literature against IPFS, the largest live Kademlia DHT, and finds no basic defences. Attack: IPFS stores Provider records for a content id (Cid) on the 20 peers whose PeerIDs are XOR-closest to the Cid, and a lookup for the Cid stops once it has collected 10 Provider records, fake or not (go-libp2p-kad-dht/routing.go, Listing 1). PeerIDs are hashes of self-generated keys, so the attacker brute-forces keypairs until it has at least 20 PeerIDs within a chosen XOR distance of the target Cid; from a 3-day crawl of 3.5 million Cids and 6,800 PeerIDs the authors derive a distance bound of 2230 that beats every legitimate peer for 99.95 percent of Cids, and generate the needed identities in about 1.5 hours on an 8-core desktop. The Sybils run lightly modified Kubo clients that accept Provider records for the target but never return them. Experiments on the public network (Table 1): with 27 Sybils on 27 IP addresses, all 20 Provider records were captured in 8 of 11 runs on Kubo 0.19.2 and 10 of 12 on Kubo 0.20.0, failures all occurring within the first hour before Sybils were well integrated; with 20 Sybils behind a single IP address, every run succeeded (11 of 11 and 12 of 12), i.e. the IP diversity filter described in prior work was not in effect. Result is an almost complete denial of access to the targeted content. Findings were disclosed to Protocol Labs; the paper notes Kubo 0.28.0 still lacked the protection at time of writing. Recommended fixes, in layers: limit PeerIDs per IP or subnet (as KAD and gtk-gnutella did), do not let the Provider-count stop condition fire before a minimum number of lookup steps, and detect anomalous PeerID density around a key (statistical distance tests from the authors' earlier KAD work). Whole paper read (7 pages).

## Contribution

Empirical proof that a 2008-era Sybil eclipse of individual DHT keys works unchanged on IPFS in 2024, with concrete cost figures (one machine, one IP, 20 identities, about 90 minutes of key grinding), plus the specific code path that makes it cheap.

## Key results

- Distance bound 2230 beats legitimate peers for 99.95 percent of 3.5 million observed Cids (Section 3).
- 20 PeerIDs within that bound generated in about 1h30 on 8 cores.
- 27 Sybils / 27 IPs: 8/11 (Kubo 0.19.2) and 10/12 (0.20.0) full captures, near misses 17 to 19 of 20 records.
- 20 Sybils / 1 IP: 23/23 full captures, content unreachable.
- Lookup aborts at 10 Provider records regardless of provenance (Listing 1).

## Methods and models

Live-network experiments with modified Kubo clients in Docker, separate provider and fetcher machines, at least 15 minutes of Sybil integration before each trial; DHT crawl to calibrate the distance threshold; no simulation.

## Limitations and open questions

Targets one Cid at a time (localised eclipse), not the whole network. Success depends on Sybils having been online long enough to enter routing tables. Does not evaluate the proposed defences. The authors flag that discarded identifiers could be stored as a rainbow table to attack arbitrary Cids later, which is not tested.

## Relevance to us

A clean, current, low-cost case study of free-identity Sybil capture of a structured overlay, useful as the baseline threat for any agent swarm that uses a DHT or closest-id routing for discovery. Historical lineage: [[douceur-2002-sybil]], [[castro-2002-secure]], [[baumgart-2007-skademlia]], [[singh-2006-eclipse]]; compare the stake-based variant in [[gao-2025-heterogeneity]]. The "stop once you have enough answers" bug is a general lesson for aggregation in swarms: early-termination thresholds counted over unauthenticated responders are a Sybil amplifier.
