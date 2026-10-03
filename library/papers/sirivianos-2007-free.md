---
id: sirivianos-2007-free
type: paper
title: "Free-riding in BitTorrent Networks with the Large View Exploit"
authors: [Michael Sirivianos, Jong Han Park, Rex Chen, Xiaowei Yang]
year: 2007
venue: 6th International Workshop on Peer-to-Peer Systems (IPTPS 2007), Bellevue, WA
url: https://users.cs.duke.edu/~xwy/publications/largeview-iptps.pdf
doi: null
arxiv: null
cite: "Sirivianos, M., Park, J. H., Chen, R., & Yang, X. (2007). Free-riding in BitTorrent Networks with the Large View Exploit. In Proceedings of the 6th International Workshop on Peer-to-Peer Systems (IPTPS 2007)."
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: "not available (no DOI; OpenAlex rate-limited at access time; batch metadata lists 161)"
code: []
---

## Summary

Experimental study of a BitTorrent free-riding technique that needs no uploading at all: the modified client repeatedly asks the tracker (and peer exchange) for more peers until it holds a much larger than normal view of the swarm, connects to all of them, and simply waits for optimistic unchokes and seeder uploads, never reciprocating. Because every compliant peer optimistically unchokes a random neighbour periodically, a peer connected to everyone collects a steady trickle from each. Results: (a) in common public torrents the free-rider downloads faster than a compliant client; (b) on PlanetLab swarms of about 300 leechers (30 KB/s rate limits, compliant clients capped at 50 connections) free-riders on average outperform compliant clients as long as they are under about 40% of the swarm; (c) as the free-rider fraction rises to 60% both free-riders and compliant peers degrade substantially (tragedy of the commons). The paper positions itself against Shneidman et al.'s conjecture that a peer could multiply optimistic unchokes by presenting multiple identities to the tracker (a Sybil attack, cited to Douceur) and by reconnecting to improve queue placement: the large-view exploit achieves the effect without multiple identities, though the authors note modified clients could additionally assume multiple identities to widen their view when trackers cap per-request peer lists. Read: abstract, introduction, related work, mechanism description, PlanetLab results (Figures and Table), discussion; implementation details skimmed.

## Contribution

Shows that BitTorrent's reciprocity can be beaten by breadth rather than by cheating on contribution: optimistic unchoking, needed for bootstrapping, is itself the subsidy that a well-connected free-rider harvests.

## Key results

- Free-riders beat compliant clients in most public torrents tested.
- PlanetLab ~300-leecher swarms: free-riders faster on average when they are <40% of peers; at 60% everyone slows down substantially.
- Exploit works with a single identity; Sybil identities are an optional amplifier when trackers limit view size.

## Methods and models

Modified BitTorrent client (large view, no upload); live public torrents; controlled PlanetLab swarms with 10%, 40%, 60% free-rider fractions and 30 KB/s rate limits; compliant clients limited to 50 connections.

## Limitations and open questions

2007 client ecosystem (per-IP connection limits and later PEX/tracker changes alter the picture); workshop paper with small number of torrents; no proposed fix beyond noting that limiting view size pushes attackers toward Sybil identities, which just relocates the problem.

## Relevance to us

Useful companion to [[piatek-2007-incentives]] (BitTyrant) and [[cheng-2024-tight]]: together they show that a decentralised reciprocity mechanism can be exploited by (i) strategic allocation, (ii) breadth of connections, and (iii) identity multiplication, and that the three substitute for one another, so closing one channel pushes operators to another. For LLM agent marketplaces, rate limits per identity without identity cost invite exactly this substitution. Prior Sybil-in-BitTorrent framing: [[levine-2006-survey]]. Root: [[douceur-2002-sybil]].
