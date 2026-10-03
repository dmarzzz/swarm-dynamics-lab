---
id: zhang-2009-promoting
type: paper
title: "Promoting Honesty in Electronic Marketplaces: Combining Trust Modeling and Incentive Mechanism Design"
authors: [Jie Zhang]
year: 2009
venue: PhD thesis, David R. Cheriton School of Computer Science, University of Waterloo (UWSpace handle 10012/4413)
url: https://personal.ntu.edu.sg/zhangj/paper/phd-thesis-Jie-Zhang.pdf
doi: null
arxiv: null
cite: "Zhang, J. (2009). Promoting Honesty in Electronic Marketplaces: Combining Trust Modeling and Incentive Mechanism Design. PhD thesis, University of Waterloo. http://hdl.handle.net/10012/4413"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "30 (OpenAlex via Exa summary, 2026-10-03; not independently verified)"
code: []
---

## Summary

Waterloo PhD thesis (supervisor Robin Cohen) on trust modelling in agent-mediated e-commerce. Buyers must judge sellers using ratings from other buyers ("advisors") who may lie (ballot stuffing, bad-mouthing), may be a dishonest majority, may flood the system with ratings, or may change behaviour. The thesis proposes a "personalized approach": a buyer computes each advisor's private reputation from agreement on commonly rated sellers, a public reputation from all the advisor's ratings, weights the two by how much personal evidence it has, tracks ratings in time windows, limits the number accepted per advisor per window (anti-flooding) and discounts old ratings with a forgetting factor. Experiments (simulated marketplaces) show it beats the Beta Reputation System (BRS), TRAVOS and similar models at detecting dishonest advisors and in buyer profit, including when advisors flood (Fig. 3.19 shows BRS false positives rising with rating volume). The second half embeds this in an incentive mechanism: buyers pick their most trustworthy advisors as social-network neighbours, sellers model buyers' reputation and give better offers to well-connected honest buyers, and the thesis proves honest buyers and sellers earn more. On identity attacks specifically: Section 6.2 and the "Robustness to Attacks" discussion (p. 139) name Sybil attacks (citing Douceur) as creating pseudonyms to gain influence, and the proposed defences are (a) registration authentication as on eBay (credit card) and (b) low initial trust for newcomers plus a trustworthiness threshold on which advisors are consulted, so fake identities take long to matter; betrayal attacks are handled by the forgetting factor. Read: abstract, Section 3.x example around fake identities and the flooding experiment, Section 6 robustness discussion, conclusion; the mechanism-design chapters and proofs skimmed by heading. The UWSpace record itself did not render from this box; the author's own PDF copy was read.

## Contribution

A personalised (per-buyer) advisor-trust model that is robust to dishonest majorities and rating floods, coupled with a market mechanism in which reputation flows both ways (sellers also model buyers) so honesty is profitable.

## Key results

- Personalized approach outperforms BRS/TRAVOS-type models in dishonest-advisor detection and buyer profit across majority-dishonest, flooding, sparse-experience and behaviour-change scenarios (simulation; specific numbers not captured).
- BRS false positive rate increases with rating volume even when ratings are fair (Fig. 3.19).
- Theoretical result that the incentive mechanism yields greater profit to honest buyers and sellers (later published as Zhang, Cohen and Larson, Computational Intelligence 28(4), 2012).
- Sybil handling is by newcomer discounting and registration cost, not by detection.

## Methods and models

Beta-distribution style rating aggregation with time windows and forgetting; private/public reputation weighting; simulated e-marketplace with buyer and seller agents; game-theoretic profit analysis for the mechanism.

## Limitations and open questions

Sybil resistance is argued, not measured: no experiment creates many pseudonyms and checks influence. Newcomer discounting penalises honest newcomers and is a known weak defence against patient attackers. 2009 simulations with hand-set parameters.

## Relevance to us

Background for reputation-based Sybil defences in agent societies: it shows the standard pre-blockchain toolkit (rate limits per identity, newcomer discounting, registration friction) and its honesty about relying on authentication for the hard case. Compare the Sybilproof reputation results in [[cheng-2005-sybilproof]], the P2P taxonomy in [[urdaneta-2011-survey]], the open-MAS review [[bijani-2014-review]] and the author's VANET trust survey [[zhang-2011-survey]]. Root: [[douceur-2002-sybil]].
