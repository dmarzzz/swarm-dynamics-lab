---
id: chuang-2025-teefail
type: paper
title: "TEE.fail: Breaking Trusted Execution Environments via DDR5 Memory Bus Interposition"
authors: [Jalen Chuang, Alex Seto, Nicolas Berrios, Stephan van Schaik, Christina Garman, Daniel Genkin]
year: 2025
venue: Paper PDF on the authors' project site tee.fail (disclosed 28 October 2025); not checked against a proceedings version
url: https://tee.fail/files/paper.pdf
doi: null
arxiv: null
cite: "Chuang, J., Seto, A., Berrios, N., van Schaik, S., Garman, C., & Genkin, D. (2025). TEE.fail: Breaking Trusted Execution Environments via DDR5 Memory Bus Interposition. Paper available at https://tee.fail/files/paper.pdf."
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

The authors build a DDR5 memory-bus interposer from second-hand parts for under $1,000 (logic-analyzer probe under $500) and use it with the deterministic AES-XTS memory encryption of Intel SGX/TDX and AMD SEV-SNP to recover secrets from machines in fully trusted "UpToDate" attestation status. On a 5th-generation Xeon they extract the Provisioning Certification Key (PCK) from Intel's Provisioning Certification Enclave in about 2 minutes of ciphertext mapping plus 13 minutes of tracing, then sign their own attestation keys and forge SGX and TDX quotes that Intel's DCAP Quote Verification Library accepts. Case studies: a BuilderNet node run outside TDX that registers with BuilderHub and receives secrets and order flow; dstack (Phala) SDK calls forged outside TDX; NVIDIA Confidential Computing attestations relayed from a rented H100; a Secret Network master key extracted directly; and ECDSA keys pulled from OpenSSL inside SEV-SNP with ciphertext hiding (about 1 hour of recording). I read the introduction, background, Sections 6.3, 7, 8 and 11, and skimmed the hardware and enclave-control sections.

## Contribution

First memory-interposition attack on DDR5 server TEEs and first end-to-end PCK extraction on a TDX machine in UpToDate status. It moves physical attacks on server TEEs from "lab equipment" to hobbyist budgets and shows the practical gap between vendor threat models (physical attacks out of scope) and permissionless deployments.

## Key results

- Cost: entire DDR5 snooping setup under $1,000; prior Membuster setup cited at $170,000.
- PCK recovery about 15 minutes in total; forged quotes verify under Intel DCAP.
- BuilderNet (Section 7): using a BuilderHub v0.2.1 instance configured for Azure TDX and BuilderNet image v1.4.0, an attacker machine without TDX registered as a node and obtained configuration secrets, an Ethereum key that held $200,000 at the time of writing, a relay signing key and access to order flow. The paper notes BuilderNet then required manual approval from Flashbots for operators.
- Attestation relay: NVIDIA does not bind an H100 attestation to a specific VM, so the authors passed CC attestation by fetching it on demand from a rented, genuine H100.
- Mitigations discussed: avoid deterministic encryption (Intel says a microcode fix is impossible for current CPUs), add per-block entropy, restrict deployment to reputable clouds or use MPC, and add location verification or CPU allowlisting to attestation.

## Methods and models

Custom DDR5 RDIMM interposer and a second-hand logic analyzer observing one channel; reverse-engineered physical-address-to-DIMM mapping, kernel modifications to place target pages, cache flushing and a page-granular control channel to single out ECDSA nonce reads in the PCE. Attacks run on the authors' own machines and official testnets; coordinated disclosure to Intel (April 2025), NVIDIA (June 2025), AMD (August 2025) and affected deployments.

## Limitations and open questions

Requires physical custody of the machine; the authors flag that faster interposers will likely remove the bus-speed barrier. Venue status beyond the project-site PDF was not checked. Production BuilderNet's response that IP allowlists and approved clouds block the attack is in [[collective-2025-why]].

## Relevance to us

For "one agent equals one attested enclave", this is the cost of forgery: one interposer and one owned Xeon yield a PCK that signs arbitrarily many valid quotes, so the number of attested identities stops being bounded by the number of chips. The binding that fails is chassis plus code measurement; what survives is binding to an operator who is trusted to hold the chassis, which is the route taken by [[rezabek-2025-proof]] and BuilderNet's allowlists [[gh-flashbots-builder-hub]]. The GPU relay result is the renting attack in hardware form: a genuine attestation from a rented machine was presented as the attacker's own, which parallels key rental in [[austgen-2024-liquefaction]]. Earlier DDR4 SGX attack: [[seto-2025-wiretap]]. Secondhand summary of both: [[ethresearch-2026-physical]].
