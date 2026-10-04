---
id: margolin-2007-informant
type: paper
title: "Informant: Detecting Sybils Using Incentives"
authors: [N. Boris Margolin, Brian N. Levine]
year: 2007
venue: Financial Cryptography and Data Security (FC 2007), Lecture Notes in Computer Science vol. 4886, pp. 192-207
url: http://forensics.umass.edu/pubs/margolin.FC.2007.pdf
doi: 10.1007/978-3-540-77366-5_18
arxiv: null
cite: "Margolin, N. B., & Levine, B. N. (2007). Informant: Detecting Sybils Using Incentives. In Financial Cryptography and Data Security (FC 2007), LNCS 4886, pp. 192-207. Springer. https://doi.org/10.1007/978-3-540-77366-5_18"
topics: [sybil-resistance, swarm-detection]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "9 (Crossref, 2026-10-03)"
code: []
---

## Summary

An economic rather than technical Sybil detector. A detective offers a reward to any identity willing to reveal that it shares an owner with another identity: the informant posts a security deposit f and names a target peer; the detective pays the deposit plus a reward (2r in the Trust Game) to the target. Backward induction (Theorem 1) shows an independent target keeps the money, so no rational identity will name an independent peer (it would lose f), while a Sybil identity naming its own sibling simply moves money between pockets and nets 2r; hence playing is a dominant strategy exactly for Sybils with opportunity cost c <= 2r (Theorem 2 adds the detective's participation condition b >= 2r, where b is the value of learning about a Sybil). The full Informant protocol replaces the fixed reward with a reverse Dutch auction, raising r from an initial r0 until some identity confesses, which finds the minimum reward that reveals a Sybil attacker in the population; the paper argues legitimate users have higher opportunity cost for self-exposure than attackers. Because the mechanism is purely economic it needs no trusted hardware, physical measurement or application-specific structure; the paper notes it does not distinguish Sybils from close friends who fully trust each other with money, and that attackers who value their Sybils above the reward remain hidden. Read: abstract, introduction, Trust Game and Sybil Game with Theorems 1-2 and proofs, Dutch-auction protocol, discussion of limitations and related work (including collusion detection in eBay records); formal parameter analysis skimmed.

## Contribution

First incentive-based Sybil detection: make confession a dominant strategy for identities under common ownership and price-discover the attacker's valuation of secrecy with an auction.

## Key results

- Theorem 1: in the Trust Game only Sybil pairs profit from informing; independents never name independents.
- Theorem 2: participation thresholds, detective offers iff b >= 2r, Sybil informs iff c <= 2r.
- Reverse Dutch auction yields the minimum revealing reward; general-purpose, no physical token.

## Methods and models

Game-theoretic analysis with backward induction, rational self-interested identities, monetary deposits and rewards, auction extension; no empirical deployment.

## Limitations and open questions

Requires a payment rail and a detective with budget; cannot separate Sybils from fully trusting friends; attackers with high opportunity cost or coordinated refusal defeat it; costs scale with how much the attacker values concealment. Low citation count suggests limited uptake.

## Relevance to us

A genuinely different tool for the swarm-detection problem: instead of fingerprinting agents, pay them to defect against their siblings and measure the price. For LLM agents under one operator the opportunity-cost argument changes (agents may not be able to accept money or may be instructed to refuse), but bounty-for-self-identification mechanisms are a plausible layer on agent platforms. Fits with the incentive-level Sybil papers [[kash-2012-optimizing]], [[resnick-2009-sybilproof]], [[cheng-2005-sybilproof]] and with the survey [[levine-2006-survey]] by the same group. Root: [[douceur-2002-sybil]].
