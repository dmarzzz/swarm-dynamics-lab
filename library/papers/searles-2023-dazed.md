---
id: searles-2023-dazed
type: paper
title: "Dazed & Confused: A Large-Scale Real-World User Study of reCAPTCHAv2"
authors: ["Andrew Searles", "Renascence Tarafder Prapty", "Gene Tsudik"]
year: 2023
venue: "arXiv preprint"
url: https://arxiv.org/abs/2311.10911
doi: "10.48550/arXiv.2311.10911"
arxiv: "2311.10911"
cite: "Searles, A., Prapty, R. T., & Tsudik, G. (2023). Dazed & Confused: A Large-Scale Real-World User Study of reCAPTCHAv2. arXiv preprint arXiv:2311.10911."
topics: ["swarm-detection", "sybil-resistance"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Searles, Prapty and Tsudik ran a 13-month study with over 3,600 distinct users of a live university account-creation and password-recovery service protected by reCAPTCHAv2, plus a post-study survey. Users improve on checkbox challenges with repetition; website context changes solving time; image challenges are rated annoying and checkbox ones easy (SUS 'OK' vs 'good'). Weighing cost against security, they conclude reCAPTCHAv2 has an immense cost and no security, and should be deprecated.

## Contribution

Large real-world human-cost measurement of the most deployed CAPTCHA, giving the human side of the cost ledger.

## Key results

- Measured (abstract): over 3,600 users over 13 months.
- Measured (abstract): context (account creation vs password recovery) significantly affects solving time.
- Claimed (abstract): reCAPTCHAv2 has 'immense cost and no security'.

## Methods and models

Live deployment with logging, post-study survey, System Usability Scale. Abstract only.

## Limitations and open questions

Abstract only; the security claim relies on other work's attacks.

## Relevance to us

Human friction is the price of challenge-based detection; any swarm-detection scheme that adds challenges pays it. Pairs with [[plesner-2024-breaking]].
