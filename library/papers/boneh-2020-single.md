---
id: boneh-2020-single
type: paper
title: Single Secret Leader Election
authors: [Dan Boneh, Saba Eskandarian, Lucjan Hanzlik, Nicola Greco]
year: 2020
venue: Proceedings of the 2nd ACM Conference on Advances in Financial Technologies (AFT 2020)
url: https://eprint.iacr.org/2020/025.pdf
doi: 10.1145/3419614.3423258
arxiv: null
cite: Boneh, D., Eskandarian, S., Hanzlik, L., & Greco, N. (2020). Single secret leader election. Proceedings of the 2nd ACM Conference on Advances in Financial Technologies (AFT '20), 12-24. Also Cryptology ePrint Archive, Paper 2020/025.
topics: [fork-merge-security, sybil-resistance, sync-consensus]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 49 (Crossref, 2026-10-03); 74 citing papers listed by Semantic Scholar
code: []
---

## Summary

The paper defines Single Secret Leader Election (SSLE): a group repeatedly elects exactly one leader such that only the leader knows it was chosen until it reveals itself with a proof. It formalises uniqueness, fairness and unpredictability (an adversary who does not control the winner can do no better than guess among honest users) and notes these imply the best possible DoS robustness: attacking a random alpha fraction disrupts an election with probability alpha. It gives three constructions: an ideal one from indistinguishability obfuscation; one from threshold FHE with an election circuit of multiplicative depth as low as 10 for N = 2^16, which works while any t parties are online; and a practical one from DDH plus shuffling, where each user posts a re-randomisable commitment (g^r, g^(k r)), registrants shuffle and re-randomise one of sqrt(N) buckets, and the beacon picks a row.

## Contribution

First formal definition of SSLE and the first constructions with exactly one hidden leader, giving a precise security-cost menu for hiding who acts next.

## Key results

- Robustness bound: with uniqueness, fairness and unpredictability, a DoS on an alpha fraction succeeds with probability at most alpha; this is optimal.
- TFHE scheme is t-threshold unique, unpredictable and fair (security holds while fewer than t parties are corrupted); the paper flags a long-run attack where an adversary buys key shares from users who leave until it holds t, mitigated by periodic re-sharing.
- DDH shuffle scheme with deterministic buckets is only 1/(sqrt(N) - c) unpredictable with c corrupted users, so an attacker needs O(sqrt(N)) corruptions to break hiding; random bucket assignment pushes this to O(N) corruptions at the cost of a one-election registration delay.
- Prior VRF-style secret elections can produce several candidate leaders, leading to duplicated work, withheld-winner attacks and forks; SSLE avoids these.
- Attacks named and defended: duplication (two users registering the same secret), modification of revealed secrets, re-randomising someone else's commitment to bias fairness.

## Methods and models

Game-based security definitions (uniqueness, unpredictability, fairness experiments), constructions in the random oracle model, proofs in appendices (I read the main text and constructions, not every appendix proof).

## Limitations and open questions

The practical DDH scheme trades hiding strength for cost; the TFHE scheme needs a threshold of online key holders and setup; obfuscation is not practical. Open problem stated: a scheme with both optimal security and performance.

## Relevance to us

Q1 and Q2 together. SSLE is the closest formal object to "the parent picks which sub-agent returns, and nobody, including the other sub-agents, learns which until it returns with a proof". Mapping: sub-agents register re-randomisable commitments before leaving; a public beacon picks the row that will be merged; only the chosen sub-agent can prove it was chosen, so an attacker cannot target the returning part in advance and a corrupted non-chosen part cannot impersonate it. The multiple-leader extension (an ordered list of k hidden leaders) is the natural form for "merge k of n". The unpredictability bounds give a quantitative answer to "how many parts must the attacker corrupt before hiding fails": O(sqrt(N)) for the cheap scheme, O(N) with random buckets, below a threshold t for the TFHE scheme. Empirical follow-up: [[burianova-2025-secret]]; deployment design: [[ethresear-2022-whisk]]; FHE variant: [[freitas-2022-homomorphic]]; what hiding the leader costs elsewhere: [[azouvi-2021-private]]; network-layer leaks that bypass it: [[heimbach-2024-deanonymizing]].
