---
id: das-2018-anonymity
type: paper
title: 'Anonymity Trilemma: Strong Anonymity, Low Bandwidth Overhead, Low Latency - Choose Two'
authors: [Debajyoti Das, Sebastian Meiser, Esfandiar Mohammadi, Aniket Kate]
year: 2018
venue: 2018 IEEE Symposium on Security and Privacy (SP)
url: https://eprint.iacr.org/2017/954.pdf
doi: 10.1109/sp.2018.00011
arxiv: null
cite: Das, D., Meiser, S., Mohammadi, E., & Kate, A. (2018). Anonymity Trilemma - Strong Anonymity, Low Bandwidth Overhead, Low Latency - Choose Two. 2018 IEEE Symposium on Security and Privacy (SP), 108-126.
topics: [fork-merge-security]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: 50 (Crossref, 2026-10-03)
code: []
---

## Summary

Das and colleagues prove necessary conditions linking bandwidth overhead, latency overhead and anonymity in anonymous communication against a global passive adversary. If a fraction beta of users send noise per round and messages may stay in the network for at most l rounds, no protocol achieves strong anonymity (anonymity up to negligible failure) when 2 beta l < 1 - 1/poly(eta). If the adversary also passively compromises c of K protocol parties, strong anonymity is impossible when 2 (l - c) beta < 1 - 1/poly(eta) for c < l. They place existing protocols relative to these bounds and find several close to them.

## Contribution

A formal trilemma: of strong anonymity, low bandwidth overhead and low latency overhead, a protocol can have at most two.

## Key results

- Impossibility of strong anonymity when 2 beta l < 1 - 1/poly(eta), even with all parties honest.
- Each passively compromised party effectively removes one round of latency from the budget: bound 2 (l - c) beta.
- Separate treatment of synchronized and unsynchronized user distributions.

## Methods and models

Indistinguishability-based anonymity games against a global passive adversary; an ideal protocol used to show the bounds are the best any protocol can achieve under the model.

## Limitations and open questions

Necessary conditions only, not sufficient; passive compromise only.

## Relevance to us

Q1 cost model. Any scheme that hides which sub-agent returns by mixing real returns with decoys or by delaying returns pays in decoy bandwidth (beta) or merge latency (l), and every corrupted relay or courier part (c) eats into the latency budget. For a fork-merge design this gives a principled way to say how many decoys or how much delay is needed for a given number of corrupted parts, instead of guessing. Applies to [[piotrowska-2017-loopix]], [[chaum-1981-untraceable]] and [[dingledine-2004-tor]]; definitions of the anonymity notions in [[kuhn-2018-privacy]] and [[pfitzmann-2010-terminology]].
