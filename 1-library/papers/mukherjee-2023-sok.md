---
id: mukherjee-2023-sok
type: paper
title: "SoK: The Ghost Trilemma"
authors: ["Sulagna Mukherjee", "Srivatsan Ravi", "Paul Schmitt", "Barath Raghavan"]
year: 2023
venue: "arXiv preprint (cs.CR)"
url: https://arxiv.org/abs/2308.02202
doi: null
arxiv: "2308.02202"
cite: "Mukherjee, S., Ravi, S., Schmitt, P., & Raghavan, B. (2023). SoK: The Ghost Trilemma. arXiv preprint arXiv:2308.02202."
topics: [sybil-resistance, meta]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "not checked"
code: []
---

## Summary

The authors posit the Ghost Trilemma: three properties of online identity, sentience (a live human is behind it), location (the claimed place is real) and uniqueness (one identity per person), cannot all be verified in a fully decentralised setting. The paper surveys trolls, bots and Sybils on social platforms, reviews prior verification approaches against the three properties, sketches a proof, and outlines incrementally deployable schemes that trade off reliance on centralised trust anchors, decentralised operation, attack resistance and privacy.

## Contribution

A systematisation that generalises Douceur's uniqueness question [[douceur-2002-sybil]] to three properties and ties the impossibility to distributed-computing consensus results.

## Key results

- Theorem 1 (sketch): for a verifier in an asynchronous, permissionless decentralised system without an honest majority, it is impossible to confirm sentience, location and uniqueness in finite time. The argument reduces verification to wait-free consensus among witnesses, some Byzantine. The authors say a full proof may be hard because of human elements.
- Case studies contrast real accounts with known troll accounts (for example Internet Research Agency accounts) by how well each property can be corroborated from public content.
- Practical direction: accept limited trust in centralised anchors to escape the trilemma.

## Methods and models

Systematisation of knowledge, qualitative case analysis, informal impossibility proof. About 22 pages; I read the introduction, framework, theorem statement and proof opening, case examples and conclusion.

## Limitations and open questions

The proof is a sketch. "Sentience" is defined operationally rather than formally. No quantitative evaluation of the proposed schemes.

## Relevance to us

For AI agent swarms the trilemma shifts: "sentience" becomes "which principal or model is behind this agent", and uniqueness becomes one agent per principal per role. The result says that, without an honest majority or a trusted anchor, a decentralised swarm cannot verify all of these together, which argues for explicit trust anchors (attested hardware, issuers) in agent admission. Pairs with [[ford-2020-identity]] and [[siddarth-2020-who]].
