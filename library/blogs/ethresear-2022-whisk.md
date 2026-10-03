---
id: ethresear-2022-whisk
type: blog
title: 'Whisk: A practical shuffle-based SSLE protocol for Ethereum'
authors: [asn, Justin Drake, Dankrad Feist, Gottfried Herold, Dmitry Khovratovich, Mary Maller, Mark Simkin]
year: 2022
url: https://ethresear.ch/t/whisk-a-practical-shuffle-based-ssle-protocol-for-ethereum/11763
site: ethresear.ch
topics: [fork-merge-security, sybil-resistance, sync-consensus]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

A research-forum design post (13 January 2022) proposing Whisk, a shuffle-based single secret leader election for Ethereum. Validators register trackers (rG, krG) bound to their identity; each day 16,384 trackers are drawn from the validator set, shuffled and re-randomised over 8,192 slots by successive proposers who each shuffle 128 trackers with a zero-knowledge shuffle proof, and then 8,192 of them become the next day's hidden proposer list. A proposer reveals by proving knowledge of k for its tracker. Reported overheads: about 16.5 KB per block, 880 ms to shuffle and prove on a laptop and 21 ms to verify, and about 45.5 MB extra state for 300k validators.

## Key claims

- Hides the next day's proposers from everyone until each proposes, defeating sequential DoS on known proposers.
- Anonymity set about 8,192 candidates, estimated at about 2,108 distinct nodes if 20% of nodes run 80% of validators.
- Binding trackers to identities prevents "selling" a proposer slot by transferring keys.
- Residual RANDAO-bias risk: a simulated 10% adversary gains about 1.69 extra proposals per day through selective aborts.
- Limitations stated: added consensus complexity, cannot penalise missed proposals, blind DDoS on all home stakers still possible; compared with SASSAFRAS (needs a mixnet and trusted setup), Dandelion++ and Algorand-style multi-leader election.

## Evidence quality

Design proposal by Ethereum researchers with benchmark numbers and a simulation of RANDAO bias; not peer reviewed. Builds on [[boneh-2020-single]]. An independent simulation [[burianova-2025-secret]] found the public candidate list makes a coordinated DoS worse (28% missed blocks versus 6-8%).

## Relevance to us

Q1. Whisk is a worked, costed instance of "shuffle the identities of possible returners so nobody can tell which will act, then let the chosen one prove it". For a fork-merge agent it shows the operational shape (register before departure, many small verifiable shuffles by other parts, reveal with proof at merge) and its two known weaknesses: the candidate pool is public before shuffling, and the randomness source can be biased by a participant who withholds. Q2 (my inference, not stated in the post as read): privacy of a shuffle chain of this kind should rest on at least one honest shuffler mixing a given tracker, an anytrust assumption like [[chaum-1981-untraceable]]. Network leaks that bypass it: [[heimbach-2024-deanonymizing]].
