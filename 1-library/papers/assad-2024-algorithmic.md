---
id: assad-2024-algorithmic
type: paper
title: "Algorithmic Pricing and Competition: Empirical Evidence from the German Retail Gasoline Market"
authors: ["Stephanie Assad", "Robert Clark", "Daniel Ershov", "Lei Xu"]
year: 2024
venue: "Journal of Political Economy"
url: https://ideas.repec.org/a/ucp/jpolec/doi10.1086-726906.html
doi: "10.1086/726906"
arxiv: null
cite: "Assad, S., Clark, R., Ershov, D., & Xu, L. (2024). Algorithmic Pricing and Competition: Empirical Evidence from the German Retail Gasoline Market. Journal of Political Economy, 132(3), 723–771."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "190 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

First empirical study of algorithmic pricing and competition, using high-frequency prices from German retail gasoline stations, where pricing software became widely available in 2017. Adoption dates are unknown, so adopters are detected by structural breaks in markers of algorithmic pricing; most breaks fall around the time of widespread introduction. Adoption is instrumented by brand headquarters' decisions. Adoption raises margins, but only for non-monopoly stations, and in duopoly and triopoly markets only when all stations adopt.

## Contribution

The main in-the-wild evidence that pricing algorithms coordinate on higher margins, and an example of detecting agent adoption itself from behavioural structural breaks.

## Key results

- Working-paper abstract (CESifo 8521, opened on RePEc): adoption raises margins by 9%, only in non-monopoly markets; in duopolies market-level margins do not change when one station adopts but rise by 28% when both do.
- Journal abstract: margins increase only if all stations adopt, in duopoly and triopoly markets.

## Methods and models

Structural break tests on station-level markers associated with algorithmic pricing to infer adoption (the abstract does not list the markers); IV with brand-headquarters adoption.

## Limitations and open questions

Abstract only (journal abstract and working-paper abstract on RePEc). Adoption is inferred, not observed; the mechanism (learning collusion versus faster matching) is not identified by the abstract.

## Relevance to us

A rare measured effect of agent coordination in a real market and a method for detecting which actors are agents from behaviour breaks. Theory: [[calvano-2020-artificial]]; audit method: [[eschenbaum-2026-auditing]].
