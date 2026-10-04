---
id: marti-2004-limited
type: paper
title: "Limited Reputation Sharing in P2P Systems"
authors: [Sergio Marti, Hector Garcia-Molina]
year: 2004
venue: Proceedings of the 5th ACM Conference on Electronic Commerce (EC '04), New York, pp. 91-101
url: https://cs.uwaterloo.ca/~klarson/teaching/F04-886/papers/marti04.pdf
doi: 10.1145/988772.988787
arxiv: null
cite: "Marti, S., & Garcia-Molina, H. (2004). Limited Reputation Sharing in P2P Systems. In Proceedings of the 5th ACM Conference on Electronic Commerce (EC '04), pp. 91-101. ACM. https://doi.org/10.1145/988772.988787"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "147 (Crossref, 2026-10-03)"
code: []
---

## Summary

Asks how much reputation information peers in an unstructured P2P file-sharing network need to share to avoid downloading corrupted files from malicious providers, and compares selection strategies: no reputation (random), local experience only, and "limited sharing" where a peer keeps a Friend-Cache of nodes it has had good experiences with and asks a small quorum of them for opinions (voting reputation), weighting answers by its own trust in them. Two identity models are simulated: static identities tied to a login (e.g. managed by a certificate authority) and self-generated key pairs that permit whitewashing, where a malicious node discards a bad reputation by minting a new identity; the paper notes self-managed identities make the system vulnerable to this and cites Douceur for the general multi-identity problem. In simulations of 100 to 5,000 nodes with up to 40% malicious nodes subverting 90% of files, the main metric is efficiency (expected downloads per valid file): random selection needs 42.5 attempts at 40% malicious nodes while voting reputation needs about 2, a 21x improvement, i.e. "limited reputation sharing can reduce the number of failed transactions by a factor of 20". Whitewashing degrades the reputation system but less than expected, about 2.3x worse at a verification ratio of 4.5 (four or five tries instead of two), which the authors read as a clear advantage of login-bound identities. Front nodes (malicious users using some identities to serve good files to promote their bad identities) have no adverse effect at quorum weight w_Q = 0.1. A Friend-Cache of about 10 suffices; larger quorums add traffic without improving selection; the "best provider" selection rule is more efficient than weighted-random but skews load onto the best-behaved nodes. Read: abstract, introduction, identity models, metrics, the whitewashing and front-node results, conclusion; the Friend-Cache query-routing section skimmed.

## Contribution

Quantifies, in simulation, that a small amount of locally curated reputation sharing captures most of the benefit of global reputation, and that cheap identity change (whitewashing) costs a reputation system a constant factor rather than breaking it.

## Key results

- Efficiency at 40% malicious nodes: random 42.5 downloads per good file vs ~2 with voting reputation (21x).
- Whitewashing: ~2.3x worse efficiency (verification ratio 4.5), still far better than random.
- Front-node promotion attacks ineffective at w_Q = 0.1.
- Friend-Cache size ~10 sufficient; quorum growth beyond top nodes wastes traffic.

## Methods and models

Discrete-event simulator of an unstructured Gnutella-style network, 100-5,000 nodes, malicious fraction pi_B and subversion probability p_B, static vs whitewashing identity models, Friend-Cache plus quorum voting, best vs weighted-random provider selection.

## Limitations and open questions

Malicious nodes do not lie about reputation or collude in the main experiments; whitewashing is modelled as periodic identity reset, not as parallel Sybil identities inflating votes; file validity is binary. Pre-DHT-era design.

## Relevance to us

A concrete baseline for how much identity churn hurts a reputation-based defence: constant-factor, not catastrophic, when peers rely mainly on their own experience and a few trusted friends. That is the design posture an agent platform could take against cheap agent identities (local trust, small quorums, newcomer discounting) before reaching for hard identity. Compare the Sybilproof reputation theory in [[cheng-2005-sybilproof]], the advisor-trust model in [[zhang-2009-promoting]] and the P2P Sybil taxonomy in [[urdaneta-2011-survey]]. Root: [[douceur-2002-sybil]].
