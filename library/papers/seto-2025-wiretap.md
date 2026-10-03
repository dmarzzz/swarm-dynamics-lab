---
id: seto-2025-wiretap
type: paper
title: "WireTap: Breaking Server SGX via DRAM Bus Interposition"
authors: [Alex Seto, Oytun Kuday Duran, Samy Amer, Jalen Chuang, Stephan van Schaik, Daniel Genkin, Christina Garman]
year: 2025
venue: ACM CCS 2025 (Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, Taipei)
url: https://wiretap.fail/files/wiretap.pdf
doi: 10.1145/3719027.3765204
arxiv: null
cite: "Seto, A., Duran, O. K., Amer, S., Chuang, J., van Schaik, S., Genkin, D., & Garman, C. (2025). WireTap: Breaking Server SGX via DRAM Bus Interposition. In Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security (CCS '25), Taipei, Taiwan. ACM. https://doi.org/10.1145/3719027.3765204"
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A DDR4 memory-bus interposer built for under $1,000 from second-hand parts (DIMM metadata modified to slow the bus to 1333 MT/s, a Pentium III-era logic analyzer) exploits the deterministic AES-XTS encryption of scalable server SGX to extract an SGX DCAP attestation key from Intel's Quoting Enclave on a Xeon in fully trusted status, in about 45 minutes. With that key the authors forge quotes accepted by Intel's verification library and attack SGX-based blockchains with a combined market cap over $135M: they extract contract-state keys from Phala and Secret Network, and on Crust they register a modified enclave and fake proofs of storage, collecting storage rewards "without ever actually storing files". I read the abstract, introduction, the Crust case study, mitigations and conclusion from the PDF and the project page; the Phala and Secret sections were skimmed.

## Contribution

Shows that physical SGX attacks are within hobbyist budgets and that permissionless SGX networks, which admit any machine with a trusted attestation status, put secrets in adversarial hands. Precursor to the DDR5/TDX work in [[chuang-2025-teefail]].

## Key results

- Cost under $1,000 versus $170,000 cited for prior interposition setups.
- Attestation key extracted in about 45 minutes, bottlenecked by logic-analyzer I/O.
- Crust: node identity is an ECDSA key generated in an enclave whose quote is checked once at registration against an mrenclave allowlist; with a forged quote an attacker can run a modified enclave or register a key generated outside it and forge storage proofs at will.
- Mitigations: higher bus speeds raise the bar but do not fix it; restrict nodes to reputable cloud operators or accept occasional breaches and use MPC; avoid single master keys provisioned to all enclaves; AEX-Notify helps but is incomplete.

## Methods and models

DIMM interposer plus logic analyzer on one of eight DIMMs, physical-address mapping reverse engineered, SGX driver modified to place target pages, cache flushing synchronised by a control channel, ciphertext-equality oracle on ECDSA scalar multiplication to recover the nonce. Experiments on the authors' hardware and local testnets; coordinated disclosure to Intel and affected projects.

## Limitations and open questions

Needs physical access and DDR4 (TDX on DDR5 was left to future work, then done in [[chuang-2025-teefail]]). The paper does not measure detection by operators.

## Relevance to us

Crust is a clean case of TEE attestation used as a Sybil and work-proof gate: one registered enclave identity per storage node, rewards per proof. Once one attestation key is extracted, an attacker can mint many registered "nodes" and claim rewards for work never done, so the scarce resource behind the identity collapses from "a genuine enclave doing work" to "one compromised CPU". For agent swarms that admit members on attestation alone, the authors' own recommendation (admit only machines held by reputable operators) is a custody-based Sybil bound, the same move as [[rezabek-2025-proof]] and [[collective-2025-why]]. Secondhand summary of the figures: [[ethresearch-2026-physical]].
