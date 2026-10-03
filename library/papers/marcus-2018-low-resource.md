---
id: marcus-2018-low-resource
type: paper
title: "Low-Resource Eclipse Attacks on Ethereum's Peer-to-Peer Network"
authors: ["Yuval Marcus", "Ethan Heilman", "Sharon Goldberg"]
year: 2018
venue: "IACR Cryptology ePrint Archive, Report 2018/236"
url: https://eprint.iacr.org/2018/236.pdf
doi: null
arxiv: null
cite: "Marcus, Y., Heilman, E., & Goldberg, S. (2018). Low-Resource Eclipse Attacks on Ethereum's Peer-to-Peer Network. IACR Cryptology ePrint Archive, Report 2018/236. https://eprint.iacr.org/2018/236"
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: "208 (Semantic Scholar, 2026-10-03; S2 lists the record under year 2020)"
code: []
---

## Summary

The authors eclipse Ethereum geth nodes (version 1.6.6, discovery protocol v4) using only two hosts, each with one IP address. Two attacks are given: connection monopolisation, which fills all 25 maxpeers slots with incoming connections right after the victim reboots, and "owning the table", which uses crafted node IDs (free ECDSA keys chosen to land in specific Kademlia buckets) to ping the victim so that its outgoing connections go to attacker IDs after restart. A third attack works if the victim's clock is more than 20 seconds ahead. They trace the weakness to Ethereum's adoption of Kademlia, whose public XOR distance metric and cheap node IDs it does not actually need, and propose countermeasures, several of which shipped in geth 1.8.0.

## Contribution

Shows that cryptographic node identity without a cost of creation is a Sybil vector: Ethereum's authenticated messages and 13 outgoing connections looked stronger than Bitcoin's 8, but free node IDs made eclipsing far cheaper than in [[heilman-2015-eclipse]].

## Key results

- Before geth 1.8, an unlimited number of node IDs could run from one machine with one IP; thousands of IDs can be generated in seconds.
- On a long-running victim, the table attack owned all 25 connections in 34 of 51 reboots (66%) and owned all outgoing connections in 49 of 51 (96%); on a young victim in Singapore, 44 of 50 reboots (88%). Most failures were honest nodes sneaking in incoming connections.
- A precomputed lookup table of crafted IDs lets the attack scale to many victims.
- Countermeasure 1 (an upper limit on incoming TCP connections, forcing a mix of incoming and outgoing) is live in geth 1.8.0, with a configurable bound that defaults to floor(maxpeers/3) = 8. Countermeasure 2 (one-to-one IP to key mapping) was only partly adopted: geth 1.8.0 limits nodes from the same /24 to two per bucket and ten per table, so each attacker IP can still contribute up to ten IDs.
- Countermeasures 3 and 4 (secret, salted mapping of IDs to buckets; private lookup targets) were not adopted because they remove Kademlia's public distance metric. Countermeasures 5 and 6 (always seed from the database; delay unsolicited bonding until seeding completes) shipped in 1.8.0.

## Methods and models

Exposition of geth's RLPx discovery v4 by reverse engineering the code (db, table with 256 buckets of 16, bonding, seeding, lookup(self)). Attacks run from machines in Boston and New York against the authors' own instrumented victims on mainnet. I read the introduction, attack descriptions, experiments and countermeasure sections, not the time-manipulation section in full.

## Limitations and open questions

Victims were the authors' nodes, rebooted repeatedly; the authors note this skews results. The fix that shipped bounds IDs per /24 rather than binding one key per IP, which still lets cheap cloud ranges contribute many IDs. Results predate discovery v5 ([[gh-ethereum-devp2p]]).

## Relevance to us

Agent identities are usually key pairs, and key pairs are free, which is the exact precondition for this attack. Any agent overlay that places agents by a public function of their key (DHT distance, hash-based sharding) lets an attacker grind keys to sit next to a target. The fixes generalise: cap inbound slots, prefer outbound peers chosen by the victim, salt the placement function with a local secret, and limit identities per network prefix or per stake. This is the Ethereum execution-layer p2p that mempool transactions, and hence searcher and builder order flow, travel over before they reach Flashbots infrastructure. Bounds identities per IP prefix and influence via inbound caps. Related: [[heilman-2015-eclipse]], [[baumgart-2007-skademlia]], [[singh-2006-eclipse]], [[kadianakis-2023-proof]], [[alpturer-2026-aetherweave]], [[heimbach-2024-deanonymizing]].
