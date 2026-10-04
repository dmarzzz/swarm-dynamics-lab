---
id: miller-2024-sirrah
type: blog
title: "Sirrah: Speedrunning a TEE Coprocessor"
authors: [Andrew Miller, Mateusz Morusiewicz, Frieder Paape]
year: 2024
url: https://writings.flashbots.net/suave-tee-coprocessor
site: writings.flashbots.net (Flashbots)
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Flashbots post (25 January 2024) building a minimal TEE coprocessor for SUAVE's Andromeda line: a fork of REVM running under Gramine-SGX in nodes called Kettles, with extra precompiles that expose enclave randomness, volatile and sealed storage, and remote attestation to Solidity. A contract bootstraps a key in one Kettle, posts the public key with an SGX quote, and an on-chain DCAP verifier (Automata) installs it once; users encrypt bids to that key and any Kettle can decrypt and post an attested second-price result. A Helios light client inside the enclave checks chain state. The improved key manager shares the bootstrapped key with other SGX nodes that register, verifying the expensive attestation once per node and then accepting cheap signatures from the registered address. Attestations are domain-separated by contract address so contracts cannot spoof each other.

## Key claims

- Most of the trusted code is Solidity: about 139 lines for the auction, 61 for Andromeda.sol, 185 lines of Rust for the attestation precompiles, about 1,000 lines for RPC and light-client plumbing.
- Sealing keys are bound to the particular CPU and enclave.
- Threat model is an "analysis-oriented Kettle operator" running everything except the enclave; side channels (memory size, SLOAD/SSTORE access patterns, SGX-Step) are acknowledged and documented through a redacted leakage trace rather than mitigated.
- Key rotation and governance of acceptable mrenclaves are left open.

## Evidence quality

Design and code walkthrough with a live testnet demo (Rigil timelock contract); no security evaluation. I read the design, key bootstrap, attestation, key-manager and security sections, and skipped the code listings in detail.

## Relevance to us

Sirrah shows the registry pattern that most TEE networks, including later Flashtestations [[gh-flashbots-flashtestations]], use for identity: attest once at registration, then map an address to that attestation. The Sybil question is what the registry is keyed on. Here it is the node address bound to an mrenclave, so any machine that can produce a valid quote can add another node; the scarce resource is "a CPU that attests", which [[seto-2025-wiretap]] and [[chuang-2025-teefail]] show can be faked. A shared application key across all nodes also means nodes are interchangeable, which helps liveness but removes any per-node identity at the application layer. Related SUAVE framing: [[quintus-2023-problems]].
