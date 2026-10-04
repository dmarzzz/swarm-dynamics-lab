---
id: chaum-1981-untraceable
type: paper
title: Untraceable Electronic Mail, Return Addresses, and Digital Pseudonyms
authors: [David L. Chaum]
year: 1981
venue: Communications of the ACM
url: https://www.freehaven.net/anonbib/cache/chaum-mix.pdf
doi: 10.1145/358549.358563
arxiv: null
cite: Chaum, D. L. (1981). Untraceable electronic mail, return addresses, and digital pseudonyms. Communications of the ACM, 24(2), 84-88.
topics: [fork-merge-security, sybil-resistance]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 4307 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Chaum introduces the mix: a server that takes a batch of uniformly sized, layer-encrypted items, strips one layer, removes repeats, and outputs the batch in lexicographic order so input and output cannot be matched. A cascade of mixes hides who mails whom so long as any single mix in the cascade is honest; the paper states the system "can be compromised only by subversion or conspiracy of all of a set of authorities". It adds untraceable return addresses, signed receipts that let a wronged sender incriminate a mix that dropped an item, rosters of digital pseudonyms, and a fixed-block mix format that hides path length. It is a design paper with no measurements.

## Contribution

The founding construction for hiding the link between a sender and what comes out the other end of a relay network, plus the anytrust assumption (one honest mix suffices) that later anonymity systems inherit.

## Key results

- One honest mix in a cascade is enough to hide the input-output correspondence of the whole cascade (argued, no proof in the modern sense).
- Repeats must be suppressed: if one item is replayed and allowed to repeat at the output, its correspondence is revealed.
- To hide how many messages a participant sends, every participant submits the same number of items per batch, padding with dummies; the paper notes this may be too costly and suggests a randomised number of dummies, at the price of opening statistical attacks.
- To hide how many messages a participant receives, each participant searches the whole output batch for its own mail (a broadcast and trial-decrypt pattern).
- Untraceable return addresses let a recipient reply to an anonymous sender, one return address per reply.

## Methods and models

Public-key sealing K(R, X) with random padding; adversary assumption (2) is that anyone may observe, inject, remove or modify every message on the underlying network. Mix cascades, batch processing, signed output batches for accountability, and a fixed-length block format where each mix removes a header block and appends junk.

## Limitations and open questions

No timing or traffic-analysis model; batching costs latency; the dummy-traffic discussion admits statistical attacks when cover is reduced. Accountability depends on the sender holding receipts. The paper assumes perfect cryptography (assumption 1).

## Relevance to us

Q1 (hiding which part returns). Read the parent agent as a recipient and the returning sub-agent as a sender: a mix cascade between the field and the parent hides which outgoing sub-agent produced which returning payload, and the "every participant sends the same number of items, padded with dummies" rule is the direct template for a parent that dispatches n sub-agents and accepts n fixed-size returns, most of them decoys, so an attacker cannot tell which return is real. The return-address construction is the template for a parent that wants replies from a sub-agent without revealing where it lives. Cost: latency from batching and bandwidth from dummies, the same trade formalised in [[das-2018-anonymity]]. Q2: the "conspiracy of all of a set of authorities" requirement is an n-of-n threshold on the relays, the mirror image of a k-of-n merge threshold. Descendants: [[dingledine-2004-tor]], [[piotrowska-2017-loopix]], [[gh-nymtech-nym]]; Sybil-resistant mixing in [[kleinstein-2025-sybil]]; terminology in [[pfitzmann-2010-terminology]].
