---
id: alvisi-2013-sok
type: paper
title: "SoK: The Evolution of Sybil Defense via Social Networks"
authors: ["Lorenzo Alvisi", "Allen Clement", "Alessandro Epasto", "Silvio Lattanzi", "Alessandro Panconesi"]
year: 2013
venue: "2013 IEEE Symposium on Security and Privacy (S&P 2013)"
url: https://www.cs.cornell.edu/lorenzo/papers/Alvisi13SoK.pdf
doi: "10.1109/sp.2013.33"
arxiv: null
cite: "Alvisi, L., Clement, A., Epasto, A., Lattanzi, S., & Panconesi, A. (2013). SoK: The Evolution of Sybil Defense via Social Networks. In 2013 IEEE Symposium on Security and Privacy, pp. 382-396. IEEE."
topics: [sybil-resistance, meta]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "178 (OpenAlex, 2026-10-03); 86 (Crossref)"
code: []
---

## Summary

A systematisation of social-graph Sybil defences from SybilGuard onward. It asks which structural property of social graphs (heavy-tailed degree, small world, clustering, conductance) can separate honest from Sybil regions and settles on conductance. It then shows the defences are random-walk methods that find fast-mixing regions around an honest seed, connects them to the theory of random walks, and identifies a community detection method based on approximate personalised PageRank (APPR) with provable guarantees for Sybil defence.

## Contribution

Two proposals: use APPR-style local community detection with guarantees, and change the goal from global, universal Sybil detection to securely white-listing a local region of the graph around each honest user, used as one layer in a defence in depth.

## Key results

- Popularity, small-world and clustering properties are shown to be unhelpful or exploitable for Sybil defence; conductance is the useful one (Section II analysis).
- The real social graph is a constellation of tightly knit communities loosely connected to each other, not one fast-mixing honest region; this undermines the original SybilGuard/SybilLimit model, consistent with [[viswanath-2010-analysis]].
- APPR gives a local algorithm whose cost depends on the community found, not the graph size.
- Methods with sophisticated guarantees can still fail against real attacks of primitive structure, reported from deployment experience (conclusion).

## Methods and models

Survey and analysis with random-walk theory; experiments on real graphs comparing structural properties and the APPR approach (skimmed).

## Limitations and open questions

Local white-listing protects a user's neighbourhood but does not provide global admission control. Pre-dates proof-of-personhood and blockchain identity work.

## Relevance to us

Swarm trust graphs are likely to be modular (teams, spatial clusters). The SoK's recommendation, accept a local, provably clean neighbourhood instead of trying to classify every agent globally, is a realistic target for agent swarms where each agent only needs to trust the peers it coordinates with. Connects SybilRank's propagation [[cao-2012-aiding]] to personalised PageRank, and should be read with [[yu-2006-sybilguard]], [[yu-2008-sybillimit]], [[danezis-2009-sybilinfer]], [[mohaisen-2013-sybil]].
