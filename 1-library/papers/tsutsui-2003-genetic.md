---
id: tsutsui-2003-genetic
type: paper
title: "Genetic diversity, asymmetrical aggression, and recognition in a widespread invasive species"
authors: ["N. D. Tsutsui", "A. V. Suarez", "R. K. Grosberg"]
year: 2003
venue: "Proceedings of the National Academy of Sciences of the United States of America"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC298729/
doi: 10.1073/pnas.0234412100
arxiv: null
cite: "Tsutsui, N. D., Suarez, A. V., & Grosberg, R. K. (2003). Genetic diversity, asymmetrical aggression, and recognition in a widespread invasive species. Proceedings of the National Academy of Sciences of the United States of America, 100(3), 1078-1083."
topics: [fork-merge-security, collective-decision, sybil-resistance]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: 127  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Tests Crozier's paradox in the invasive Argentine ant (Linepithema humile): recognition needs diverse labels, but if being rejected is costly, individuals carrying rare labels are attacked more and the diversity that recognition depends on is selected away. Field: 607 pairwise worker assays among 5 colonies (one from the large California supercolony). Aggression was polarized in 9 of 10 colony pairs (one side almost always started it), and the attacking colony had fewer polymorphic loci in every case (sign test P < 0.001) and fewer alleles in all but two (P = 0.055), but not lower expected heterozygosity (P = 0.38). In 193 trials with a clear aggressor, when only one ant survived the aggressor survived six times more often (P < 0.0001). Lab: 28 single-queen subcolonies reared for 8 months lost genetic diversity and then attacked workers of their own source colony; aggression was polarized in 18 of 24 aggressive pairs and the low-diversity side initiated in 14 of 18 (P < 0.05). Interpretation: low-diversity colonies have narrower templates, reject more, and win fights, which drives positive frequency-dependent selection against diverse colonies and stabilizes the supercolony.

## Contribution

Measures both conditions of Crozier's paradox in one system: rejected individuals pay a cost, and rejection is directed from low-diversity to high-diversity groups. It supplies a mechanism for how a recognition system can erode itself.

## Key results

- 607 field assays; aggression polarized in 9 of 10 colony pairs. Measured.
- Attacking colony had fewer polymorphic loci in all pairs (P < 0.001). Measured.
- Aggressors survived 6x more often than recipients when one died (P < 0.0001); held even when the aggressor came from the usually attacked colony (13 of 15). Measured.
- Single-queen lab subcolonies (lower diversity) attacked their own source colony; 14 of 18 polarized pairs (P < 0.05). Measured.
- Workers learn a shared colony template from colony odour; a broader referent gives a broader, less stringent template. Background from the paper.

## Methods and models

Paired-worker aggression assays (5 min, scored 1 to 4; extended to 2 h for survival), 12 microsatellite loci on 610 workers, diversity measured as alleles, polymorphic loci and expected heterozygosity, sign tests across colony pairs. Experimental single-queen subcolonies with 20 workers maintained 8 months, then assayed against field source colonies and genotyped.

## Limitations and open questions

Assays were not blind at first; a blind rescoring of 31 trials found one misidentified attacker, against the direction of bias. Microsatellites are a proxy for unknown recognition loci. Worker-level survival is not shown to translate into colony-level productivity.

## Relevance to us

Q2 and Q1. The recognition template is learned from the group, and its breadth sets how much is accepted. A group with a narrow template (low internal diversity) rejects outsiders aggressively; a group with a broad template accepts more. For a fork-merge agent, a parent whose acceptance criterion is learned from its own recent merged state will widen over time as it absorbs diverse parts, lowering its guard; this is a drift mechanism to watch. The paper also shows how a recognition system can collapse into one huge accepting unit ([[giraud-2002-evolution]]), at which point a single shared label admits anyone who carries it, the weakness that ant social parasites exploit ([[lenoir-2001-chemical]], [[buschinger-2009-social]]). Cross-lane: the label-based admission here is a natural sybil-resistance case, see [[douceur-2002-sybil]].
