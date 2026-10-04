---
id: wright-2020-coordinated
type: talk
title: Coordinated Inauthentic Behavior
authors:
- Colin Wright
year: 2020
url: https://letsknowthings.substack.com/p/coordinated-inauthentic-behavior-c39
venue: Let's Know Things, 2020-06-02
topics:
- swarm-detection
- sybil-resistance
added_by: shadow/sol-aud
accessed: '2026-10-03'
read_depth: full
relevance: 3
---

## Summary

Colin Wright's Let's Know Things explainer discusses botnets, sockpuppets, and influence operations. Read the complete approximately 38-minute Deepgram transcript. This is secondary commentary on news and earlier research, not original detector validation.

- [08:38] Wright introduces an MIT Technology Review report about suspected automated participation in COVID-related Twitter discussion. [10:35] He relays a corpus of approximately 200 million tweets and a taxonomy of behaviors including bridging communities, artificially backing accounts, and provoking removal of a target group. [11:25] He reports high suspected-bot fractions among influential retweeters, but the episode does not provide classifier thresholds, error estimates, or a prevalence denominator suitable for independent verification.
- [11:42] Automated networks and human-run sockpuppets are distinguished while sharing a campaign-level pattern of accounts supporting one another. [19:23] Removing deceptive groups risks catching legitimate ones; [20:21] domestic advocacy and ordinary strongly held opinions can resemble some influence-operation behaviors.
- [24:01] He describes a feedback loop in which coordinated posting creates apparent popularity, recommender systems amplify it, and journalists or politicians pick up the resulting frame. This is an explanatory mechanism rather than a measured causal effect in the podcast.
- [30:17] Restricting replies is described as a proposed countermeasure with a tradeoff: it can reduce abusive interruption but also suppress corrective fact-checking. Wider claims about platform business incentives and near-universal personal manipulation are commentary, not established causal findings here.

## Relevance to us

A readable taxonomy of population-level manipulation and why detecting coordination cannot stop at identifying individual automated accounts. Treat the relayed bot estimates cautiously and trace them to primary studies before quantitative use. Compare [[gleicher-2021-coordinating]]: that interview uses a narrower platform-policy definition and explicitly discusses unknown denominators and investigation bias. Neither episode is evidence for detecting contemporary LLM swarms.
