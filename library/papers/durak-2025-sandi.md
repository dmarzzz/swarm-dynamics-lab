---
id: durak-2025-sandi
type: paper
title: "Sandi: A System for Accountability"
authors: [F. Betül Durak, Kim Laine, Simon Langowski, Radames Cruz Moreno]
year: 2025
venue: "2025 IEEE 10th European Symposium on Security and Privacy (EuroS&P)"
url: https://arxiv.org/abs/2401.16759
doi: 10.1109/EuroSP63326.2025.00041
arxiv: "2401.16759"
cite: "Durak, F. B., Laine, K., Langowski, S., & Cruz Moreno, R. (2025). Sandi: A System for Accountability. In 2025 IEEE 10th European Symposium on Security and Privacy (EuroS&P), pp. 607-630. https://doi.org/10.1109/EuroSP63326.2025.00041"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "0 (Crossref, 2026-10-03)"
code: []
---

## Summary

Microsoft Research design for a downvote-only, privacy-preserving reputation system for first-contact communication (email, DMs) where the receiver has no prior relationship with the sender, motivated partly by generative AI making content alone a poor legitimacy signal. A central Accountability Server (AS) keeps a score per registered sender. To open an "endorsed channel", the sender gets an endorsement tag from AS containing commitments to its short-term verification key and the receiver's address, a timestamp, a coarse reputation level (e.g. low/medium/high, so the score cannot identify the sender), and the sender ID encrypted under an AS key, all signed by AS. The receiver sees the reputation and can report by returning the tag. Each epoch, AS updates the score from the number of reports plus differential-privacy noise (protecting reporters from retaliation); scores recover over time unless reports exceed a tolerance k. Blinded Privacy Pass tokens attached by the sender let AS prove it really received reports (score integrity against a malicious AS). Game-theoretic result: a rational sender's optimal strategy keeps reports per epoch near or below k, so k tunes behaviour. Implementation in Rust: endorsement tag 508 B, AS stores 160 B per sender, each protocol step runs in 158-279 microseconds single-threaded. Whitewashing (creating new sender accounts) is explicitly out of scope and assumed handled by account-creation friction. Skimmed: abstract, introduction, overview, optimality and implementation sections; proofs in appendices not read.

## Contribution

A reputation primitive with receiver-side reporting, sender unlinkability, reporter privacy via DP, and provable score integrity, built from standard cryptography (commitments, signatures, Privacy Pass) and cheap enough for messaging-scale use.

## Key results

- Endorsement tag 508 B; AS state 160 B per sender; sender state 248 B per channel.
- Protocol steps 158-279 microseconds per party on one core.
- Optimality theorems: optimal sender strategies are "normalized" and can be restricted to keeping reports plus noise at or below k per epoch.

## Methods and models

Cryptographic protocol design with security games (score integrity, communication privacy, reporter privacy, unlinkability), DP noise on report counts, a rational-sender game, Rust implementation (curve25519-dalek, ed25519-dalek, HMAC-SHA256, AES-CBC); code stated as MIT-licensed under Microsoft on GitHub (not opened).

## Limitations and open questions

Sybil resistance is delegated: it only works if sender accounts are costly (identity proof, PKI, phone verification), which is exactly what an AI-agent swarm operator attacks. Malicious mass-reporting by colluding receivers is acknowledged as indistinguishable from real reports. Centralised AS.

## Relevance to us

A ready design for attaching accountable, privacy-preserving reputation to messages from unknown senders, which is one way to make agent swarms pay for misbehaviour per sender identity. Its explicit dependence on whitewashing defences ties it to personhood and Sybil work: [[adler-2024-personhood]], [[douceur-2002-sybil]]. Privacy Pass building block: [[davidson-2018-privacy]], [[hanff-2025-security]].
