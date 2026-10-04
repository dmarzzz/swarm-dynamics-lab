---
id: gh-ethereum-devp2p
type: code
title: "ethereum/devp2p: Ethereum peer-to-peer networking specifications, including the Node Discovery v5 rationale on Sybil and eclipse attacks"
repo: ethereum/devp2p
url: https://github.com/ethereum/devp2p/blob/master/discv5/discv5-rationale.md
authors: ["Ethereum devp2p specification authors (the rationale document names no individual author)"]
year: 2015
language: Markdown (specifications)
license: "none detected by the GitHub API"
stars: 1125
last_commit: 2026-08-27
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
papers: [marcus-2018-low-resource, baumgart-2007-skademlia]
---

## Summary

The devp2p repository specifies Ethereum's networking layer (RLPx, discv4, discv5, ENR, DNS discovery). This entry covers discv5/discv5-rationale.md (protocol version v5.1, last changed 2026-08-27), which lists design requirements and security goals for Node Discovery v5 and its topic-based service discovery (TopDisc). Its "Sybil and Eclipse Attacks" section states that creating node identities is essentially free, that Sybils matter little for plain node enumeration but are serious for topic discovery, and that no single solution fully protects a structured overlay; it then recommends IP-subnet limits on routing tables, not admitting new members on incoming contact unless the table is well stocked from outbound queries, and liveness checks on an independent schedule that favours long-lived nodes. It rejects mandatory proof-of-work ids for now but keeps an escape hatch through mixed ENR identity schemes.

## What it can do for us

A compact engineering checklist for Sybil and eclipse resistance in a discovery layer, written by the people who run it: limit Kademlia buckets to two nodes per /24 and the whole table to ten per /24; prefer outbound-discovered peers; do not let incoming traffic trigger evictions; age-weight liveness checks. For service discovery it adds waiting-time admission control with tickets: registrars make advertisers wait longer when an ad would raise cache occupancy, duplicate an already well represented topic (service similarity) or come from an over-represented IP prefix (IP similarity), with a safety constant so waiting never drops to zero and a lower bound so re-requesting tickets does not help. Security goals named explicitly include advertisement flooding, registrar resource exhaustion, service censorship, service eclipse, service-table poisoning and advertisement redirection. Each maps onto an agent registry where agents advertise capabilities under topics.

## Run notes

Not run. The rationale document was read in full except the wire-encoding details of the encryption section.

## Limitations

The document gives no measured attack costs; its claims are design arguments. The note that a global limit on node IDs per IP is itself an attack vector (an attacker can claim many IDs on a victim's IP and lock it out) shows that identity-per-address limits must be local. The rationale argues PoW ids "can never beat determined attackers", consistent with [[castro-2002-secure]] and in tension with the resource-competitive results of [[gupta-2021-bankrupting]].

## Relevance to us

Bounds influence per network prefix and per incoming contact, and bounds time-to-admission per advertiser; it does not bound identities. Topic discovery is the closest analogue in Ethereum to an agent capability registry (ERC-8004 style or A2A agent cards), and the IP-similarity waiting time is a graded alternative to a hard one-per-prefix rule. Related: [[marcus-2018-low-resource]], [[baumgart-2007-skademlia]], [[alpturer-2026-aetherweave]], [[kadianakis-2023-proof]], [[heimbach-2024-deanonymizing]], [[gh-libp2p-specs]].
