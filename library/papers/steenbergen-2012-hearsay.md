---
id: steenbergen-2012-hearsay
type: paper
title: "Hearsay: Suppressing spam using trust in mobile social gossiping networks"
authors: [Onno Steenbergen]
year: 2012
venue: MSc thesis, Embedded Software Section, Delft University of Technology (committee K. G. Langendoen, E. Onur, D. H. J. Epema, N. Brouwers)
url: https://repository.tudelft.nl/record/uuid:2b257abd-a17a-43c0-938b-2b25fcead09a
doi: null
arxiv: null
cite: "Steenbergen, O. (2012). Hearsay: Suppressing spam using trust in mobile social gossiping networks. Master's thesis, Delft University of Technology, Delft, The Netherlands. http://resolver.tudelft.nl/uuid:2b257abd-a17a-43c0-938b-2b25fcead09a"
topics: [sybil-resistance, swarm-intelligence]
added_by: shadow/sol-p2
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "1 (Exa index, 2026-10-03; not in Crossref, no DOI)"
code: []
---

## Summary

Master's thesis on spam suppression in pocket-switched (opportunistic, phone-to-phone gossip) networks of the kind proposed for protests and disasters when the Internet is cut. Plain gossip delivers every message to everyone, so a single spammer can saturate the network. Hearsay ranks senders by social distance using a TrustRank-style (PageRank-derivative) computation over the local social graph each phone has observed opportunistically; messages are queued and forwarded in rank order, new or unknown users get rank zero, and users revoke friendships when they register spam, which propagates as friendship-removal messages. Three variants are simulated in NetLogo 5.0 (at least 5 seeded runs per test, standard deviation around 25 percent on some metrics): plain Hearsay, Hearsay Friendship (friendship messages prioritised) and Hearsay Threshold (do not forward messages below a rank threshold). The design chapter states the Sybil constraints explicitly: never rely on globally computed or peer-reported values, let new nodes receive but limit their sending, and assume an unrestricted number of spammers. The thesis also walks through a group attack where passive Sybil "friends" keep an active spammer's rank up so that blocking one spammer just lets the group swap in a new identity. Results: with equal volumes of spam and real messages, plain gossip converges to a 50 percent signal-to-noise ratio, while Hearsay blocks the attacker and recovers; Threshold holds signal-to-noise around 96 percent because nobody forwards spam, at the cost of slower propagation of legitimate and friendship messages; one attacker trusted by five users (10 percent of the population) still manages to "infect" (get forwarded by) 50 percent of users under plain Hearsay before revocation catches up. Propagation of normal messages is only marginally slower than plain gossip. Read the abstract, related work on Sybil and trust, design considerations, the attack chapter and the results and conclusion chapters; the ranking equations and the NetLogo setup were skimmed.

## Contribution

A concrete local-only trust-ranking design for gossip networks that treats Sybil creation as the default adversary (cheap identities, no central authority), and a simulation showing that social-distance ranking plus distributed revocation suppresses spam without a bootstrap server. Student work, so modest in scope, but unusually explicit about which signals are safe to trust (local observations only) and which are not (anything reported by peers).

## Key results

- Plain gossip under 1:1 spam load: signal-to-noise settles at 50 percent; Hearsay variants recover after users revoke the attacker (Figure 5.9).
- Hearsay Threshold: about 96 percent signal-to-noise during the attack, slower recovery and slower friendship propagation.
- One attacker with five friends (10 percent of users) infects 50 percent of nodes under plain Hearsay before purging (Figure 5.11).
- Block probability per received spam of about 0.1 percent chosen; lower is similar, higher blocks too eagerly or causes repeated spam waves (Figure 5.8).
- Bluetooth-range (10 m) gossip reaches 50 percent of users in a week; Wi-Fi range (100 m) reaches 90 percent (baseline from related work, Section 2).

## Methods and models

TrustRank-derived ranking over a locally observed social graph with trust decay factor alpha; rank-ordered forwarding queues; friendship and revocation messages; NetLogo 5.0-RC7 agent-based simulation with random walks, seeded repeats, Bluetooth-like contact ranges. No deployment.

## Limitations and open questions

Simulation only, small populations (about 50 users inferred from "five friends = 10 percent"), high variance (standard deviation about 25 percent). The group/Sybil-ring attack is described but the mitigation (everyone revoking the passive accomplices) relies on user diligence and is not quantified. The thesis itself lists the lack of a real implementation and the power cost of on-phone PageRank as open. No formal Sybil bound of the SybilGuard kind.

## Relevance to us

Background. Useful as a small, legible example of social-graph trust as a Sybil defence in a swarm of peer devices, in the lineage of [[yu-2006-sybilguard]] and [[yu-2008-sybillimit]] but with purely local computation, and as a worked case of the "passive Sybil friends prop up an active attacker" pattern that any reputation-based agent swarm would face. Same Delft group as [[durmus-2014-sybil]] (Langendoen, Onur), which took the identity-free route instead.
