---
id: giglietto-2020-it
type: paper
title: "It takes a village to manipulate the media: coordinated link sharing behavior during 2018 and 2019 Italian elections"
authors: ["Fabio Giglietto", "Nicola Righetti", "Luca Rossi", "Giada Marino"]
year: 2020
venue: "Information, Communication & Society"
url: https://api.semanticscholar.org/graph/v1/paper/DOI:10.1080/1369118X.2020.1739732?fields=title,year,authors,venue,externalIds,citationCount,abstract,openAccessPdf,publicationVenue,journal
doi: "10.1080/1369118X.2020.1739732"
arxiv: null
cite: "Giglietto, F., Righetti, N., Rossi, L., & Marino, G. (2020). It takes a village to manipulate the media: coordinated link sharing behavior during 2018 and 2019 Italian elections. Information, Communication & Society, 23(6), 867–891."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "131 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Combines Facebook data from the CrowdTangle API with datasets of Italian political news stories from the 2018 general and 2019 European elections. It identifies networks of pages, groups and verified profiles that shared the same political news articles within a very short time of each other ("coordinated link sharing behavior"). Some entities were openly political; others presented themselves as entertainment venues. The share of inauthentic entities in a network relates to how many different news sources the network shares.

## Contribution

Introduced coordinated link sharing behaviour (CLSB) as a detection target on Facebook. The same first author later published CooRnet, a tool for this (title seen in search results; not opened).

## Key results

- Several networks of entities that shared the same political news within a very short period identified on Facebook (abstract; counts not in the abstract).
- Networks with more inauthentic entities shared a different range of sources, suggesting distinct strategies (abstract).

## Methods and models

Near-simultaneous sharing of the same political news URL by multiple Facebook entities, linked into networks of entities that repeatedly co-share (as described in the abstract; the exact time threshold is not given there).

## Limitations and open questions

Abstract only (read via the Semantic Scholar API; the publisher page refused automated access). CrowdTangle has since been shut down, so the data pipeline cannot be rerun as published.

## Relevance to us

URL co-sharing within seconds is how agent swarms amplify links. One of the special cases unified by [[pacheco-2021-uncovering]]; reviewed in [[mannocci-2026-detection]].
