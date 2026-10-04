---
id: marraffini-2008-crispr
type: paper
title: "CRISPR interference limits horizontal gene transfer in staphylococci by targeting DNA"
authors: ["L. A. Marraffini", "E. J. Sontheimer"]
year: 2008
venue: "Science"
url: https://europepmc.org/article/MED/19095942
doi: 10.1126/science.1165771
arxiv: null
cite: "Marraffini, L. A., & Sontheimer, E. J. (2008). CRISPR interference limits horizontal gene transfer in staphylococci by targeting DNA. Science, 322(5909), 1843-1845."
topics: [fork-merge-security]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 1326  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Horizontal gene transfer in bacteria happens through phage transduction, transformation and conjugation; conjugation spreads antibiotic resistance. CRISPR loci give sequence-directed immunity against phages. A clinical Staphylococcus epidermidis isolate carries a CRISPR spacer matching the nickase gene present in nearly all staphylococcal conjugative plasmids. The authors show CRISPR interference prevents both conjugation and plasmid transformation in this strain. Inserting a self-splicing intron into the nickase gene blocked interference even though the spliced mRNA reconstituted the target sequence, showing the machinery targets DNA, not RNA. Conclusion: CRISPR counters multiple routes of horizontal transfer. Abstract only.

## Contribution

First demonstration that CRISPR, known as phage immunity, also blocks plasmid transfer, i.e. it filters what other lineages can add to a genome, and that it checks the incoming DNA itself.

## Key results

- CRISPR spacer matching nickase blocks conjugation and transformation (abstract).
- Disrupting the DNA target with an intron abolishes interference even when the mRNA target is restored (abstract).

## Methods and models

Conjugation and transformation assays in S. epidermidis with wild-type and modified targets (abstract only).

## Limitations and open questions

Abstract only. One strain and one plasmid family.

## Relevance to us

Q2 and Q3. CRISPR is a memory of past invaders used to reject matching incoming material at the point of transfer, a signature-based merge filter. It checks a specific representation (DNA), and a change in that representation defeats it even when the functional product is unchanged. For a fork-merge agent, a filter on returning content is only as good as its match to the form the content arrives in; a check on one representation can be bypassed by content that only becomes the dangerous form after admission. Also note the cost side: blocking all horizontal transfer also blocks useful genes (here antibiotic resistance), the same trade-off a parent faces in rejecting what a sub-agent learned abroad. Related: [[cortesi-2001-genetic]] (identity-based barrier to virus transfer), agent-side memory injection [[dong-2025-memory]].
