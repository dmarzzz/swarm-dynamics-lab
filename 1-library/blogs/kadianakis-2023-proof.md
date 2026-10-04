---
id: kadianakis-2023-proof
type: blog
title: "Proof of Validator: A simple anonymous credential scheme for Ethereum's DHT"
authors: [George Kadianakis, Mary Maller, Andrija Novakovic, Suphanat Chunhapanya]
year: 2023
url: https://ethresear.ch/t/proof-of-validator-a-simple-anonymous-credential-scheme-for-ethereums-dht/16454
site: ethresear.ch
topics: [sybil-resistance, sync-consensus]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Forum post (23 August 2023) motivated by a Sybil attack on data availability sampling over a Kademlia DHT: an attacker generates many node IDs close to a victim's ID and withholds information about the victim, so its samples become undiscoverable. The proposed fix restricts DHT membership to beacon-chain validators via an anonymous credential. Each validator registers p_i = Hash(s_i); to join, a node publishes a derived key D = s_i G and proves in zero knowledge that p_i is in the registered set and that D was derived from the matching secret. Two membership-proof instantiations are given: a Merkle tree with a SNARK-friendly hash (no trusted setup) and a Caulk+ lookup over a KZG commitment (faster, but needs a large trusted setup). Requirements are uniqueness (one derived key per validator, so misbehaving keys can be blocklisted), privacy (derived key not linkable to the validator) and verification under 200 ms. Halo2/IPA Merkle benchmarks on an i7-8550U laptop: 325 ms prover and 13.8 ms verifier for 4 million validators (depth 22), 547 ms and 21 ms for 67 million (depth 26), proofs about 3 KB.

## Key claims

- Tying network-layer identities to staked validators makes a DHT Sybil attack cost staked ETH.
- Uniqueness of the derived key both caps Sybil count and enables local punishment by blocklisting.
- Rotating daily keys (r_i = Hash(s_i || daily string)) improve privacy but let a misbehaving node escape its blocklist the next day; permanent blocklisting of rotating identities needs a stronger scheme such as SNARKBlock.
- In replies the authors confirm that an operator with k validators gets a quota of k DHT identities: the scheme is stake-proportional, not one-per-operator.

## Evidence quality

Concrete protocol with benchmarks from linked code; no deployment. The Sybil bound is economic (stake per identity), not a personhood bound.

## Relevance to us

This is a clean, small template for "join the overlay only with an unlinkable proof that you hold a scarce credential, with one derived key per credential". It maps onto agent swarms where agents must prove membership in an admitted set (staked, credentialed) without revealing which member they are, while still allowing per-identity punishment. The reply about multi-validator operators is the key caveat for swarms: credential-per-identity schemes bound Sybils by the scarce resource, not by the number of principals. The later stake-backed discovery design [[alpturer-2026-aetherweave]] extends the same idea with slashing that de-anonymises only misbehaving nodes. Compare per-context nullifiers in [[ethresearch-2026-anonymous]].
