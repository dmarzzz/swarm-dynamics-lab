---
id: grum-grzhimaylo-2021-somatic
type: paper
title: "Somatic deficiency causes reproductive parasitism in a fungus"
authors: ["Alexey A. Grum-Grzhimaylo", "Eric Bastiaans", "Joost van den Heuvel", "Cristina Berenguer Millanes", "A. J. M. Debets", "D. K. Aanen"]
year: 2021
venue: "Nature Communications"
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC7862218/
doi: 10.1038/s41467-021-21050-5
arxiv: null
cite: "Grum-Grzhimaylo, A. A., Bastiaans, E., van den Heuvel, J., Berenguer Millanes, C., Debets, A. J. M., & Aanen, D. K. (2021). Somatic deficiency causes reproductive parasitism in a fungus. Nature Communications, 12(1), 783."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 18  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Finds the mechanism behind the Neurospora crassa cheaters from [[bastiaans-2016-experimental]]. Whole-genome sequencing of the cheaters from all 8 independent free-fusion lines found mutations in known fusion genes in every one: six in soft (so), five of them loss of function, one each in ham-5 and ham-8 (binomial P = 4.0e-6 that this is chance). So the cheaters have lost the ability to initiate fusion. A clean so deletion reproduced the cheating: it beat the wild type at frequencies up to about 30 percent and lost above that, and total spore output fell as its frequency rose. Wild-type mycelia readily fused with the mutant (more than 20 percent heterokaryotic spores after one transfer, up to 40 percent by the fourth), while mutant-mutant fusion was under 0.2 percent. With vegetatively incompatible wild types, which kill fused cells carrying different het alleles, the mutant had no advantage at any frequency. Inside a chimera the mutant's nuclei declined during somatic growth but were over-represented in spores when below about 60 percent of nuclei. Interpretation: fusion is an altruistic act that builds the shared somatic network; cheaters let others fuse to them and then are less likely to be used for somatic work, so their nuclei end up in reproductive hyphae.

## Contribution

Shows a counterintuitive attack shape: the parasite is the partner that does not initiate the merge but accepts being merged into. The cost and benefit of fusion are unequally distributed and the passive partner profits. It also shows that an allorecognition barrier (het incompatibility) is necessary and sufficient here to stop the exploitation.

## Key results

- All 8 independently evolved cheaters carry mutations in fusion genes (so x6, ham-5, ham-8); P = 3.991e-06 against chance. Measured.
- Delta-so beats wild type only below about 30 percent frequency; total spore yield declines as its frequency rises. Measured.
- Wild type fuses with Delta-so often (20 to 40 percent heterokaryotic spores); Delta-so with itself under 0.2 percent. Measured.
- No advantage against incompatible wild types at 10 or 90 percent start frequency. Measured.
- In chimeras, Delta-so nuclei decline during growth (mean end/start ratio 0.61, P = 4.8e-07) but are enriched in spores below about 60 percent frequency. Measured.
- Four of seven other fusion mutants also cheat; three do not, so fusion loss is not the whole story. Measured.
- The authors speculate that cheater accumulation in long-lived clonal fungi resembles germline senescence and that long-lived species need policing (allorecognition, compartmentalization, synchronized division).

## Methods and models

Illumina whole-genome sequencing of 36 evolved morphotypes and 2 ancestors (about 25x and 40x), variant calling with VarScan. Competition assays at 10 to 90 percent mutant frequency, phenotype counts on sorbose plates and qPCR on hygB versus so. Heterokaryon transfer experiments with inl and pan auxotrophic markers. Competitions against near-isogenic het-incompatible strains. Race-tube growth of 10 heterokaryons followed by sporulation, qPCR of nuclear ratios. Most experiments performed once with three biological replicates.

## Limitations and open questions

Most experiments were run once (three replicates). Lab regime with very high spore density; the authors note natural ecology of N. crassa is poorly known. Not all fusion mutants cheat, so other factors matter. The frequency dependence means cheaters self-limit, which may not hold in systems without spatial fragmentation.

## Relevance to us

Q3, strong: the most effective "corrupted part" here is not an aggressive one. It is a part that stops paying for integration, lets the healthy parts reach out and merge with it, and then rides the shared infrastructure into what gets passed on. For agents: a sub-agent that never initiates sharing but accepts every merge request, and whose state is less often used for expensive shared work, can end up over-represented in the parent's persistent memory. A merge protocol in which the parent pulls from returning parts is exposed to this; it suggests weighting each part's contribution by its verified work rather than by its presence.
Q2: the measured defence is the incompatibility check at fusion, which removed the advantage entirely; this is a gate, not a quorum. The frequency dependence (benefit only below about 30 percent) is a natural threshold: a cheater that becomes common fragments the network and loses. That points to a design where merge payoffs fall as the share of low-contribution parts rises.
Related: [[bastiaans-2016-experimental]], [[stoner-1996-somatic]], [[cortesi-2001-genetic]].
