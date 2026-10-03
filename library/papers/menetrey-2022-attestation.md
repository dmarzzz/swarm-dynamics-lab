---
id: menetrey-2022-attestation
type: paper
title: "Attestation Mechanisms for Trusted Execution Environments Demystified"
authors: ["Jämes Ménétrey", "Christian Göttel", "Anum Khurshid", "Marcelo Pasin", "Pascal Felber", "Valerio Schiavoni", "Shahid Raza"]
year: 2022
venue: "22nd International Conference on Distributed Applications and Interoperable Systems (DAIS 2022), Springer LNCS"
url: https://arxiv.org/pdf/2206.03780
doi: null
arxiv: "2206.03780"
cite: "Ménétrey, J., Göttel, C., Khurshid, A., Pasin, M., Felber, P., Schiavoni, V., & Raza, S. (2022). Attestation Mechanisms for Trusted Execution Environments Demystified. In Distributed Applications and Interoperable Systems (DAIS 2022), Lecture Notes in Computer Science, Springer. doi:10.1007/978-3-031-16092-9_7. arXiv:2206.03780."
topics: [fork-merge-security]
added_by: dmarz/fm-mobile-agents
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: 51  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

A review of how remote attestation works on four TEE families: Intel SGX, Arm TrustZone (A and M profiles), AMD SEV, and RISC-V proposals. Remote attestation lets a verifier establish that it is talking to a specific measured program running inside genuine hardware. The authors conclude that SGX provides a complete built-in attestation protocol for multiple independent enclaves, SEV attests whole VMs against an untrusted hypervisor, TrustZone-A and native RISC-V lack built-in attestation of the trusted environment and rely on community or academic schemes, and TrustZone-M provides a root of trust. Maturity and security differ widely, and attestation remains an industrial challenge. I read the abstract, introduction, conclusion and comparison material.

## Contribution

A compact reference on what current hardware can and cannot prove about remote code, which is the modern answer to the 1990s question "has the host run my agent correctly".

## Key results

- SGX: built-in remote attestation for multiple trusted applications.
- SEV: VM-level attestation against untrusted hypervisors.
- TrustZone-A and plain RISC-V: no native attestation of the trusted environment.
- Attestation proves identity and integrity of measured code at launch, not correctness of later behaviour (a general point in the review).

## Methods and models

Literature and documentation review with a comparison framework; no new measurements.

## Limitations and open questions

Short review; does not cover side-channel breaks of TEEs in depth or attestation of GPU workloads, which matters for model inference.

## Relevance to us

Q3 and Q2: a returning sub-agent could carry an attestation quote that binds its outputs to a measured model, prompt and tool configuration, which closes the "host substituted or edited the agent" path the mobile agent papers worried about ([[farmer-1996-security]], [[yee-1997-sanctuary]]). It does not close the main LLM path: a faithfully executed, attested sub-agent can still be persuaded by the content it reads, because attestation proves what code ran, not that its inputs were benign. Q1: attestation identifies the platform, which works against hiding where a child ran. Related: [[algesheimer-2001-cryptographic]], [[harrison-1995-mobile]].
