---
id: de-tomaso-2005-isolation
type: paper
title: "Isolation and characterization of a protochordate histocompatibility locus"
authors: ["Anthony W. De Tomaso", "Spencer V. Nyholm", "Karla J. Palmeri", "Katherine J. Ishizuka", "W. B. Ludington", "K. Mitchel", "Irving L. Weissman"]
year: 2005
venue: "Nature"
url: https://europepmc.org/article/MED/16306984
doi: 10.1038/nature04150
arxiv: null
cite: "De Tomaso, A. W., Nyholm, S. V., Palmeri, K. J., Ishizuka, K. J., Ludington, W. B., Mitchel, K., & Weissman, I. L. (2005). Isolation and characterization of a protochordate histocompatibility locus. Nature, 438(7067), 454-459."
topics: [fork-merge-security]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 145  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Identifies the gene behind the Botryllus schlosseri fusion/rejection decision. From the abstract: histocompatibility, the ability to tell own cells from another's, is universal in Metazoa, but before this paper only the vertebrate MHC had been functionally characterized. The authors isolate a candidate gene encoding an immunoglobulin superfamily member that by itself predicts the outcome of histocompatibility reactions in this protochordate. They describe it as the first non-vertebrate histocompatibility gene and suggest it may inform the evolution of vertebrate adaptive immunity. Allele counts and prediction accuracy are not in the abstract and I did not read the full text.

## Contribution

Moves the Botryllus fusion gate from a genetically mapped locus to a cloned gene whose alleles predict fuse versus reject, which makes the gate a concrete, sequence-level identity check.

## Key results

- A single immunoglobulin-superfamily gene predicts histocompatibility outcome (abstract).
- Polymorphism levels, allele number and accuracy not checked.

## Methods and models

Positional cloning and characterization of the Fu/HC region in B. schlosseri (details not read).

## Limitations and open questions

Abstract only. Later work (not read here) adds further genes to the system; whether one gene fully explains the outcome is not checked.

## Relevance to us

Q2 and Q1. The biological fusion gate is a highly polymorphic, shared-allele match: two colonies fuse only if they share an allele, and high polymorphism makes a chance match with a non-relative unlikely. In protocol terms this is a secret-matching check whose security comes from allele diversity, not from voting among parts. For a fork-merge agent the analogue is a per-lineage secret (a key or nonce issued at fork) that a returning part must present; an attacker who corrupts a part but cannot read its secret cannot forge a different returning part, though a corrupted part that keeps its secret passes the gate. That is exactly the failure in [[stoner-1996-somatic]]: the gate checks identity, not integrity. See also [[buss-1982-somatic]].
