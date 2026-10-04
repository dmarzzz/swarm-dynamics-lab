---
id: sasy-2024-sok
type: paper
title: 'SoK: Metadata-Protecting Communication Systems'
authors: [Sajin Sasy, Ian Goldberg]
year: 2024
venue: Proceedings on Privacy Enhancing Technologies 2024(1)
url: https://petsymposium.org/popets/2024/popets-2024-0030.pdf
doi: 10.56553/popets-2024-0030
arxiv: null
cite: 'Sasy, S., & Goldberg, I. (2024). SoK: Metadata-Protecting Communication Systems. Proceedings on Privacy Enhancing Technologies, 2024(1), 509-524.'
topics: [fork-merge-security]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: 20 (Semantic Scholar citing-paper listing of Loopix, 2026-10-03)
code: []
---

## Summary

Sasy and Goldberg systematise 31 metadata-protecting communication systems that aim to resist a global network adversary. They classify them by privacy goal, using the notions of [[kuhn-2018-privacy]] (sender-message unlinkability, receiver-message unlinkability, relationship unobservability, communication unobservability) combined with functionality (end-to-end messaging or anonymous broadcast), and separately by core technique (DC-nets, mixnets including Loopix-style stratified designs, PIR-based mailboxes, private-write systems, secure multiparty computation, and a differential-privacy family). They find that only eight systems reach even generously defined low latency, that several of those process messages sequentially, that few scale horizontally, and that most offer weak protection against anonymity-set manipulation.

## Contribution

The most recent review of metadata-hiding communication, with two taxonomies and a direct comparison of guarantees, costs and failure modes.

## Key results

- 31 systems surveyed; four categories by guarantee, six families by technique.
- Only eight systems achieve low latency; five of them (PIR or RPIR based, such as Pung, SealPIR, Express, Riposte, Sabre) process messages sequentially, with horizontal scaling quadratic in user growth.
- Communication-unobservable designs are mostly synchronous on purpose, because having every user send in every round defeats statistical disclosure and intersection attacks; any relationship-unobservable design becomes communication-unobservable if every client sends a real or dummy message each round.
- Most systems do not protect against anonymity-set manipulation attacks.

## Methods and models

Systematisation of knowledge with tables comparing privacy goals, assumptions, latency and scalability; I read the abstract, introduction, taxonomy, trade-off sections and conclusion.

## Limitations and open questions

Messaging-centric; does not consider agent workloads. Deployment remains the stated open goal.

## Relevance to us

Q1 review anchor. The rule "everyone sends in every round, dummy if needed" is the cleanest statement of how a parent can make the identity of the returning sub-agent unobservable: every sub-agent reports every round, real or dummy, and the parent merges only the real one. The SoK's warning about anonymity-set manipulation matters for fork-merge: an attacker who can create or remove parts (Sybil, [[douceur-2002-sybil]]) shrinks the set the real returner hides in. Cost evidence for [[das-2018-anonymity]]; system examples [[piotrowska-2017-loopix]], [[chaum-1981-untraceable]], [[chor-1998-private]]; agent-protocol analogue [[dangol-2026-privacy]].
