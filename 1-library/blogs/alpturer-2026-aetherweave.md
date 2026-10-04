---
id: alpturer-2026-aetherweave
type: blog
title: "AetherWeave: stake-backed peer discovery for Ethereum"
authors: [Kaya Alpturer, Constantine Doumanidis, Aviv Zohar]
year: 2026
url: https://ethresear.ch/t/aetherweave-stake-backed-peer-discovery-for-ethereum/24927
site: ethresear.ch
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

Forum post (22 May 2026) summarising a paper on Sybil- and eclipse-resistant peer discovery. Ethereum consensus makes identities expensive through stake, but its peer-discovery layer treats network identities as free, so an attacker with a few thousand IP addresses can crowd a node's peer table. AetherWeave requires each discovery node to back participation with a stake deposit, proves stake ownership in zero knowledge without revealing which deposit, limits request volume in proportion to stake, and lets anyone slash a node that sends too many requests: each request carries a share of a slashing secret, so two conflicting request batches in one round reveal the deposit. Each node keeps two peer tables of size s√n (s = 4 in experiments) seeded independently; the requester chooses a pseudorandom slice, so a malicious responder can only suppress matching records, not inject extra ones, and suppression shows up as an unexpectedly sparse table that triggers an eclipse alarm. Results claimed: per-node communication O(s√n) per round; a gossip convergence condition s²(1 − α) > 1, which with s = 4 tolerates up to 15/16 adversarial stake; a proof that any partition of honest nodes either fails or is detected by a large fraction of the smaller side when overlay degree is Ω(log n). A Prysm fork prototype ran up to 625 nodes on one AMD EPYC 9354P server with 2-minute rounds.

## Key claims

- The network layer under a Sybil-resistant consensus can remain the weak point; stake can be reused there.
- Unlinkability and slashability can coexist: honest nodes stay anonymous, misbehaviour leaks exactly the information needed to slash.
- Keeping the requester's slice seed private needs either a TEE at the responder or private information retrieval at higher bandwidth.

## Evidence quality

Summary of a paper with a proof sketch, mean-field analysis, prototype and simulator. I read the post's motivation, protocol, guarantees, privacy and prototype sections; I did not read the full paper or all replies (Micah Zoltu and Anton Nashatyrev comment).

## Relevance to us

AetherWeave is a design pattern for agent overlays: admit an agent to the discovery or gossip layer only with an anonymous proof of a bonded resource, rate-limit by that resource, and make protocol violations self-incriminating. The "requester picks the slice" trick, which turns injection attacks into detectable suppression, is useful for any swarm where agents learn about peers from other, possibly Sybil, agents. Builds on the anonymous-credential approach in [[kadianakis-2023-proof]]; falls in the bond category of [[ankushin-2026-public]].
