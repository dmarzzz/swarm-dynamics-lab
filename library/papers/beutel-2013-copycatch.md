---
id: beutel-2013-copycatch
type: paper
title: CopyCatch
authors:
- Alex Beutel
- Wanhong Xu
- Venkatesan Guruswami
- Christopher Palow
- Christos Faloutsos
year: 2013
venue: Proceedings of the 22nd international conference on World Wide Web
url: https://api.openalex.org/works/W2133591726?mailto=sol@shad0w.xyz
doi: 10.1145/2488388.2488400
arxiv: null
cite: Alex Beutel; Wanhong Xu; Venkatesan Guruswami; Christopher Palow; Christos Faloutsos.
  (2013). CopyCatch. Proceedings of the 22nd international conference on World Wide
  Web, 119-130. https://doi.org/10.1145/2488388.2488400
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 344
code: []
---

## Summary

CopyCatch detects coordinated Facebook Page Likes using a bipartite user-Page graph and edge timestamps. The abstract describes a convergent iterative algorithm, a scalable MapReduce approximation, bounds against greedy attacks, and deployment on Facebook rather than an LLM-specific detector.

## Contribution

Lockstep coordination is operationalized as graph structure plus temporal constraints.

## Key results

- Two algorithms are described; production use at Facebook is reported, but precision and recall are not in the abstract.

## Methods and models

User-Page edges and creation times, synthetic data and Facebook deployment.

## Limitations and open questions

The abstract does not establish detection robustness against adaptive LLM agents or distinguish legitimate coordination from malicious intent.

## Relevance to us

This provides a prior-art comparison for detecting coordinated automation, not evidence that any observed population is an LLM swarm.

## Access and citation provenance

Opened Crossref metadata and the OpenAlex indexed abstract on 2026-10-03. Citation count is OpenAlex cited_by_count on that date. Unpaywall was queried for this DOI; full text was not read.
