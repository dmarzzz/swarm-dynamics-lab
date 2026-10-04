---
id: alkalay-houlihan-2014-false-name
type: paper
title: "False-Name Bidding and Economic Efficiency in Combinatorial Auctions"
authors: [Colleen Alkalay-Houlihan, Adrian Vetta]
year: 2014
venue: Proceedings of the 28th AAAI Conference on Artificial Intelligence (AAAI-14), Quebec City, pp. 538-544
url: https://www.math.mcgill.ca/vetta/Research.dir/falsename.pdf
doi: 10.1609/aaai.v28i1.8828
arxiv: null
cite: "Alkalay-Houlihan, C., & Vetta, A. (2014). False-Name Bidding and Economic Efficiency in Combinatorial Auctions. In Proceedings of the 28th AAAI Conference on Artificial Intelligence (AAAI-14), pp. 538-544. AAAI Press. https://doi.org/10.1609/aaai.v28i1.8828"
topics: [sybil-resistance, collective-decision]
added_by: shadow/sol-p1
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "6 (Crossref, 2026-10-03)"
code: []
---

## Summary

Takes the opposite tack from the false-name-proof design literature: rather than building mechanisms immune to pseudonymous bidding (which sacrifice efficiency, per Iwasaki et al.), ask how much welfare the plain VCG mechanism actually loses when bidders do use false names. The analysis is a price-of-anarchy style bound over Nash equilibria of the VCG game with free disposal, monotone valuations and the notion of alpha near-submodularity (alpha = 1 is submodular / goods are substitutes, larger alpha allows bounded complementarities). Theorem 1: with individually rational bidders whose valuations and bid functions are alpha near-submodular, every Nash equilibrium of VCG has welfare at least OPT / (1 + alpha). Theorem 2 (main): if each bidder's valuation is alpha near-submodular and one bidder uses false-name bids (possibly non-individually-rational and arbitrary bid vectors across its pseudonyms), every Nash equilibrium still has welfare at least OPT / (1 + alpha); the bound is almost tight (instances with welfare at most OPT / alpha exist) and extends to k false-name bidders with welfare at least (1/(1+alpha))^k OPT when all but one deviant bid near-submodularly. The authors emphasise that for substitutes (alpha = 1) false-name bidding costs at most half the welfare under VCG, which they argue is a better trade than the large efficiency losses of false-name-proof mechanisms, and that computational hardness of finding profitable pseudonymous strategies further limits harm in practice. Read: abstract, introduction and VCG background, definitions, Theorems 1-2 statements with discussion of tightness and extensions, proof outline for Theorem 2, conclusion.

## Contribution

Shows that VCG is robust in welfare terms to false-name bidding when complementarities are bounded: a 1/(1+alpha) price-of-anarchy guarantee, which reframes Sybil bidding as a bounded efficiency loss rather than a disqualifying flaw.

## Key results

- Theorem 1: VCG Nash equilibria achieve >= OPT/(1+alpha) with IR, alpha near-submodular bidders.
- Theorem 2: same bound survives one arbitrary false-name bidder; almost tight; (1/(1+alpha))^k for k deviants.
- For substitutes, false-name bidding under VCG loses at most a factor 2 of welfare.

## Methods and models

Combinatorial auction with m goods and n bidders, VCG payments, Nash equilibria of the complete-information bidding game, smoothness-style welfare arguments, near-submodularity parameter.

## Limitations and open questions

Nash equilibria of the full-information game, not dominant strategies; bounds degrade with complementarity alpha and with the number of pseudonymous bidders; revenue (which VCG can lose entirely under false names) is not addressed.

## Relevance to us

Counterweight to [[iwasaki-2010-worst-case]] and [[sakurai-1999-limitation]]: if agents' valuations over resources are close to substitutes, a platform may be better off running VCG and tolerating Sybil bidders (bounded 2x welfare loss) than paying the 2/(m+1) worst-case price of a false-name-proof rule. That is a concrete design decision for agent resource markets. Related bounds in other domains: [[cheng-2024-tight]] (2x Sybil gain in proportional response), [[bachrach-2008-divide]] (voting power). Framework: [[yokoo-2000-effect]], [[yokoo-2004-effect]]. Root: [[douceur-2002-sybil]].
