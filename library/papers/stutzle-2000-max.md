---
id: stutzle-2000-max
type: paper
title: MAX–MIN Ant System
authors:
- Thomas Stützle
- Holger H. Hoos
year: 2000
venue: Future Generation Computer Systems
url: https://doi.org/10.1016/S0167-739X(00)00043-1
doi: 10.1016/S0167-739X(00)00043-1
arxiv: null
cite: Stützle, T., & Hoos, H. H. (2000). MAX–MIN Ant System. Future Generation Computer Systems, 16(8), 889–914. https://doi.org/10.1016/S0167-739X(00)00043-1
topics:
- swarm-intelligence
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 2734 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Presents MAX-MIN Ant System (MMAS), derived from Ant System but differing in key ways (pheromone bounds, greedier
search), and demonstrates the usefulness of each change experimentally. Relates MMAS's greedier search to search
space analysis of the problems, and reports that MMAS was among the best performing algorithms for the TSP and the
quadratic assignment problem. (Abstract read from the CORE record.)

## Contribution

Introduces bounded pheromone trails to prevent stagnation, the most widely used ACO variant in later theory
(runtime analyses of MMAS, e.g. [[neumann-2009-runtime]] lineage).

## Key results

- Claimed in abstract: MMAS among best performers on TSP and QAP at the time (numbers not read).

## Methods and models

Bounded pheromone trails and greedier search than AS; experiments on TSP and QAP (abstract only).

## Limitations and open questions

Abstract-level reading. Metadata note: the Crossref record for this DOI renders the title as "– Ant System" (the
small-caps MAX-MIN is lost), so `lab.py verify` flags a title mismatch; the title here follows the CORE record (OpenAlex
mirrors the truncated Crossref title).

## Relevance to us

Pheromone bounds are a simple mechanism to keep a stigmergic swarm away from lock-in (a form of noise floor), useful
when designing stigmergy-based coordination.

## Notes from dmarz/swarm-intelligence-audit

Audit 2026-10-03: `lab.py verify` flags a title mismatch because Crossref stores this title as "– Ant System" (the
small-caps MAX/MIN were dropped). Crossref volume 16(8), pages 889-914 and authors match the entry; the entry's
title is correct and the flag is a false positive.
