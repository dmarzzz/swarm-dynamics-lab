---
id: collective-2024-portrait
type: blog
title: "Portrait of a TEE: applications and identity"
authors: [mateusz]
year: 2024
url: https://collective.flashbots.net/t/portrait-of-a-tee-applications-and-identity/4142
site: collective.flashbots.net (Flashbots forum)
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

Forum essay (topic created November 2024, post last edited January 2025) by the forum user mateusz on what a trusted execution environment instance can and cannot be identified by. Attestations can pin the specific CPU (via the encrypted PPID), the booted image (measurements) and runtime extensions (RTMR3), but cannot tell apart two instances on one CPU, cannot distinguish owners of identical workloads, and cannot by themselves identify an "application" that spans many instances and changing images. The author argues that application identity has to come from external governance, most naturally a smart contract that allowlists measurements.

## Key claims

- Identifiable from an attestation: the physical CPU (encrypted PPID), the image through measured boot, post-boot configuration through runtime measurements; user data in the quote is "easily faked".
- Flashbots was not then using the PPID to identify the infrastructure operator, and the author says it should; a signed list of PPIDs published by operators would approximate a "proof of cloud".
- Missing: distinguishing instances on the same CPU ("if there's two instances on the same CPU and one is misbehaving, no one would know"), distinguishing workload owners, and mapping instances to applications.
- Using measurements as key-derivation domain separators can be catastrophic (for TEE searching it would let any instance with the same image read proprietary logic) or useful (all same-config instances can share sealed data).
- Proposal: a smart contract that maps expected measurements to an application handle, with transparent, enforceable governance of upgrades.

## Evidence quality

Engineering opinion from a practitioner working on BuilderNet and related TEE services; technically specific, no experiments.

## Relevance to us

Attestation is often proposed as a Sybil defence for agents ("only genuine, attested agents may join"). This post lists the gaps: attestation proves code and sometimes a CPU, not a distinct operator or a distinct instance, so one operator can run many attested instances, and the binding from attested instance to accountable entity is a governance decision outside the hardware. For attested agent swarms the identity unit has to be chosen explicitly (CPU, operator, or governed application), and only the CPU-level identifier is scarce in a physical sense. Follow-ups: DCEA proof of cloud ([[rezabek-2025-proof]]), BuilderNet's permissioned operator set ([[collective-2025-why]]), and the provisioning service that implements measurement allowlists ([[gh-flashbots-builder-hub]]).
