---
id: bialek-2012-statistical
type: paper
title: Statistical mechanics for natural flocks of birds
authors: [William Bialek, Andrea Cavagna, Irene Giardina, Thierry Mora, Edmondo Silvestri, Massimiliano Viale, Aleksandra M. Walczak]
year: 2012
venue: Proceedings of the National Academy of Sciences
url: https://arxiv.org/abs/1107.0604
doi: 10.1073/pnas.1118633109
arxiv: '1107.0604'
cite: 'Bialek, W., Cavagna, A., Giardina, I., Mora, T., Silvestri, E., Viale, M., & Walczak, A. M. (2012). Statistical mechanics for natural flocks of birds. Proceedings of the National Academy of Sciences, 109(13), 4786–4791.'
topics: [collective-motion, criticality-measurement]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "809 (OpenAlex, 2026-10-03); 705 (Crossref is-referenced-by-count, 2026-10-03); 736 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Builds the maximum-entropy model of flight directions consistent with measured local correlations in
starling flocks. The model is mathematically a Heisenberg model and predicts, with no free parameters, how
order propagates through entire flocks. Comparing flocks of different densities shows the effective
interaction range is a fixed number of topological neighbours; comparing sizes, the model reproduces the
scale-invariant long-range correlations. Read at abstract level from arXiv.

## Contribution

Brought maximum-entropy inference from neuroscience to collective motion and independently confirmed
topological interactions ([[ballerini-2008-interaction]]) and scale-free correlations
([[cavagna-2010-scale]]).

## Key results

- Claimed: zero-free-parameter prediction of order propagation; topological interaction range; scale-invariant
  correlations reproduced.
- Fitted values (added by audit from the arXiv text): for a typical snapshot the likelihood peaks at n_c = 11
  with J = 45.73 matching C_int = 0.99592; averaged over flocks n_c = 21.2 +/- 1.7, roughly constant in flock
  density (topological). Calibration on simulated flocks maps this to a true interaction range of about
  7.8 neighbours, close to the n_c = 7.0 +/- 0.6 they quote from the earlier STARFLAG analyses
  ([[ballerini-2008-interaction]] itself reports 6.5 +/- 0.9); the inflation is attributed to
  birds moving through the flock, which a static maximum-entropy model cannot represent.

## Methods and models

Maximum-entropy (pairwise) model fitted to 3D velocity snapshots of starling flocks.

## Limitations and open questions

Abstract-level read; static (equal-time) inference only.

## Relevance to us

MaxEnt fitting is a reusable way to infer effective coupling strength and range from swarm snapshots.

## Notes from dmarz/collective-motion-audit

Audit 2026-10-03. Metadata confirmed on OpenAlex (W2092685486) and arXiv 1107.0604. Added the fitted n_c and J
values to Key results after reading Fig. 2 and the Discussion of the arXiv PDF; read_depth left at abstract
because the rest of the paper was not read. cited_by_count 809 (OpenAlex, 2026-10-03).
