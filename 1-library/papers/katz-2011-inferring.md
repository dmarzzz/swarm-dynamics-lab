---
id: katz-2011-inferring
type: paper
title: Inferring the structure and dynamics of interactions in schooling fish
authors: [Yael Katz, Kolbjørn Tunstrøm, Christos C. Ioannou, Cristián Huepe, Iain D. Couzin]
year: 2011
venue: Proceedings of the National Academy of Sciences
url: https://europepmc.org/article/MED/21795604
doi: 10.1073/pnas.1107583108
arxiv: null
cite: 'Katz, Y., Tunstrøm, K., Ioannou, C. C., Huepe, C., & Couzin, I. D. (2011). Inferring the structure and dynamics of interactions in schooling fish. Proceedings of the National Academy of Sciences, 108(46), 18720–18725.'
topics: [collective-motion]
added_by: dmarz/collective-motion
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: "979 (OpenAlex, 2026-10-03); 899 (Crossref is-referenced-by-count, 2026-10-03); 949 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Infers interaction rules directly from trajectories of golden shiners in groups of 2 and 3 by mapping mean
effective forces (speeding and turning) as functions of neighbour position and velocity. Speed regulation is
a dominant interaction and is transmitted to fish behind and ahead; alignment emerges from attraction and
repulsion rather than explicit orientation matching; fish copy direction changes of those ahead. Comparing 2-
and 3-fish groups shows substantial three-body effects, contradicting the standard assumption of averaging
pairwise responses, though the pairwise spatial structure persists in groups of 10 and 30. Read at abstract
level via Europe PMC.

## Contribution

With [[herbert-read-2011-inferring]] (same PNAS issue), the founding data-driven "force map" approach; both
challenge explicit alignment and simple neighbour averaging assumed in [[vicsek-1995-novel]] and
[[couzin-2002-collective]].

## Key results

- Measured: speed modulation dominant; no evidence of explicit orientation matching; significant three-body
  (non-additive) interactions; spatial structure persists for N = 10, 30.

## Methods and models

Golden shiners (Notemigonus crysoleucas), automated tracking, effective-force maps conditioned on relative
position and speed.

## Limitations and open questions

Abstract-level read; full text on PMC (PMC3219116) not accessible from here.

## Relevance to us

Force-map inference is the right tool to check what rule a learned or LLM agent swarm has actually
converged to.

## Notes from dmarz/collective-motion-audit

Audit 2026-10-03. Checked the summary against the OpenAlex abstract (W2002266200) and Crossref:
golden shiners in 2- and 3-fish shoals, speed regulation dominant, no explicit orientation matching,
substantial three-body effects, structure persisting in groups of 10 and 30. All match; read_depth abstract
is accurate. Citation count updated to OpenAlex (979).
