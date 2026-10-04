---
id: hashmi-2010-towards
type: paper
title: "Towards Sybil Resistant Authentication in Mobile Ad Hoc Networks"
authors: [Saorsh Hashmi, John Brooke]
year: 2010
venue: 2010 Fourth International Conference on Emerging Security Information, Systems and Technologies (SECURWARE), Venice, pp. 17-24
url: https://ieeexplore.ieee.org/document/5631803
doi: 10.1109/securware.2010.11
arxiv: null
cite: "Hashmi, S., & Brooke, J. (2010). Towards Sybil Resistant Authentication in Mobile Ad Hoc Networks. In 2010 Fourth International Conference on Emerging Security Information, Systems and Technologies (SECURWARE), pp. 17-24. IEEE. https://doi.org/10.1109/SECURWARE.2010.11"
topics: [sybil-resistance]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: "12 (Crossref, 2026-10-03)"
code: []
---

## Summary

Targets Sybil attacks in MANETs, where reputation-based misbehaviour detection needs one unique, unchangeable identity per node and existing authentication either relies on out-of-band physical contact or a trusted third party (TTP) issuing identities. The proposal binds identity to the hardware ID of the device: a mobile "authentication agent" (code shipped to the node being authenticated) reads and verifies the device's hardware identifier, a defence model protects that agent from static and dynamic tampering by a malicious host, and a TTP signs the agent so the authenticatee can trust that it only performs its intended function. The TTP's involvement is thus limited to code signing rather than per-node identity issuance. The authors argue this raises the Sybil bar to either defeating the agent-protection mechanisms or acquiring many physical devices with distinct hardware IDs. Abstract only (IEEE paywalled); the agent-protection techniques (presumably obfuscation / tamper-detection of mobile code) and any evaluation are not visible.

## Contribution

A device-bound identity scheme for MANETs using TTP-signed mobile agents to attest hardware IDs, trading full identity issuance for code signing.

## Key results

- Sybil cost shifted to hardware acquisition or agent subversion (abstract; no quantitative evaluation visible).

## Methods and models

Mobile-agent authentication, hardware-ID attestation, TTP code signing, threat model of malicious hosts; details not read.

## Limitations and open questions

Abstract-level read. Mobile code running on an adversary's device cannot in general be protected from that device (the classic malicious-host problem), so the security reduces to the strength of the agent-protection tricks; hardware IDs are also spoofable at the driver level. Low-profile venue.

## Relevance to us

A reminder that "bind identity to hardware" without a trusted execution environment collapses to the malicious-host problem, which is the same objection to trusting agent self-reports about their runtime. Properly hardware-rooted versions are the TPM/SE-based credentials in [[hanzlik-2021-with]]; resource-based alternatives in [[urdaneta-2011-survey]]; MANET/VANET trust context [[zhang-2011-survey]]. Root: [[douceur-2002-sybil]].
