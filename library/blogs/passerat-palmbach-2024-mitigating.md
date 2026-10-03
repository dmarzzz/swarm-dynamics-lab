---
id: passerat-palmbach-2024-mitigating
type: blog
title: Mitigating MEV with FHE - Blind Arbitrage on Ethereum
authors:
- Jonathan Passerat-Palmbach
year: 2024
url: https://writings.flashbots.net/blind-arbitrage-fhe
site: Flashbots Writings
topics:
- sybil-resistance
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 2
---

## Summary

This prototype lets a searcher calculate an arbitrage backrun over an encrypted user transaction without learning its details. A trusted builder decrypts the resulting bundle. The FHE implementation reduces interactive bandwidth relative to earlier secret-sharing work, but slow integer arithmetic and missing encrypted ECDSA signing make it unsuitable for deployment.

## Key claims

- The amount calculation took about 1,025 seconds, or 846 seconds with AVX512, for the reported 128-bit workload on a 128-core Xeon Platinum 8375C.
- Server key size was 105 MB; transaction and strategy ciphertexts were 47 MB and 20 MB respectively.
- The builder is trusted and shares a secret key securely with the user; threshold-FHE among validators is explicitly out of scope.

## Evidence quality

First-party feasibility study with detailed protocol assumptions, runtime table, hardware, and implementation limitations. The code was not executed. The 128-bit runtime column denotes arithmetic width, while the default cryptographic parameters separately target at least 128-bit security.

## Relevance to us

Background for adversarial agent markets and programmable information access. Confidentiality constrains what a searcher can exploit, but this is not identity authentication or a Sybil defense. Related selective-disclosure mechanism: [[smedley-2023-searching]]. No LLM swarm experiment is conducted.
