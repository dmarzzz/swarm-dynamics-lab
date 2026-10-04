---
id: ford-2008-offline
type: paper
title: "An Offline Foundation for Online Accountable Pseudonyms"
authors: ["Bryan Ford", "Jacob Strauss"]
year: 2008
venue: "Proceedings of the 1st Workshop on Social Network Systems (SocialNets '08)"
url: https://bford.info/pub/net/sybil.pdf
doi: "10.1145/1435497.1435503"
arxiv: null
cite: "Ford, B., & Strauss, J. (2008). An Offline Foundation for Online Accountable Pseudonyms. In Proceedings of the 1st Workshop on Social Network Systems (SocialNets '08), pp. 31-36. ACM."
topics: [sybil-resistance, collective-decision]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "10 (Crossref, 2026-10-03)"
code: []
---

## Summary

The paper that introduces pseudonym parties. Its argument is that online abuse (spam, ballot stuffing, wiki vandalism) comes from the disposability of identities, not from anonymity. On one "Pseudonym Day" each year, local parties hand a pseudonym certificate and a slow-fading hand stamp to everyone physically present. A pseudonym server then lets each certificate create exactly one account per participating online service, without linking accounts across services and without collecting personal information. Banning an abuser removes them for a year, because they cannot re-enter under a new costume.

## Contribution

States "one body, one pseudonym" as a Sybil defence that keeps anonymity, and frames the remaining problem as keeping organisers accountable rather than users. This is the origin of the proof-of-personhood line [[borge-2017-proof-of-personhood]], [[ford-2020-identity]].

## Key results

- Position paper, no implementation or measurements.
- Classifies prior defences into four groups: tie users to network endpoints (IP addresses; MIT's large address block let students rig Slashdot and Doonesbury polls), authenticate real identities, rate-limit (CAPTCHAs, puzzles, social-graph heuristics), and remove incentives (false-name-proof auctions). Rate-limiting defences stop large automated attacks but not widespread small-scale cheating where everyone gains by cheating "just a bit".
- Secondary labels (credit cards, phone numbers, passports) fail because people can hold several or none; bodies are one per person.
- Federation: parties on the same day everywhere, with standardised procedures; operators of services choose which pseudonym providers to trust, like browser root certificates. A peer-to-peer system could be sliced into one DHT per trusted provider.
- Cost estimate by analogy to elections: UN figures of $1-3 per voter in developed countries and $4-8 in less experienced ones.
- Open questions listed include immediate first-time access, backup routes for people who cannot attend, and whether a rich actor can pay people to attend and collect their certificates.

## Methods and models

Design proposal with a security and trust model; workshop paper of six pages.

## Limitations and open questions

Annual cadence is slow; certificate selling is acknowledged but unsolved; organisers can mint extra certificates unless federations audit each other.

## Relevance to us

Two ideas carry over to agent swarms. First, accountability needs non-disposable identities, not deanonymisation: a swarm can keep agents pseudonymous if each controlling principal gets one slot per role and loses it on misbehaviour. Second, the closing deadline ("no latecomers once the ball starts") is the synchronous-admission fix to Douceur's Lemma 4 [[douceur-2002-sybil]]. The paper's suggestion that peer-to-peer protocols prioritise information from accountable-pseudonym neighbours is a direct precedent for weighting agent inputs by verified principal. See also [[siddarth-2020-who]].
