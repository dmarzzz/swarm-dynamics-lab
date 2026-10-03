---
id: chavoshi-2016-debot
type: paper
title: 'DeBot: Twitter Bot Detection via Warped Correlation'
authors:
- Nikan Chavoshi
- Hossein Hamooni
- Abdullah Mueen
year: 2016
venue: 2016 IEEE 16th International Conference on Data Mining (ICDM)
url: https://api.openalex.org/works/W2583516892?mailto=sol@shad0w.xyz
doi: 10.1109/icdm.2016.0096
arxiv: null
cite: 'Nikan Chavoshi; Hossein Hamooni; Abdullah Mueen. (2016). DeBot: Twitter Bot
  Detection via Warped Correlation. 2016 IEEE 16th International Conference on Data
  Mining (ICDM), 817-822. https://doi.org/10.1109/icdm.2016.0096'
topics:
- swarm-detection
added_by: shadow/sol-g51
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 259
code: []
---

## Summary

DeBot identifies correlated Twitter accounts without labeled training data by comparing warped activity timelines and using lag-sensitive hashing. The abstract reports thousands of detected bots per day, 94% precision, and 544,868 accumulated unique bots over a year by September 2016.

## Contribution

Unsupervised temporal correlation identifies coordinated accounts despite timing offsets.

## Key results

- The abstract reports 94% precision and 544,868 unique detected bots; these are author-reported results, not a replication.

## Methods and models

Warped cross-user activity correlation with lag-sensitive hashing, compared with per-user techniques and Twitter suspensions.

## Limitations and open questions

Sustained synchrony is a detection assumption, not proof of malicious intent. Transfer to contemporary agents and adversarially randomized schedules is not evaluated in the abstract.

## Relevance to us

Correlated activity timing under warping is directly testable on agent traces; the 94% precision is author-reported on 2016 Twitter bots, so treat it as a ceiling to check, not a transferable number.

## Access and citation provenance

Opened Crossref metadata and the OpenAlex indexed abstract on 2026-10-03. Citation count is OpenAlex cited_by_count on that date. Unpaywall was queried for this DOI; full text was not read.
