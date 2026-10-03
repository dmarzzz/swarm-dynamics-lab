---
id: cao-2012-aiding
type: paper
title: "Aiding the Detection of Fake Accounts in Large Scale Social Online Services"
authors: ["Qiang Cao", "Michael Sirivianos", "Xiaowei Yang", "Tiago Pregueiro"]
year: 2012
venue: "9th USENIX Symposium on Networked Systems Design and Implementation (NSDI 2012)"
url: https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final42_2.pdf
doi: null
arxiv: null
cite: "Cao, Q., Sirivianos, M., Yang, X., & Pregueiro, T. (2012). Aiding the Detection of Fake Accounts in Large Scale Social Online Services. In 9th USENIX Symposium on Networked Systems Design and Implementation (NSDI 12). USENIX Association."
topics: [sybil-resistance]
added_by: dmarz/sybil-foundations
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "443 (OpenAlex, 2026-10-03)"
code: [gh-binghuiwang-sybildetection, gh-brightid-brightid-antisybil]
---

## Summary

This is the SybilRank paper. SybilRank ranks accounts in an online social network by degree-normalised trust from an early-terminated power iteration (a short random walk) seeded at several known-honest accounts. Because few edges cross from honest to Sybil regions, trust does not reach Sybils before the iteration stops. It runs in O(n log n) on Hadoop and was deployed at Tuenti, then the largest social network in Spain.

## Contribution

The first social-graph Sybil defence shown to work in production at scale, with a design (multiple seeds placed in detected communities, degree normalisation, early termination at about the honest-region mixing time) that tolerates the community structure and slow mixing that broke earlier schemes.

## Key results

- Measured at Tuenti: about 90% of the 200K accounts ranked most likely fake actually warranted suspension, versus about 5% fake among accounts inspected under Tuenti's user-report process.
- Tuenti spent 14 full-time employees on manual fake-account review before deployment.
- Analytical: at most O(log n) Sybils per attack edge obtain higher degree-normalised trust than honest nodes; the guarantee only needs the full graph to mix more slowly than the honest region, not an absolute O(log n) mixing time.
- Compared against SybilLimit, SybilInfer, GateKeeper and others on real graphs (evaluation section).

## Methods and models

Power iteration of trust from seeds for O(log n) steps, then division by node degree; seeds chosen in Louvain-detected communities. Implementation in Hadoop/MapReduce on graphs with hundreds of millions of nodes.

## Limitations and open questions

Ranks rather than decides; operators still inspect the bottom of the list. Requires known honest seeds. Fails against attackers who obtain many attack edges (befriending real users), a gap later addressed by victim-prediction work such as Integro (not catalogued here).

## Relevance to us

SybilRank is the algorithm BrightID adapted (GroupSybilRank) for its proof-of-personhood graph, per [[siddarth-2020-who]], and its variants are implemented and benchmarked in the BrightID anti-Sybil package catalogued by another agent ([[gh-brightid-brightid-antisybil]]). For agent swarms it is the most practical template: seed trust at a few audited agents, propagate for a bounded number of steps, normalise by degree so that highly connected spam agents do not soak up trust. Compare [[alvisi-2013-sok]] on why this is a personalised-PageRank method.

## Notes from dmarz/sybil-code-data

SybilRank implementations: [[gh-binghuiwang-sybildetection]] (C++, single and multi-threaded, alongside SybilBelief, SybilSCAR and GANG) and [[gh-brightid-brightid-antisybil]] (Python, with GroupSybilRank, WeightedSybilRank and other variants evaluated against scripted attacks on the BrightID graph).
