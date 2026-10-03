---
id: stoner-1996-somatic
type: paper
title: "Somatic and germ cell parasitism in a colonial ascidian: Possible role for a highly polymorphic allorecognition system"
authors: ["Douglas S. Stoner", "Irving L. Weissman"]
year: 1996
venue: "Proceedings of the National Academy of Sciences of the United States of America"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC26390/
doi: 10.1073/pnas.93.26.15254
arxiv: null
cite: "Stoner, D. S., & Weissman, I. L. (1996). Somatic and germ cell parasitism in a colonial ascidian: Possible role for a highly polymorphic allorecognition system. Proceedings of the National Academy of Sciences of the United States of America, 93(26), 15254-15259."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 113  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

The colonial tunicate Botryllus schlosseri either fuses with a neighbouring colony (shared blood vessels, a chimera) or rejects it, and the choice is set by one highly polymorphic locus, Fu/HC: colonies fuse only if they share at least one allele. Stoner and Weissman tracked microsatellite genotypes in buds (soma), sperm (germline) and blood of 9 laboratory chimeras and 10 field chimeras from a Monterey marina, plus 15 pairs of touching but unfused field colonies. Measured: blood was chimeric in every fused pair; partner genotypes entered buds and testes in all 5 stable lab chimeras by week 4; in several pairs one partner's testes were replaced by the other's genotype (at least 96 to 98 percent, the assay detection limit) within 4 weeks, and this persisted after the pair was surgically separated. In the field, 8 of 10 chimeras showed germ cell transfer and 4 of 10 showed germ cell parasitism; in two of these one partner took almost the entire sperm output. Progeny tests confirmed it: in one cross all 24 offspring of a "parasitized" half were sired by the partner, and eggs were usurped too. Germ or somatic cell parasitism was found in 40 percent of fused chimeras versus 6.7 percent of unfused adjacent pairs (G = 4.1, P < 0.05). Speculated: Fu/HC polymorphism is maintained because it restricts fusion, and therefore this parasitism, to siblings.

## Contribution

First field demonstration that fusion of two genetically distinct colonies leads to one partner's circulating stem cells taking over the other's gonads, while the body of the victim still looks like itself. It is the empirical anchor for Buss's hypothesis [[buss-1982-somatic]] that allorecognition exists to gate fusion against germline parasitism.

## Key results

- Fused chimeras: G/SCP in 40 percent; unfused adjacent pairs: 6.7 percent (13 of 15 pairs showed no admixture). Measured.
- Germline replacement in lab chimeras completed in as little as 4 weeks and persisted at least 8 weeks, including in pairs separated after 1 week of fusion. Measured.
- Field: almost the entire spermatic output of one partner usurped in 2 of 10 chimeras; cross 10.2 x 670.2 gave 24 of 24 progeny sired by the partner. Measured.
- Somatic tissue of the loser kept its own genotype while its gametes were replaced: "a somatic appearance may mask the winner of a gametic war". Measured and stated by the authors.
- Natural chimerism rate cited as up to 20 percent of colonies (from earlier work, not measured here).

## Methods and models

Laboratory: fusible pairs cut into four subclones, fused on glass slides, harvested at 1, 4, 8 weeks, or separated after 1 week and harvested 7 weeks later. Tissue sampled along a transect across the fusion plane: buds, sperm, blood. Field: 10 chimeras identified by colour polymorphism, 15 unfused contacting pairs. PCR typing at several microsatellite loci with titration controls (detection limit 2 to 4 percent of the minor genotype). Progeny testing by crossing chimeric halves to a third lab colony.

## Limitations and open questions

Small samples (9 lab, 10 field chimeras). The unfused pairs were classed as "putatively rejecting" without knowing their history; some may have fused and separated earlier. The authors could not tell whether replacement comes from clonal seeding or competition among lineages, and could not yet say whether "winner" genotypes are heritable parasitic specialists. They state that they have no mathematical model for inheritance when germlines compete inside a fused body.

## Relevance to us

Q3 (attack vector), strong: this is the clearest biological case of a merge where the returning part's "body" looks normal but its reproductive output, the thing that is inherited, has been taken over by another lineage. The analogue for agents is a sub-agent whose surface behaviour passes inspection while whatever it writes into shared memory or weights on merge is the attacker's. Detection that looks only at the soma (outputs, style) would miss it, as the field observers would have without genotyping. The effect also survives separation: once the parasitic cells are in, cutting the connection does not remove them.
Q2 (thresholds): the defence observed is a single gate at the point of fusion (Fu/HC match), not a k-of-n vote. Once fused, there is no further check, and the parasitism rate jumps from 6.7 to 40 percent. This argues for checking at merge time rather than relying on later audit.
Q1: no direct bearing. Related: [[laird-2005-stem]] isolates the stem cells responsible, [[de-tomaso-2005-isolation]] clones the gate, [[pancer-1995-coexistence]] is the independent lab replication, [[grum-grzhimaylo-2021-somatic]] is the fungal analogue.
