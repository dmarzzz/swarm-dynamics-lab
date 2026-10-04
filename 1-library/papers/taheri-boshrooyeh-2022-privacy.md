---
id: taheri-boshrooyeh-2022-privacy
type: paper
title: "Privacy-Preserving Spam-Protected Gossip-Based Routing"
authors: ["Sanaz Taheri-Boshrooyeh", "Oskar Thorén", "Barry Whitehat", "Wei Jie Koh", "Onur Kilic", "Kobi Gurkan"]
year: 2022
venue: "arXiv preprint (cs.CR)"
url: https://arxiv.org/pdf/2207.00116
doi: "10.48550/arXiv.2207.00116"
arxiv: "2207.00116"
cite: "Taheri-Boshrooyeh, S., Thorén, O., Whitehat, B., Koh, W. J., Kilic, O., & Gurkan, K. (2022). Privacy-Preserving Spam-Protected Gossip-Based Routing. arXiv preprint arXiv:2207.00116."
topics: [sybil-resistance]
added_by: dmarz/sybil-credentials
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: [gh-vacp2p-zerokit]
---

## Summary

A two-page paper describing WAKU-RLN-RELAY, the spam and Sybil defence for the Waku anonymous gossip pub/sub network (built on libp2p GossipSub). Each peer stakes ETH into a registry contract to join an RLN group (a Merkle tree of identity commitments, kept off-chain by peers in this design). Peers may publish one message per epoch (epoch = floor(unix time / T)), attaching an internal nullifier H(H(sk, epoch)), a Shamir share of sk derived from the message, and a zkSNARK proving group membership and correct derivation. Relays verify the proof, drop messages whose epoch is more than Thr = D/T away from local time, and keep a nullifier map; two different messages in one epoch reveal two shares, which reconstruct sk, so anyone can remove the member and claim part of the stake.

## Contribution

First published end-to-end integration of the Rate-Limiting Nullifier ([[barrywhitehat-2019-semaphore]]) into a peer-to-peer routing layer, with design changes for cost: off-chain tree (constant-cost registration and deletion instead of logarithmic on-chain updates) and off-chain message propagation.

## Key results

- Membership proof generation for a group of 2^32 takes about 0.5 s on an iPhone 8; verification is constant at about 30 ms (numbers cited from the kilic/rln library, not newly measured).
- Each peer stores 32-byte keys and a prover key of about 3.89 MB; a depth-20 tree needs 67 MB, reducible to 0.128 KB with a frontier optimisation.
- Claims: global spam protection where PoW (Whisper, EIP-627) is too costly for constrained devices and GossipSub peer scoring is local and cheap to defeat with many bots; Sybil attacks are "mitigated by making registration expensive".

## Methods and models

Construction description plus a proof-of-concept in nim-waku. No formal security proof, no simulation of attacks, no measurement of network-level spam under adversarial load.

## Limitations and open questions

- Sybil resistance reduces entirely to the stake price; the paper gives no analysis of what stake level deters which attacker.
- Peers must stay synchronised with the group tree; proving against a stale root leaks the member's index.
- A rate of exactly one message per epoch is coarse (later RLNv2 allows a per-member limit, see [[gh-vacp2p-zerokit]]).
- Epoch validation depends on loosely synchronised clocks.

## Relevance to us

This is the cleanest worked example of rate-limited anonymous participation in a gossip swarm: every agent may speak, nobody can tell which registered agent spoke, and an agent that exceeds its rate loses its stake and identity to whoever notices. It is directly applicable to an LLM agent swarm that communicates over a gossip bus, and it links staking (economic Sybil cost) with cryptographic accountability. Generalisations: [[rosenberg-2023-zk-creds]] (arbitrary predicates), [[crapis-2026-zk]] (RLN for paid API calls with refunds). Contrast with reputation-based peer scoring, which the paper argues is Sybil-cheap.
