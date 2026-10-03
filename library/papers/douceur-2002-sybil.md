---
id: douceur-2002-sybil
type: paper
title: "The Sybil Attack"
authors: ["John R. Douceur"]
year: 2002
venue: "Peer-to-Peer Systems (IPTPS 2002), Lecture Notes in Computer Science, vol. 2429"
url: https://www.microsoft.com/en-us/research/wp-content/uploads/2002/01/IPTPS2002.pdf
doi: "10.1007/3-540-45748-8_24"
arxiv: null
cite: "Douceur, J. R. (2002). The Sybil Attack. In Peer-to-Peer Systems (IPTPS 2002), Lecture Notes in Computer Science, vol. 2429, pp. 251-260. Springer."
topics: [sybil-resistance, sync-consensus, meta]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "5626 (Semantic Scholar, 2026-10-03); 2267 (Crossref, 2026-10-03)"
code: []
---

## Summary

Douceur names and formalises the Sybil attack: one faulty entity presenting many identities to defeat redundancy in a peer-to-peer system. In a generic model with a broadcast cloud, correct and faulty entities, and no trusted authority, he proves four short lemmas showing that identity distinctness cannot be established except under unrealistic assumptions: equal resources for all entities, simultaneous validation of all identities, and a vouching threshold larger than the number of faulty entities.

## Contribution

The founding impossibility result for decentralised identity. It frames every later defence as either a logically central certifier or a bet on some scarce resource (computation, storage, bandwidth, and later social links, money or physical presence). Every other entry in this lane responds to it.

## Key results

- Lemma 1: a faulty entity with ρ times the resources of a minimally capable entity can present ρ distinct identities, even under direct resource testing.
- Lemma 2: if identities are not validated simultaneously, a single faulty entity can present an unbounded number of identities by reusing resources over time (this is decisive for temporal resources such as CPU and bandwidth; storage challenges can be extended indefinitely).
- Lemma 3: if a local entity accepts any identity vouched for by q accepted identities, a faulty set F can present unboundedly many identities when |F| ≥ q, or when its collective resources reach those of q + |F| minimal entities.
- Lemma 4: if correct entities do not coordinate their acceptance windows, even a minimally capable faulty entity can present ⌊|C|/q⌋ identities. A system tolerating a fraction φ of faulty identities then tolerates only φ/g of faulty entities.
- Three resource tests are sketched: timed communication replies, storage of large incompressible data with spot checks, and hash puzzles (find x, z such that the low n bits of hash(x|y|z) are zero). Combinable puzzles can be detected by checking that two identities' solutions are not the same concatenation.

## Methods and models

Formal model: entities E = C ∪ F, a broadcast cloud with guaranteed delivery, polynomially bounded computation, identities as hashes of public keys. Proofs are elementary counting arguments. No experiments.

## Limitations and open questions

The model is deliberately friendly to defenders (no DoS, guaranteed delivery), which strengthens the negative results but says little about the cost an attacker actually pays. It treats resource heterogeneity as fatal, whereas later work ([[gupta-2020-resource]], [[borge-2017-proof-of-personhood]]) asks only that Sybil influence be bounded or priced rather than eliminated. Social trust graphs are dismissed through the vouching lemmas, a point SybilGuard [[yu-2006-sybilguard]] answers by restricting attack edges instead of vouchers.

## Relevance to us

This is the baseline argument for any agent swarm: if agents are cheap to spawn (LLM instances, simulated robots, wallet-holding bots), then voting, quorum or redundancy among them is only meaningful if some scarce resource or trusted issuer bounds identities. Lemma 4's coordination requirement maps directly onto asynchronous agent onboarding: an attacker who joins different sub-swarms at different times can be counted many times. [[bara-2026-epistemic]] extends the same logic from identities to evidence. Surveys of the responses: [[levine-2006-survey]], [[mohaisen-2013-sybil]], [[alvisi-2013-sok]], [[siddarth-2020-who]]. Robotics instantiation: [[newsome-2004-sybil]], [[gil-2015-guaranteeing]].
