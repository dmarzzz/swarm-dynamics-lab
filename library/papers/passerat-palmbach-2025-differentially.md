---
id: passerat-palmbach-2025-differentially
type: paper
title: "Differentially Private aggregate hints in mev-share"
authors: [Jonathan Passerat-Palmbach, Sarisht Wadhwa]
year: 2025
venue: arXiv preprint (cs.CR)
url: https://arxiv.org/abs/2508.14284
doi: 10.48550/arXiv.2508.14284
arxiv: "2508.14284"
cite: "Passerat-Palmbach, J., & Wadhwa, S. (2025). Differentially Private aggregate hints in mev-share. arXiv preprint arXiv:2508.14284."
topics: [sybil-resistance]
added_by: dmarz/sybil-flashbots
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Paper by a Flashbots researcher and a Duke University researcher proposing differentially private aggregate hints for MEV-Share. Instead of per-transaction hints, a trusted curator (the matchmaker) releases noisy aggregate statistics (countOf, sumOf with Laplace noise) over pending user transactions, so users can quantify privacy loss and ask for rebates accordingly. It includes a threat model in which searchers inject their own transactions to infer others' data or degrade hint quality, and proposes random subsampling before aggregation as the Sybil defence.

## Contribution

Applies the trusted-curator model of differential privacy to MEV order-flow hints and makes the Sybil threat explicit: in a permissionless matchmaker, rate-limiting per user does not work because an adversary can appear as many users.

## Key results

- Attack cost: an attacking searcher can submit signed transactions with low fees and low MEV so that most are never included yet still count toward aggregates; the authors say this cost can be assumed close to 0 under ideal conditions.
- "Typical Trusted Curator deployment would mitigate the threat model ... by rate-limiting users submitting an abnormal number of transactions. However, in a permissionless system, the adversary can mount sybil attacks and spread its capital to appear as many different users."
- Raising mechanism sensitivity to absorb malicious inputs degrades utility without discouraging attacks.
- Proposed defence: the curator samples a random subset of received transactions and applies the DP mechanism only to the subsample, so an attacker cannot be sure its injected samples are included. By privacy amplification by subsampling, with sampling rate q, epsilon' = log(1 + q(e^epsilon - 1)) = O(q epsilon) and delta' = q delta, so the Sybil mitigation also strengthens privacy.

## Methods and models

Analysis of two searcher strategies on MEV-Share, a DP mechanism design in the trusted curator model, sensitivity analysis for count and sum queries, and the subsampling lemma. No deployment data. Read: abstract, threat model, attack mitigation, aggregate queries, discussion and conclusion.

## Limitations and open questions

The subsampling defence reduces an attacker's certainty and influence but does not bound the number of Sybil identities; with enough injected transactions an attacker still shifts sums. The trusted curator must itself be trusted (or run in a TEE). Utility for searchers is argued, not measured.

## Relevance to us

A clean example of a defence that does not try to identify Sybils at all: randomise which inputs count, so that controlling many identities yields only proportional, noisy influence. The same technique fits agent swarms that aggregate reports from unverified agents (sampling plus noise rather than per-agent rate limits). Read with [[collective-2023-mev-share]] for the original design and its "searcher posing as a user" problem, and [[pan-2024-sybil]] for why randomised allocation is hard to make Sybil-proof when values differ.
