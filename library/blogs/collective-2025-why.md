---
id: collective-2025-why
type: blog
title: "Why TEE.fail is bullish for BuilderNet: Hardening the Path to Permissionless Blockbuilding"
authors: [Quintus]
year: 2025
url: https://collective.flashbots.net/t/why-tee-fail-is-bullish-for-buildernet-hardening-the-path-to-permissionless-blockbuilding/5349
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Flashbots forum post (October 2025) responding to the wiretap.fail, Battering RAM and TEE.fail physical memory-bus interposer attacks on SGX, TDX and SEV, one of which was demonstrated on a lab BuilderNet instance. It states that production BuilderNet is not affected because it runs a permissioned operator set that must deploy in approved cloud environments, and that verification relies on both attestations and IP allowlists. It then sets out the roadmap to permissionless participation through a Proof-of-Cloud system that admits any machine provably hosted in an approved data center.

## Key claims

- The attacks require physical access; "our current systems do not allow operators to run outside vetted cloud environments".
- BuilderNet "is operating in a permissioned model during this phase"; joining requires deploying in approved clouds.
- Forging Azure TPM attestation quotes (mentioned in the paper) is "insufficient to bypass BuilderNet's verification and access controls which rely on both attestations and IP allowlists".
- Path to permissionlessness: a Proof-of-Cloud scheme (DCEA, arXiv 2510.12469) that extends attestations to data centers, on-chain attestation verification (Flashtestations), on-chain TEE governance, and longer-term cryptographic replacements and trustless TEE hardware.

## Evidence quality

Operator statement about its own security model; no independent verification. The described access controls are consistent with the BuilderHub code ([[gh-flashbots-builder-hub]]), which checks measurements against an allowlist and looks builders up by IP.

## Relevance to us

A frank description of what attestation-as-identity needs in practice today: attestation is combined with an operator allowlist and network-location allowlist, so admission is permissioned, and the stated route to permissionless admission is to make "where the hardware is" attestable. For attested agent swarms this means hardware attestation alone does not bound the number of identities an adversary controls or rule out physical tampering; a location or custody proof plus governance is being used as the scarce resource instead. See [[rezabek-2025-proof]] for the Proof-of-Cloud design, [[collective-2024-portrait]] for the identity gaps, and [[eigenphi-2025-buildernet]] for an outside critique of the resulting monoculture.

## Notes from dmarz/sybil-foundations

I opened the primary TEE.fail paper, now catalogued as [[chuang-2025-teefail]]. Its Section 7 describes the BuilderNet demonstration: the authors stood up their own BuilderHub v0.2.1 configured to accept only Azure TDX measurements for the BuilderNet v1.4.0 image, forged an Azure TPM and TDX attestation chain on a machine without TDX using reference quotes from a public BuilderNet node, registered, and retrieved secrets including an Ethereum key that held $200,000 "at the time of writing" and access to order flow. The paper itself notes that BuilderNet required manual Flashbots approval for operators. This is consistent with the post's claim that production, which also checks IP allowlists, was not affected; the paper does not test IP allowlisting. The Proof of Cloud route the post proposes is read in full in the notes on [[rezabek-2025-proof]].
