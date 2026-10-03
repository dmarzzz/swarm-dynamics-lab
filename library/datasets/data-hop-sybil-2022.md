---
id: data-hop-sybil-2022
type: dataset
title: "Hop Protocol airdrop Sybil lists: eliminated Sybil attacker addresses and final eligible set (2022)"
authors: ["Hop Protocol"]
year: 2022
url: https://github.com/hop-protocol/hop-airdrop/tree/master/src/data
license: "none stated"
size: "eliminatedSybilAttackers.csv 610 KB (14,195 addresses); eligibleAddresses.txt 1.2 MB (28,857 addresses); finalDistribution.csv 13 MB; plus nine category blacklists (contract, exchange, deposit address, connection, Gitcoin grants and others)"
format: "CSV, TXT, JSON and TypeScript arrays of Ethereum addresses"
topics: [sybil-resistance]
added_by: dmarz/sybil-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: []
---

## Summary

Public output of the HOP token airdrop Sybil filtering. `eliminatedSybilAttackers.csv` lists 14,195 Ethereum addresses removed as Sybil attackers, mostly through community-submitted reports reviewed by the Hop team, and `eligibleAddresses.txt` lists the 28,857 addresses that remained eligible; the two sets are disjoint (checked). `groups.json`, `eliminatedGroups.ts` and `customGroups.ts` hold the cluster structure, and `blacklists/` holds category exclusions such as contracts, exchange and deposit addresses, and Gitcoin grants and Giveth related addresses. Labels are the outcome of a bounty process and manual review, not verified ground truth.

## Access

Public, no registration. Loaded on 2026-10-03:

```bash
curl -sL -o hop_elim.csv https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/eliminatedSybilAttackers.csv
curl -sL -o hop_elig.txt https://raw.githubusercontent.com/hop-protocol/hop-airdrop/master/src/data/eligibleAddresses.txt
```
```python
elim = set(l.strip().lower() for l in open('hop_elim.csv').readlines()[1:])   # header 'address'
elig = set(l.strip().lower() for l in open('hop_elig.txt') if l.startswith('0x'))
print(len(elim), len(elig), len(elim & elig))   # 14195 28857 0
```

## Relevance to us

One of the few public, address-level Sybil label sets from a real incentive programme, and an input to the Arbitrum filter ([[gh-arbitrumfoundation-sybil-detection]]). Joined with on-chain transfer histories it gives labelled clusters of identities run by one operator, usable to test whether coordination signatures learned on airdrop farms transfer to swarms of scripted or LLM agents. Produced by [[gh-hop-protocol-hop-airdrop]]. For the economics of airdrops that motivate such farming see [[messias-2023-airdrops]]. Caveat: positive labels come from reporters who were paid for finding Sybils, so the set is biased toward easily detected cluster shapes.
