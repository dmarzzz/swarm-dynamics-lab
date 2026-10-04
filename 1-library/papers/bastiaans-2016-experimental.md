---
id: bastiaans-2016-experimental
type: paper
title: "Experimental evolution reveals that high relatedness protects multicellular cooperation from cheaters"
authors: ["E. Bastiaans", "A. J. Debets", "D. K. Aanen"]
year: 2016
venue: "Nature Communications"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC4857390/
doi: 10.1038/ncomms11435
arxiv: null
cite: "Bastiaans, E., Debets, A. J., & Aanen, D. K. (2016). Experimental evolution reveals that high relatedness protects multicellular cooperation from cheaters. Nature Communications, 7, 11435."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: skim
relevance: 5
citations: 55  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

A controlled experiment on whether free merging of individuals lets cheaters evolve. The fungus Neurospora crassa was serially propagated for 31 transfers (about 205 asexual generations) in 8 replicate lines per treatment. Low-relatedness lines used the standard strain, which fuses freely, at high spore density so every transfer formed one fused colony (the whole culture a common good). High-relatedness lines used an otherwise similar fusion-deficient mutant, so every spore grew as a separate individual. Measured: spore yield did not change in high-relatedness lines (Mann-Whitney P = 1.000) but fell on average threefold in all 8 low-relatedness lines (P = 0.001). Every low-relatedness line contained "cheater morphotypes": low yield alone (about 64-fold and 7-fold reductions in two examples) but higher competitive success when mixed with the ancestor at 1:9, and their success came mainly from reducing the ancestor's yield (regression F = 31.7, P < 0.0005). Against a near-isogenic ancestor of a different allotype that they could not fuse with, the cheaters' advantage disappeared. Cheaters and social types coexisted in 7 of 8 lines after 41 transfers, consistent with negative frequency dependence.

## Contribution

The direct experimental comparison, under otherwise identical conditions, of merging versus non-merging lineages. It shows that permitting fusion among individuals is sufficient for cheaters to evolve and erode cooperation, and that an allorecognition barrier removes most of their advantage.

## Key results

- Low relatedness (free fusion): threefold mean drop in spore yield across all 8 lines; high relatedness: no change. Measured.
- Cheater morphotypes have reduced yield alone but increased competitive success with the ancestor; strong negative relation between monoculture yield and competitive success (F1,18 = 27.1, R2 = 0.60). Measured.
- Blocking fusion with an incompatible allotype removed the cheaters' significant advantage. Measured.
- Cheaters show reduced female (costly somatic) function; mutations segregate 1:1 in back-crosses, consistent with single nuclear mutations. Measured.
- Some high-relatedness lines also produced low-yield morphotypes, suggesting other routes to exploitation without fusion (for example leaked goods or cell contents released on incompatibility death). Authors' interpretation.

## Methods and models

Neurospora crassa serial transfer of asexual spores (1 percent of about 10^8 spores per transfer, 3 days growth), 2 x 8 lines, 31 then 41 transfers. Yield and linear growth rate assays, pairwise competition at 1:9 with marked ancestor, back-crosses, competition against heterokaryon-incompatible ancestor. I read the results sections; methods skimmed.

## Limitations and open questions

Single species and a lab regime chosen to maximize fusion. The fusion-deficient mutant may differ from the wild type in other ways; the authors address this partly with the incompatible-allotype test. Mechanism of cheating was left open here and was resolved in [[grum-grzhimaylo-2021-somatic]].

## Relevance to us

Q2, strong: this is the closest thing in biology to a controlled test of "merge freely" versus "never merge". Free merging of many parts each round led every replicate to accumulate cheaters and lose a third of output; keeping parts separate and selecting on each part's own output prevented it. For a fork-merge agent, the analogue is to evaluate each returning sub-agent's contribution in isolation (its own verified output) before admitting anything into shared state, rather than pooling first and evaluating the pool. Q3: the cheaters did not attack the host directly; they invested less in shared work and still got merged in, which is the profile of a corrupted sub-agent that does little useful exploration but is reintegrated anyway. Related: [[queller-2000-relatedness]] (theory), [[foster-2002-costs]], [[cortesi-2001-genetic]] (multi-locus barrier).
