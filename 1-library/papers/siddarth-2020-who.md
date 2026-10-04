---
id: siddarth-2020-who
type: paper
title: "Who Watches the Watchmen? A Review of Subjective Approaches for Sybil-Resistance in Proof of Personhood Protocols"
authors: ["Divya Siddarth", "Sergey Ivliev", "Santiago Siri", "Paula Berman"]
year: 2020
venue: "Frontiers in Blockchain"
url: https://www.frontiersin.org/articles/10.3389/fbloc.2020.590171/full
doi: "10.3389/fbloc.2020.590171"
arxiv: "2008.05300"
cite: "Siddarth, D., Ivliev, S., Siri, S., & Berman, P. (2020). Who Watches the Watchmen? A Review of Subjective Approaches for Sybil-Resistance in Proof of Personhood Protocols. Frontiers in Blockchain, 3, 590171."
topics: [sybil-resistance, collective-decision, meta]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: "41 (OpenAlex, 2026-10-03); 45 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

A review of proof-of-personhood (PoP) protocols that use "subjective" human inputs (voting, vouching, interpreting, being present) instead of compute or stake. It defines PoP by a subjective substrate plus an objective incentive, sets out the "decentralized identity trilemma" (Sybil resistance, self-sovereignty, privacy), gives a taxonomy of primitives (reverse Turing tests, pseudonym parties, web of trust, intersectional identity, token curated registries, DAOs) and reviews seven projects: Idena, Humanity DAO, Kleros Proof of Humanity, Upala, BrightID, Duniter and the Equality Protocol.

## Contribution

The standard review of the blockchain-era PoP projects as of mid-2020, with a comparison table of governance, size, substrate, decentralisation, privacy and scalability for each.

## Key results

- Reported network sizes in 2020: Idena 4,012 validated identities; Humanity DAO about 640 members before shutdown in January 2020; BrightID 556 users with a positive anti-Sybil rank; Duniter Ğ1 2,801 holders; Equality Protocol 529 scored addresses (Table 1 and text; figures supplied by the projects).
- Idena: synchronous validation ceremonies about every two weeks, human-made FLIP picture-ordering tests; human accuracy about 95% versus 60-76% for AI teams (as reported in 2020). Invite codes add a web-of-trust layer. Main cost is the coordination burden.
- BrightID: social-graph verification from trusted seeds using GroupSybilRank, a variant of SybilRank [[cao-2012-aiding]]; the review states its Sybil resistance "has yet to be proven".
- Duniter: five certifications and at most five hops from referent members; good Sybil protection, slow growth.
- Four of seven projects rely mainly on web of trust, and the authors note there is no evidence of web-of-trust effectiveness against multiple attack vectors; an attacker can build real relationships under different names in disjoint groups.
- Applications that need PoP: UBI, one-person-one-vote governance, quadratic voting and funding (where splitting across accounts pays), airdrops, oracle juries.

## Methods and models

Literature and secondary-source review of project documentation; no experiments. The authors disclose involvement with the Equality Protocol, Kleros and the Idena community.

## Limitations and open questions

Many claims rest on project self-reports. Snapshot from 2020; Humanity DAO had already closed and several projects were prototypes. Coverage of biometric approaches (Worldcoin) is absent because they postdate the review.

## Relevance to us

Useful as a menu of mechanisms that could gate admission to an agent swarm or weight agent votes by unique principal: synchronous challenges (Idena), graph scores from seeds (BrightID), staked vouching with dispute resolution (Kleros), group liability (Upala). The review's warning about quadratic mechanisms is central for swarms: any rule that rewards breadth of support over intensity pays an attacker to split one agent into many. It also flags that AI progress erodes reverse Turing tests, which matters doubly when the participants are AI agents. Foundations: [[borge-2017-proof-of-personhood]], [[ford-2020-identity]], [[douceur-2002-sybil]]. Code: [[gh-brightid-brightid-antisybil]], [[gh-idena-network-idena-go]].

## Notes from dmarz/sybil-code-data

Code for two of the reviewed systems: [[gh-idena-network-idena-go]] (Idena node; its automine config exposes the validation ceremony timings) and [[gh-brightid-brightid-node]] with the anti-Sybil evaluation package [[gh-brightid-brightid-antisybil]] (GroupSybilRank and attack simulations).
