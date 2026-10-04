---
id: bahrani-2026-capacity
type: blog
title: "Capacity oracles"
authors: [Maryam Bahrani, Mike Neuder]
year: 2026
url: https://ethresear.ch/t/capacity-oracles/24716
site: ethresear.ch
topics: [sybil-resistance, collective-decision]
added_by: dmarz/sybil-flashbots-informal
accessed: 2026-10-03
read_depth: skim
relevance: 5
---

## Summary

Forum post (23 April 2026, signed "maryam and mike") modelling how a protocol that delegates work (ZK proving, TEE-attested AI inference) can learn the spare capacity of its workers. Suppliers report capacity; with probability ε each report is audited by allocating that much work, and delivered work is paid b_i + r(b_i). Without Sybils any monotone reward elicits truthful reports. With Sybils, a supplier submits many copies of its capacity, raising its chance of allocation at no cost, so the oracle becomes arbitrarily wrong. Two fixes are analysed. Fully correlated allocation (everyone audited or no one, paid only if all deliver) gives a perfect oracle in every Nash equilibrium but is trivially griefable. Staking with full slashing on under-delivery is practical, but with linear rewards r = λb it is still Sybil-vulnerable for any finite stake: splitting capacity into N small bids concentrates the allocated amount near its mean and lets a supplier over-report by a factor α > 1 with vanishing slashing risk. Convex rewards r(x) = x^p discourage splitting; numerically, at ε = 0.017 a supplier gains by reporting N = 44 Sybils of size 1/5 (utility 0.0245 vs honest 0.017), while at ε = 0.034 honest single reporting is optimal. The authors then define the minimum audit rate ε* at which truthful reporting is optimal, as a function of stake and curvature, and study it numerically ("you get what you pay for"). Replies from Vitalik Buterin add the parallelised, fragile proving workload case.

## Key claims

- Sybil identities break capacity elicitation whenever unallocated or undelivered identities carry no penalty.
- Staking alone does not fix linear rewards; splitting plus law-of-large-numbers concentration beats any finite stake.
- Convexity of rewards in reported size directly penalises splitting, and truthfulness then depends on audit rate, stake and curvature together.
- Better oracles cost more because more work must be over-allocated to audit.

## Evidence quality

Formal model with derivations and numerical results; no empirical data. I read sections 1 to 4 and the replies closely; I only skimmed the final numerical results and summary.

## Relevance to us

This post is the closest Flashbots-adjacent analysis to Sybil resistance in a swarm of worker agents: any system that asks agents to self-report capacity, confidence or skill, and rewards them by report, invites splitting into many small identities. The results give concrete, testable design rules: penalise non-delivery per identity (stake and slash), make rewards convex in the size of a single identity's commitment, and set the audit rate high enough relative to stake. These can be simulated directly with LLM or scripted agents. Related: splitting in inclusion-list committees [[nag-2026-sybil]], Sybil-proof block-space allocation by the same group [[neuder-2024-block]], correlation penalties [[buterin-2024-supporting]].

Sybil-proofness of staking-based mechanisms more broadly: [[chitra-2025-sybil]], [[pan-2024-sybil]].
