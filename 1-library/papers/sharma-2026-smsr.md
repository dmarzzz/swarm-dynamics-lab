---
id: sharma-2026-smsr
type: paper
title: 'SMSR: Certified Defence Against Runtime Memory Poisoning in Persistent LLM Agent Systems'
authors: [Tarun Sharma]
year: 2026
venue: arXiv preprint (submitted to IEEE)
url: https://arxiv.org/abs/2606.12703
doi: null
arxiv: '2606.12703'
cite: 'Sharma, T. (2026). SMSR: Certified Defence Against Runtime Memory Poisoning in Persistent LLM Agent Systems. arXiv preprint arXiv:2606.12703.'
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 5  # Semantic Scholar, 2026-10-03
code: []
---

## Summary

SMSR (Signed Memory with Smoothed Retrieval) defends a persistent agent memory that is written during normal use (the "multi-session memory poisoning" setting) and pairs each of its two components with a proof. Component 1 tags every legitimate write with an HMAC-SHA256 from a server-side signing oracle and drops untagged entries at retrieval. Component 2 handles authenticated adversaries, meaning legitimate users whose entries get signed. It over-fetches a candidate pool of m verified entries, draws T independent random subsets of size s, answers once per subset, has an LLM judge label each answer, and returns the majority verdict. Theorem 1 states that no provenance-free retrieval-time content filter can certify against an adaptive adversary, because fluent on-topic text can always be crafted. Theorem 2 gives a hypergeometric and binomial bound on the probability that the majority verdict is malicious, given at most k adversarial entries in the pool.

## Contribution

This is the first certified bound for live, append-only agent memory. It also names the "Consistent Minority Effect": an adversary wins string-based majority votes because its answers are textually identical while honest answers vary in wording. Voting on verdicts removes the effect.

## Key results

Measured (15 synthetic enterprise-policy scenarios, Claude Haiku 4.5 as agent and judge, 3,150 repeated trials):
- Unsigned injection: ASR falls from 93 to 100% to 0% with Component 1. Fluent "bypass" text fully defeats a keyword, entropy and semantic-anomaly heuristic (100% ASR), which the paper reads as empirical support for Theorem 1.
- Authenticated injection with 20 seed memories, k=1 and T=5: ASR is 8.0% (95% CI 5.8 to 10.9, n=450), below the Theorem 2 bound. Claude Sonnet 4.6 as agent gives the same 8.0%.
- With a small store of 10 seeds, ASR is 37.8% for direct injection and 43.1% for flooding. The flooding CI straddles the bound, so the certificate is tight there.
- On one run, string vote gives 93.3% ASR and verdict vote 13.3%. String vote picks the adversarial answer in 12 of 15 scenarios.
- Query-only end-to-end attack, where the agent writes the poison itself as in [[dong-2025-memory]]: ASR falls from 65.3% to 5.3% (n=150).
- A like-for-like comparison with an A-MemGuard-style consensus baseline [[wei-2025-amemguard]]: 3.8% against SMSR's 8.0%, with overlapping CIs. The A-MemGuard style has no certificate.
- Clean utility is 90% with Component 1 and 85% with both components. Cost is 2T model calls per query.

## Methods and models

The threat model distinguishes an unsigned adversary (database write access, no key) from an authenticated adversary (a normal user with at most k crafted entries). The certificate needs uniform sampling without replacement, which the paper confirms by a Monte Carlo of the sampler, and a bounded k. The author argues k is bounded in practice by per-user write quotas and near-duplicate detection.

## Limitations and open questions

The evaluation uses a single author, synthetic scenarios from one fictional company, and an LLM judge without human labels. The bound becomes vacuous when the adversary holds a large share of the pool. An adversary who learns to fool the judge is not covered. Section VIII extends the scheme to multi-agent pipelines, where upstream agents must sign their outputs, but leaves this as future work.

## Relevance to us

Bears directly on Q2. Component 2 is a k-of-pool threshold with a computable certificate, and it targets exactly a store that keeps being written. That matches a parent merging memories from many returning sub-agents. The paper's own multi-agent note says the signing boundary must extend to each upstream agent. For fork-merge this means a returning sub-agent's writes would be signed. Component 1 then admits poison that the sub-agent itself wrote, so only Component 2 helps. On Q1, random sampling at query time means the adversary cannot guarantee that its entry is consulted, a hiding-by-randomisation effect on the merge side. On Q3, the Consistent Minority Effect is a concrete reason a coordinated attacker who controls several sub-agents with identical payloads beats naive voting. Compare the deterministic partitioning of [[xiang-2024-certifiably]] and the k-principal corroboration of [[louck-2026-securing]].
