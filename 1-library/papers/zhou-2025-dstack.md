---
id: zhou-2025-dstack
type: paper
title: "Dstack: A Zero Trust Framework for Confidential Containers"
authors: [Shunfan Zhou, Kevin Wang, Hang Yin]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2509.11555
doi: 10.48550/arXiv.2509.11555
arxiv: "2509.11555"
cite: "Zhou, S., Wang, K., & Yin, H. (2025). Dstack: A Zero Trust Framework for Confidential Containers. arXiv preprint arXiv:2509.11555."
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Phala Network's design paper for dstack, the confidential-VM framework on Intel TDX that hosts Docker containers and that the TEE_HEE agent [[malhotra-2024-setting]] ran on. Three components: dstack-OS (minimal measured image; RTMR0-3 record firmware, kernel, root filesystem and the app's compose file and images), dstack-KMS (a P2P network of TEE nodes that derives keys from a root key, by simple duplication or Shamir threshold sharing, and supports root-key rotation), and dstack-Gateway/Ingress (TEE-controlled TLS certificates and domains). On-chain KmsAuth and per-app AppAuth contracts list allowed code hashes and "authorized TEE instance identities", and KMS releases app secrets only to instances whose quote matches. I read the introduction, Section 3 (KMS, OS, code management), the security analysis, discussion and conclusion; the gateway details and evaluation were skimmed.

## Contribution

Decouples application keys from the hardware sealing key so that an app can migrate between TEE machines and vendors, and puts code upgrades under smart-contract governance. The authors frame this as answering censorship resistance and "assume breach".

## Key results

- Application identity is the app identifier, "calculated as the hash of the application's code and configuration"; the app CA key, environment key and ECDSA signing key are derived from the KMS root key and that identifier, so every instance running the same app gets the same keys. Only the disk-encryption key also mixes in an instance identifier.
- Security analysis states "Hardware-backed TDX Quotes effectively prevent attestation spoofing attempts."
- Detection of TEE exploitation is acknowledged as largely out of scope.
- No quantitative evaluation figures were read.

## Methods and models

System design with on-chain governance (multisig or DAO AppAuth), reproducible builds and an in-TEE build pipeline; key derivation via HKDF.

## Limitations and open questions

The quote-spoofing claim is contradicted by [[chuang-2025-teefail]], which forged dstack quotes outside TDX after extracting a PCK. The paper does not discuss how many instances of one app may run, or how a verifier would learn that number.

## Relevance to us

dstack answers "what is the agent" with a code measurement, not a machine: identity is bound to hash(code, config) and the KMS deliberately gives every instance the same signing key. That is good for portability and for proving no human holds the key, but it means an attested dstack identity says nothing about count. One principal can run N replicas of the same app under one identity, or N trivially different apps (different config bytes) under N identities, and the cost per extra identity is one more CVM rental. For a swarm, dstack attestation can certify behaviour (which code) but a Sybil bound has to come from elsewhere: an instance allowlist in AppAuth, a custody proof [[rezabek-2025-proof]], stake, or a per-chassis registry. Compare the key-per-enclave design in [[gh-flashbots-flashtestations]] and the encumbrance view in [[kelkar-2024-complete]].
