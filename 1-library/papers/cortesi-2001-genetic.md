---
id: cortesi-2001-genetic
type: paper
title: "Genetic Control of Horizontal Virus Transmission in the Chestnut Blight Fungus, Cryphonectria parasitica"
authors: ["Paolo Cortesi", "Charles E. McCulloch", "Haiyue Song", "Haiqun Lin", "Michael G. Milgroom"]
year: 2001
venue: "Genetics"
url: https://europepmc.org/article/MED/11560890
doi: 10.1093/genetics/159.1.107
arxiv: null
cite: "Cortesi, P., McCulloch, C. E., Song, H., Lin, H., & Milgroom, M. G. (2001). Genetic Control of Horizontal Virus Transmission in the Chestnut Blight Fungus, Cryphonectria parasitica. Genetics, 159(1), 107-118."
topics: [fork-merge-security]
added_by: dmarz/fm-biology
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: 127  # Europe PMC citedByCount, 2026-10-03
code: []
---
## Summary

Quantifies how a multi-locus self/non-self system limits transfer of an infectious agent when two fungal individuals touch and fuse. In C. parasitica, viruses (hypoviruses) pass between individuals through hyphal fusion, and vegetative incompatibility (vic) genes trigger cell death when fused partners differ. By replicating vic genotypes in independent isolates, the authors measured the effect of mismatch (heteroallelism) at each of six vic loci. Measured: transmission is 100 percent when donor and recipient have identical vic genotypes. A single mismatch at vic4 had no effect; at vic2 transmission fell to 21 percent; at vic3 76 percent; at vic6 32 percent. For vic1, vic2 and vic7 the rate depended on which alleles were in donor versus recipient (asymmetry). Effects of mismatches at two loci were mostly additive, with small significant epistasis in four pairs. A logistic regression on mismatch, asymmetry and epistasis predicted transmission between field isolates well; host background also mattered. Abstract only; the full text was not reachable (PDF behind a bot check).

## Contribution

Gives measured per-locus transmission probabilities for a multi-locus identity barrier, showing that protection accumulates roughly additively across mismatched loci and that loci differ greatly in strength.

## Key results

- Identical vic genotypes: 100 percent virus transmission. Measured.
- Single-locus mismatch: vic4 no effect, vic3 76 percent, vic6 32 percent, vic2 21 percent. Measured.
- Two-locus mismatches: mostly additive effects; small epistasis in 4 pairs. Measured.
- Direction matters for vic1, vic2, vic7 (asymmetric). Measured.
- Logistic model predictions correlated highly with independent field-isolate tests. Measured.

## Methods and models

Replicated laboratory pairings of C. parasitica isolates with defined vic genotypes; virus-infected donors paired with recipients; logistic regression model of transmission probability. Abstract only.

## Limitations and open questions

Abstract only, so sample sizes and the model coefficients are not checked. Barrier is incomplete: even with mismatches some transmission occurs. Host genetic background matters beyond vic.

## Relevance to us

Q2, strong: this is a biological, measured version of "the attacker must get past k independent checks". Each vic locus is an independent identity check, each passes some fraction of infections, and the combined pass rate is roughly the product (additive on the logit scale). It shows two practical features a fork-merge protocol should expect: checks are not equally strong (vic4 useless, vic2 strong), and some are asymmetric (depend on who is donor and who is recipient). It also shows the barrier is probabilistic, not a hard threshold, which argues for modelling merge security as a pass probability per check rather than a k-of-n count. Q3: the transmitted agent is a virus carried in the cytoplasm of the fused partner, the direct analogue of a payload riding in a returning sub-agent. Related: [[grum-grzhimaylo-2021-somatic]], [[bastiaans-2016-experimental]], [[marraffini-2008-crispr]].
