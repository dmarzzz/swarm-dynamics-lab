---
id: queller-2000-relatedness
type: paper
title: "Relatedness and the fraternal major transitions"
authors: ["D. C. Queller"]
year: 2000
venue: "Philosophical Transactions of the Royal Society of London. Series B, Biological Sciences"
url: https://europepmc.org/article/MED/11127911
doi: 10.1098/rstb.2000.0727
arxiv: null
cite: "Queller, D. C. (2000). Relatedness and the fraternal major transitions. Philosophical Transactions of the Royal Society of London. Series B, Biological Sciences, 355(1403), 1647-1655."
topics: [fork-merge-security, collective-decision]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 157  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Theory paper on transitions where independent units of the same kind coalesce into a higher-level individual (multicellularity, insect colonies). From the abstract: kin selection based on high relatedness permitted cooperation and reproductive division of labour in both. Development from a single cell keeps selfish conflict minimal because each selfish mutant gets only one generation of within-individual advantage before the next single-cell bottleneck. Conditionally expressed traits are particularly immune to within-individual selfishness because such mutations are rarely expressed in chimaeras. In social insects, differences in relatedness leave potential conflicts, but power asymmetries can settle them so decisively that colonies act as organisms. Abstract only.

## Contribution

States the bottleneck argument cleanly: passing the whole lineage through a single cell each generation limits how long any selfish variant can profit, which is the main reason clonal multicellular bodies resist internal cheaters.

## Key results

- Theoretical; no data. Key claim: a single-cell bottleneck limits a selfish mutant to one generation of within-individual advantage (abstract).

## Methods and models

Kin selection argument (abstract only).

## Limitations and open questions

Abstract only; I did not check the formal model.

## Relevance to us

Q2: offers a defence that is not a vote threshold. A parent that rebuilds itself each "generation" from a single trusted state (a bottleneck), rather than accumulating merged state from many returning parts, caps how long any corrupted contribution can persist. The agent analogue is periodic re-derivation of the parent from a small audited core plus re-verified knowledge, instead of append-only merging. Q3: the paper predicts the strongest attacks are on systems that skip the bottleneck, i.e. that merge continuously; [[bastiaans-2016-experimental]] measures exactly this in a fungus. Also relevant to the sybil and collective-decision lanes as a relatedness-based account of why large cooperative units stay stable.
