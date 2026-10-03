---
id: rezabek-2025-proof
type: paper
title: "Proof of Cloud: Data Center Execution Assurance for Confidential VMs"
authors: [Filip Rezabek, Moe Mahhouk, Andrew Miller, Quintus Kilbourn, Georg Carle, Jonathan Passerat-Palmbach]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2510.12469
doi: 10.48550/arXiv.2510.12469
arxiv: "2510.12469"
cite: "Rezabek, F., Mahhouk, M., Miller, A., Kilbourn, Q., Carle, G., & Passerat-Palmbach, J. (2025). Proof of Cloud: Data Center Execution Assurance for Confidential VMs. arXiv preprint arXiv:2510.12469."
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Proposes Data Center Execution Assurance (DCEA), which produces a cryptographic "Proof of Cloud" that a confidential VM runs on hardware inside a trusted data center. Existing CVM attestations certify what code runs, not where, which allows proxy attacks that combine valid attestations across machines. DCEA binds the TEE attestation to platform TPM evidence so that the CVM execution, vTPM quotes and platform provenance come from the same physical chassis. It is proven in the UC model (AGATE framework) and implemented on Google Cloud bare-metal Intel TDX with Intel TXT.

## Contribution

Adds a location and custody dimension to TEE attestation by combining two independent roots of trust (the TEE manufacturer and the infrastructure provider), and names a mix-and-match proxy attack that existing attestation does not stop. Flashbots cites it as the basis of the Proof-of-Cloud route to permissionless BuilderNet ([[collective-2025-why]]).

## Key results

- Threat: commercial TEEs exclude active hardware tampering (memory interposers, physical side channels), yet attestation gives no evidence that the machine sits in a data center where such attacks are impractical.
- Attack: relay or proxy attacks, including a "novel mix-and-match proxy attack", where valid attestations from different machines are combined to falsely attest trusted execution.
- Defence: cross-link runtime TEE measurements with the vTPM-measured boot state so all evidence originates from one chassis.
- Proved to emulate an ideal location-aware TEE under a malicious host software stack; implementation overheads reported as practical (figures not read).

## Methods and models

UC-style security proof in the AGATE framework; prototype on GCP bare-metal TDX with TXT. Only the abstract was read.

## Limitations and open questions

Depends on the infrastructure provider as a second root of trust, so admission becomes "machines in approved data centers", which is a permissioned set. Overheads and deployment details were not checked.

## Relevance to us

If attested hardware is used as an identity for agents or nodes, two failure modes matter: one physical machine presenting as many, and attestations from one machine being replayed or combined to vouch for another. DCEA addresses the second by binding identity to a physical chassis in a known location, which makes the scarce resource "a machine in a vetted data center". That is a strong but centralising Sybil bound; it trades permissionless entry for physical scarcity, the same trade-off seen in [[collective-2025-why]] and [[collective-2024-portrait]]. Compare with the physical-presence and location-proof approaches catalogued by other lanes, such as [[ethresearch-2026-physical]].
