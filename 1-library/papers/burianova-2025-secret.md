---
id: burianova-2025-secret
type: paper
title: 'Secret Leader Election in Ethereum PoS: An Empirical Security Analysis of Whisk and Homomorphic Sortition under DoS on the Leader and Censorship Attacks'
authors: [Tereza Burianova, Martin Peresini, Ivan Homoliak]
year: 2025
venue: arXiv preprint (a version appears at IEEE ICBC 2026 per OpenAlex)
url: https://arxiv.org/abs/2509.24955
doi: null
arxiv: '2509.24955'
cite: 'Burianová, T., Perešíni, M., & Homoliak, I. (2025). Secret Leader Election in Ethereum PoS: An Empirical Security Analysis of Whisk and Homomorphic Sortition under DoS on the Leader and Censorship Attacks. arXiv:2509.24955.'
topics: [fork-merge-security, sybil-resistance, sync-consensus]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: 4 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

The authors build a Rust simulator of Ethereum's proposer pipeline and compare the status quo (proposers known two epochs ahead), Whisk (shuffle-based SSLE) and homomorphic sortition (threshold-FHE SSLE) under targeted DoS, an "advanced" DoS that hits a chosen 10% of validators blindly, and censorship of a victim group. With 80% of validators linkable to IPs, targeted DoS without protection caused 64% missed blocks; both SSLE schemes reduced it to near 0%. The advanced DoS was worse under Whisk (28% missed versus 6-8% otherwise) because Whisk's 16,384-candidate list is public before shuffling, narrowing the target set. Neither scheme stopped persistent attacks on a whole victim group (69-71% of victims still blocked). Whisk processing was about 20-30x the status quo but within slot time; homomorphic sortition was impractically slow.

## Contribution

First side-by-side simulation of SSLE designs under coordinated adversaries, showing that hiding the single leader does not protect a known candidate pool.

## Key results

- Targeted DoS on the known leader: 64% blocks missed, 67% of proposers affected with no protection; near 0% with Whisk or homomorphic sortition.
- Advanced DoS on candidates: 28% missed under Whisk versus 6-8% under status quo or sortition (single illustrative run plus 5-seed aggregates for Whisk and baseline; sortition run once due to cost).
- Censorship of a 10% victim group: system-wide missed slots only 6-7%, but 69-71% of victims prevented from proposing; SSLE helps only against the targeted variant.
- Cost: Whisk 20-30x slower block and epoch processing than status quo, still feasible; homomorphic sortition grows steeply with validator count.

## Methods and models

Simplified synchronous Ethereum consensus (no network layer, no fork choice), 1,000 validators for Whisk and 100 for sortition, 6 epochs, attacker targeting 10% of validators, 20% of validators with extra network protection. Whisk follows EIP-7441 with Curdleproofs; sortition uses TFHE-rs with a simplified PRINCE cipher and no threshold.

## Limitations and open questions

Small validator sets, few seeds (one run for sortition), abstracted network. The authors call SSLE "a layer of deterrence rather than a foolproof defence" and ask for network-layer anonymisation on top.

## Relevance to us

Q1, with measured numbers. The headline lesson transfers: hiding which single part returns works against an attacker who must aim at the returner, but if the set of possible returners is public (Whisk's candidate list), an attacker with enough budget attacks the whole set, and hiding can make things worse by shrinking it. For a fork-merge agent this argues for keeping the candidate set of possible merge partners as large as the whole population, or hidden too. Q2: the coordinated-group results say that once the adversary can hit a fixed fraction of parts persistently, hiding gives no protection and only a threshold rule can help. Theory: [[boneh-2020-single]]; design: [[ethresear-2022-whisk]]; sortition protocol: [[freitas-2022-homomorphic]]; network-layer deanonymisation that removes the 80% linkability assumption's guesswork: [[heimbach-2024-deanonymizing]].
