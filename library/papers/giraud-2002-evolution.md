---
id: giraud-2002-evolution
type: paper
title: "Evolution of supercolonies: The Argentine ants of southern Europe"
authors: ["T. Giraud", "J. S. Pedersen", "L. Keller"]
year: 2002
venue: "Proceedings of the National Academy of Sciences of the United States of America"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC122904/
doi: 10.1073/pnas.092694199
arxiv: null
cite: "Giraud, T., Pedersen, J. S., & Keller, L. (2002). Evolution of supercolonies: The Argentine ants of southern Europe. Proceedings of the National Academy of Sciences of the United States of America, 99(9), 6075-6079."
topics: [fork-merge-security, collective-decision, sybil-resistance]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: 212  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Samples 33 introduced Argentine ant populations along 6,004 km of Mediterranean and Atlantic coast and runs pairwise worker aggression tests among all of them (1,151 trials). Measured: two supercolonies. Within each, aggression never occurred, even between nests about 6,000 km apart; between them, aggression was always severe and killed workers in 98 percent (235 of 241) of trials. This held after 6 and 18 months of identical lab rearing, so recognition is genetic, not environmental. Workers from different nests of the same supercolony antennated each other no more than nestmates (9.14 versus 9.38 per 10 min, P = 0.66). Neutral diversity at 17 microsatellite loci was only 28 percent lower than a native population (1.4 alleles per locus), implying at least 6 to 13 founding queens, so the bottleneck was mild. Within the main supercolony, genetic distance did not predict aggression (r = -0.07, P = 0.90) despite real differentiation (Fst = 0.12). The authors propose "genetic cleansing": high nest density makes territorial fights costly, so colonies with common recognition alleles win, and recognition diversity is lost by selection rather than by drift.

## Contribution

Shows an all-or-nothing recognition system spanning millions of nests: membership is decided by a label that is shared across the whole unit and is independent of overall genetic similarity. The authors call the main supercolony the largest cooperative unit recorded.

## Key results

- 1,131 of 1,151 trials were either no antagonism or vigorous fighting; essentially binary. Measured.
- Between-supercolony trials lethal in 98 percent. Measured.
- Within-supercolony acceptance at 6,000 km; no distance or genetic-distance effect on aggression. Measured.
- Neutral allele loss 28 percent; Fst 0.12 within the main supercolony. Measured.
- Unicoloniality predicted to be unstable because selfish mutants that make larvae into queens should spread. Authors' speculation.

## Methods and models

Field collection of about 5,000 workers per population, blind randomized pairwise aggression tests (10 min, scored 0 to 5), replicate trials for 20 populations, lab re-tests after 6 and 18 months, 8 microsatellites on 20 workers per population and 22 loci on reference samples, bottleneck simulation, partial Mantel tests controlling for geography.

## Limitations and open questions

Single native reference population for the diversity comparison, which [[tsutsui-2003-genetic]] criticizes. The recognition loci themselves are unknown; the genetic cleansing hypothesis is inferred, not directly measured.

## Relevance to us

Q1 and Q3. The supercolony is a fission-fusion system that has solved the "who may rejoin" problem by making every member carry the same label, so any nest can merge with any other anywhere. This maximizes merge flexibility and anonymity among parts (Q1: no part is distinguishable), but it concentrates the whole security of the unit in one shared label. The authors' own prediction is that such a unit is vulnerable to selfish variants inside it, and the social parasite literature ([[lenoir-2001-chemical]], [[buschinger-2009-social]]) shows outsiders acquire the label by mimicry. For fork-merge agents, a single shared credential for all sub-agents makes them interchangeable but means one leaked credential admits an attacker everywhere. Related: [[tsutsui-2003-genetic]].
