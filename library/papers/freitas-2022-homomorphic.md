---
id: freitas-2022-homomorphic
type: paper
title: Homomorphic Sortition -- Secret Leader Election for PoS Blockchains
authors: [Luciano Freitas, Andrei Tonkikh, Adda-Akram Bendoukha, Sara Tucci-Piergiovanni, Renaud Sirdey, Oana Stan, Petr Kuznetsov]
year: 2022
venue: arXiv preprint
url: https://arxiv.org/abs/2206.11519
doi: null
arxiv: '2206.11519'
cite: Freitas, L., Tonkikh, A., Bendoukha, A.-A., Tucci-Piergiovanni, S., Sirdey, R., Stan, O., & Kuznetsov, P. (2022). Homomorphic Sortition -- Secret Leader Election for PoS Blockchains. arXiv:2206.11519.
topics: [fork-merge-security, sync-consensus]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 5 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Homomorphic Sortition is an SSLE protocol built on threshold fully homomorphic encryption. It is presented as the first asynchronous SSLE with non-expiring registration, so elected parties need not re-register, which makes it usable with partially synchronous leader-based consensus. It supports arbitrary stake weights without registering a user once per coin, can run off-chain after setup, and generalises SSLE to Secret Leader Permutation (SLP), which outputs a sequence of non-repeating hidden leaders.

## Contribution

Removes the expiring-registration and synchrony assumptions of earlier SSLE schemes and adds the SLP generalisation.

## Key results

- Asynchronous SSLE with non-expiring registration (claimed in abstract).
- Stake-weighted election without multiple registrations; highly parallelisable.
- Secret Leader Permutation: choose how many non-repeating hidden leaders to output in a sequence.

## Methods and models

Threshold FHE over encrypted tickets and stake prefix sums (as summarised in the abstract and in [[burianova-2025-secret]]); not read beyond the abstract.

## Limitations and open questions

[[burianova-2025-secret]] measured its computation as impractical at Ethereum scale with current FHE libraries.

## Relevance to us

Q1. SLP is the right primitive for a parent that wants to schedule a hidden order of k returning sub-agents in advance without anyone, including the sub-agents not yet called, knowing the order; non-expiring registration fits sub-agents that stay out for long and unpredictable periods. Q2: the threshold-decryption step means hiding holds only while fewer than the threshold of key holders collude, which is itself a k-of-n assumption. Compare [[boneh-2020-single]] and [[ethresear-2022-whisk]].
