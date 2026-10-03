---
id: dobrokhvalov-2025-privacy
type: blog
title: "Privacy-Preserving Sybil Resistance via MPC-TLS and Semaphore Proofs"
authors: [Mikhail Dobrokhvalov]
year: 2025
url: https://ethresear.ch/t/privacy-preserving-sybil-resistance-via-mpc-tls-and-semaphore-proofs/22722
site: ethresear.ch
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Forum post (9 July 2025) describing BringID, a design for proving control of real web accounts (Uber, GitHub, Airbnb) without revealing them. A browser extension and a TLS Notary jointly run an MPC-TLS session with the web service; the notary sees only ciphertext and signs an attestation over committed fields. The user then derives an identity commitment Hash(master_key || credential_group_id || account_id_hash) and adds it to a Semaphore group per credential type. Verifiers receive zero-knowledge group-membership proofs and can combine several groups into a composite trust score. The security model is explicitly economic: Sybils are not prevented cryptographically, only made unprofitable when reward per verified account is below the cost of producing an aged, active web account. In the replies the author sketches revocation: commitments may be updated only periodically (for example monthly) and verifications expire, so a hijacked account can be re-bound only after expiry.

## Key claims

- Web accounts with real-world activity history (rides, commits, stays) carry a forging cost that can be imported into a Sybil filter.
- Separate Semaphore groups per credential type give unlinkability across accounts and applications while allowing composable proofs.
- The design currently trusts a single TLS Notary; TEE-backed or distributed notaries are named as future work.
- Updating a commitment more often than the expiry period would let one web account yield two nullifiers in the same scope, so update frequency must be limited.

## Evidence quality

Design post with a linked draft whitepaper; no deployment numbers or attack-cost measurements are given. The economic assumption (reward per account < forging cost) is stated but not quantified.

## Relevance to us

This is the "import a cost from outside the system" approach to Sybil resistance, made private. For agent swarms the analogous move is binding each agent identity to an externally costly, hard-to-mint credential held by its operator, with one nullifier per context. It also shows a weakness that matters for agents: the credential proves an account exists, not that a distinct human or agent is acting, so account rental and purchase remain open (compare encumbrance attacks in [[austgen-2023-complete]]). Related: per-context nullifiers in [[ethresearch-2026-anonymous]], market pricing of identity cost in [[porobov-2026-price]].

Its group-proof layer is Semaphore [[gh-semaphore-protocol-semaphore]]; rate-limiting nullifiers for spam are in [[barrywhitehat-2019-semaphore]].
