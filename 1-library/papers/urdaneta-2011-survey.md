---
id: urdaneta-2011-survey
type: paper
title: "A survey of DHT security techniques"
authors: [Guido Urdaneta, Guillaume Pierre, Maarten van Steen]
year: 2011
venue: ACM Computing Surveys, vol. 43, no. 2, article 8, pp. 1-49
url: https://www.distributed-systems.net/my-data/papers/2011.acm-cs.pdf
doi: 10.1145/1883612.1883615
arxiv: null
cite: "Urdaneta, G., Pierre, G., & van Steen, M. (2011). A survey of DHT security techniques. ACM Computing Surveys, 43(2), Article 8, 1-49. https://doi.org/10.1145/1883612.1883615"
topics: [sybil-resistance, sync-consensus]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "127 (Crossref, 2026-10-03)"
code: []
---

## Summary

Survey of defences for structured peer-to-peer overlays (Chord, Pastry, Kademlia and relatives) against the three attacks the authors consider most important: the Sybil attack (one adversary injects many bogus identities to inflate the malicious fraction f that redundancy-based protocols assume is small), the Eclipse attack (poisoning honest nodes' routing tables until their neighbours are mostly malicious) and routing/storage attacks (misrouting lookups, corrupting replicas). For each attack they walk through the proposed defences paper by paper and tabulate advantages and disadvantages. Section 3 covers eleven Sybil defences and groups them into six families: centralized certification (Castro et al. 2002), distributed registration (Dinger and Hartenstein 2006), physical network characteristics and network coordinates (Wang et al. 2005; Bazzi and Konjevod 2005; Bazzi et al. 2006), social networks (Danezis et al. 2005; SybilGuard and SybilLimit), computational puzzles (Borisov 2006; Rowaihy et al. 2007) and game-theoretic economic incentives (Margolin and Levine 2007). Their verdict: certification is the most effective but needs a trusted CA that can also detect Sybils; network-characteristic methods fail against geographically spread attackers and need trusted online measurement; social-graph methods work only where a social network exists; puzzles tax honest nodes and let attackers choose IDs; incentive schemes detect rather than prevent. Section 6 notes that deployed DHTs (BitTorrent, KAD) rely on Kademlia replication plus redundant routing and remain Sybil-vulnerable because nodes pick their own identifiers. Conclusion: the hardest unsolved problem is secure, non-choosable node identifier assignment. Read: intro, all of Section 3 (Sybil) including Table I and discussion, the Eclipse intro, and the conclusions; Sections 4.x-5.x on individual Eclipse and routing defences skimmed only by heading.

## Contribution

First comprehensive survey of DHT defences (as opposed to attack taxonomies), with a side-by-side comparison table per attack class and an explicit six-way taxonomy of Sybil defences that later work reuses.

## Key results

- Sybil attack does no damage alone; it is the vector that breaks every "f < threshold" assumption (Section 3).
- Six Sybil-defence families with stated failure modes (Table I). Social-network methods were "shown to be very effective" in simulation; Danezis et al. 2005 "has not been shown to scale beyond 100 honest nodes".
- Eclipse arithmetic: with malicious fraction f = 0.25 and path length 5, single-path lookup succeeds with probability (0.75)^5 ~ 0.24, hence redundant routing is mandatory (Section 4).
- Securing a DHT requires: secure identifier assignment, low f, malicious nodes spread across the ID space, replication, and routing that reaches a correct replica set with high probability (Section 7).

## Methods and models

Literature survey, 2002-2009 material. Attack model throughout: a fraction f of participating nodes is malicious and may collude; identifiers are m-bit (m >= 128) and in the weak case chosen by the node. No new experiments; reproduces figures from surveyed papers.

## Limitations and open questions

Pre-blockchain and pre-LLM: proof-of-work as a Sybil defence appears only as Borisov's puzzles, proof-of-stake and proof-of-personhood are absent. Many conclusions are about simulations in the surveyed papers, not deployments. The authors flag that application-specific attacks (data poisoning) are out of scope.

## Relevance to us

The clearest single map of the pre-2010 Sybil defence space, useful for the sybil-resistance survey's "what is known" section and as the backward-citation hub: it chains [[douceur-2002-sybil]], [[castro-2002-secure]], [[bazzi-2005-establishment]], [[danezis-2009-sybilinfer]] precursors, [[yu-2006-sybilguard]], [[yu-2008-sybillimit]], [[baumgart-2007-skademlia]] and [[singh-2006-eclipse]]. The six-family taxonomy transfers almost directly to LLM agent swarms (who issues agent identities, can traffic fingerprints distinguish one operator's agents, do social-graph methods apply when agents have no social graph). Pairs with [[levine-2006-survey]] (earlier Sybil-specific survey) and [[gil-2015-guaranteeing]] (physical-characteristics family applied to robots, which the survey's critique of Wang et al. 2005 anticipates).
