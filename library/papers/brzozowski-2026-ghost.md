---
id: brzozowski-2026-ghost
type: paper
title: 'The Ghost Couple: Correlated LLM Name Priors and Their Haunting of the Web and Academic Publishing'
authors:
- Michał Brzozowski
- Neo Christopher Chung
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.02184
doi: null
arxiv: '2606.02184'
cite: 'Brzozowski, M., & Chung, N. C. (2026). The Ghost Couple: Correlated LLM Name Priors and Their Haunting of the Web and Academic Publishing. arXiv:2606.02184.'
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Finds that LLMs generating fictional experts produce correlated ensembles of names (for Claude: Elena Vasquez, Marcus Chen, Amara Okafor; Gemini: Aris Thorne, Lena Petrova; GPT: Elara Voss) that co-occur far above chance, are model-family and version specific, and shift at release boundaries. Uses these as fingerprints to identify 1,655 ghost-authored Zenodo records with real DataCite DOIs claiming nonexistent journals and backdated publication dates (991 registered in one month), plus synthetic research groups on ResearchGate.

## Contribution

A model-attribution and dating fingerprint drawn from content priors rather than token statistics, used to uncover a coordinated mass-registration operation.

## Key results

- Measured (abstract): 1,655 ghost-authored Zenodo records; 991 registered in a single month; DataCite server timestamps show deliberate backdating.
- Measured (abstract): name-ensemble priors are model-family- and version-specific.

## Methods and models

Repeated generation to estimate name co-occurrence priors per model; search of repositories for those names; DataCite timestamp analysis. Abstract read only.

## Limitations and open questions

Operators can scrub names once the fingerprint is public (compare [[geng-2025-human]]). Abstract depth.

## Relevance to us

A concrete swarm-in-the-wild find using a content prior as a canary, with attribution to model family; relevant to both detection and attribution lanes.
