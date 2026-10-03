---
id: wright-2004-predecessor
type: paper
title: 'The Predecessor Attack: An Analysis of a Threat to Anonymous Communications Systems'
authors: [Matthew K. Wright, Micah Adler, Brian Neil Levine, Clay Shields]
year: 2004
venue: ACM Transactions on Information and System Security
url: https://www.freehaven.net/anonbib/cache/Wright:2004.pdf
doi: null  # 10.1145/1042031.1042032; Crossref holds a truncated title ("The predecessor attack"), so lab.py verify cannot match it
arxiv: null
cite: 'Wright, M. K., Adler, M., Levine, B. N., & Shields, C. (2004). The predecessor attack: An analysis of a threat to anonymous communications systems. ACM Transactions on Information and System Security, 7(4), 489-522. https://doi.org/10.1145/1042031.1042032'
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 144 (Crossref, 2026-10-03)
code: []
---

## Summary

Wright and colleagues study corrupt members inside an anonymity protocol who simply log, in every round, which node handed them a message belonging to a tracked session. Whenever an initiator keeps talking to the same responder across path reformations, the true initiator appears as predecessor more often than anyone else, so over enough rounds the attackers identify it. They prove this for Crowds, Onion Routing, Mix-Nets, Hordes, Web Mixes and DC-Net and give upper bounds on the number of rounds needed, roughly O((n/c) log n) rounds for Crowds and O((n/c)^2 ln n) for Onion Routing with n participants and c attackers. Fully connected DC-Net resists longest but scales poorly. They also discuss fixed first hops ("helper nodes") as a defence.

## Contribution

Turned the intuition that repeated rerouting leaks the initiator into proofs and bounds that compare protocols, and introduced helper (later guard) nodes.

## Key results

- Any non-uniformity in path selection plus a persistent session is exploitable; the attack needs only passive logging by colluding members.
- Bounds on rounds-to-attack scale with (n/c) for Crowds and (n/c)^2 for Onion Routing (Table in Section 4); simulations show practical attack times below the bounds.
- Ring-topology DC-Net is cheap to attack; adding neighbours raises robustness and overhead.
- Varying path length does not by itself defeat the attack.

## Methods and models

Probabilistic analysis of logging attacks under uniform path selection with replacement, per-protocol bounds, and simulations of a static and a dynamic membership model.

## Limitations and open questions

Assumes sessions that persist across many reformations and attackers who can recognise the session in each round; churn and timing details change constants.

## Relevance to us

Q1, as the formal backbone. A fork-and-merge agent that repeatedly sends out parts and reintegrates a different one each time is an initiator reforming paths: colluding corrupted sub-agents that log which part handed them work will, over rounds, identify the parent and its merge channel. The bounds give a first quantitative handle on how many fork-merge cycles an agent can afford before its reintegration point is exposed, as a function of the fraction c/n of corrupted parts. The helper-node defence (fixed first hop) is the same move as [[overlier-2006-locating]]'s guards. Q2: the result is an argument that rotating merge partners is not free; a threshold design should avoid making the set of merging parts a fresh random draw each round. Related: [[dingledine-2004-tor]], [[chaum-1981-untraceable]].
