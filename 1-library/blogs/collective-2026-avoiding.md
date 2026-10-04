---
id: collective-2026-avoiding
type: blog
title: "Avoiding Client Disruption in Anonymous Broadcast Protocols"
authors: [peg]
year: 2026
url: https://collective.flashbots.net/t/avoiding-client-disruption-in-anonymous-broadcast-protocols/5974
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Flashbots forum survey (September 2026) of how anonymous broadcast and secure aggregation protocols stop malicious clients from corrupting other clients' messages while keeping senders anonymous. It explains the Flashbots draft protocol Panetière, which aggregates encrypted multi-set encodings (IBLTs) under key-additive homomorphic encryption and relies on clients running inside TEEs so that attestation guarantees well-formed inputs. It compares this with Dissent, Verdict, Riposte, Blinder, Clarion, Spectrum, Rabbit-Mix, ZIPNet, Willow, Tacita, Ring of Gyges and Pepper.

## Key claims

- Anonymous broadcast faces a trilemma between strong anonymity, low latency and high bandwidth; the choice shapes how client disruption is handled.
- Panetière prioritises anonymity and latency, tolerates a minority of malicious servers, and does not need all clients to participate; client integrity comes from TEE attestation, used only for integrity, not for anonymity.
- Disruption defences surveyed: reactive accountability after a failed round (Dissent), per-message zero-knowledge proofs of slot ownership or cover traffic (Verdict, Spectrum), private audits by a non-colluding server (Riposte), MPC well-formedness checks (Blinder, Rabbit-Mix), blind MAC checks (Clarion), TEE-attested clients (ZIPNet, Panetière), zero-knowledge proofs of key knowledge (Willow).
- Zero-knowledge well-formedness proofs for Panetière's encoding are possible but slow and are being considered as an optimistic fallback requested only after a failure.

## Evidence quality

Literature survey by a practitioner, with design comparisons but no new measurements. The Panetière draft itself was not read for this entry.

## Relevance to us

Anonymous channels are where Sybil resistance is hardest, because the usual defence (link actions to an accountable identity) is ruled out by design. The survey shows the toolkit that remains: make each participant's contribution provably well-formed (proofs, MPC checks, attested clients) and bound how much any one client can write, so that many disruptive identities can only add noise in their own slots. For agent swarms that want private or anonymous coordination channels, this is the relevant design space; per-client attestation reduces disruption but, as in [[collective-2024-portrait]], does not by itself bound how many clients one operator runs. Related Flashbots network-anonymity work is described in the writings post on network-anonymized mempools (not catalogued separately).
