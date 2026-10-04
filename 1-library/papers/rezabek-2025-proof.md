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

## Notes from dmarz/sybil-foundations

I read the full arXiv v2 (dated 3 March 2026) on 2026-10-03; the entry above was written from the abstract. Points that bear on Sybil resistance:

- Section 7.2, "Offering Unique Identities in Multitenancy", is the Sybil discussion. A single vTPM certificate chain and attestation key (AK) can be shared by several CVMs on one host, which "weakens the uniqueness guarantees of attestation and may complicate the detection of identity cloning". The authors propose a global or domain-scoped registry of AK public keys (Certificate Transparency or a public blockchain) so verifiers can detect duplicate AKs; in single-tenant deployments the registry should show exactly one AK and EK per hardware node.
- Section 7 ("Role of PCR values") states that PCR/RTMR values are software-stack consistency checks, not machine identifiers: two platforms with identical firmware produce identical PCR 0-7. Machine uniqueness comes from the provider-issued EK certificate chain plus the TDX quote's hardware ID. "The EKC answers which machine, while the PCR/RTMR match answers on the same machine."
- The quote carries the PPID, "unique to the CPU", and the authors suggest providers could publish PPID lists with Merkle set-membership proofs so a CVM can prove it runs in an approved data center without revealing which one. They also contrast DCEA with Intel Platform Ownership Endorsement (POE), which binds hardware to an owning organisation.
- The threat model is a software-only host adversary without physical access; the six attacks A1-A6 are relay ("mix-and-match"), quote forgery, measurement inconsistency, channel interception, identity substitution (reusing EK certificates or substituting the AK) and component compromise. The physical PCK extraction in [[chuang-2025-teefail]] is outside this model; DCEA's answer to it is the assumption that the provider will not attack its own chassis.
- Prototype on GCP bare-metal TDX with Intel TXT sealing the AK to PCRs 17-18; overhead figures are in their Fig. 8 and Appendix B, which I did not transcribe.

For agent identity this paper gives the clearest statement of what to bind to: a chassis identity certified by a provider, cross-checked against the running code, plus a duplicate-detection registry. The cost of forging becomes "subvert a cloud provider's TPM chain", and the cost of a legitimate extra identity is one more bare-metal rental, so it bounds Sybils by rented hardware, not by persons or principals. Related: [[gh-flashbots-flashtestations]], [[zhou-2025-dstack]], [[seto-2025-wiretap]].
