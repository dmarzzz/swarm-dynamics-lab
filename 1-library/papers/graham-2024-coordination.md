---
id: graham-2024-coordination
type: paper
title: "The coordination network toolkit: a framework for detecting and analysing coordinated behaviour on social media"
authors: ["Timothy Graham", "Sam Hames", "Elizabeth Alpert"]
year: 2024
venue: "Journal of Computational Social Science"
url: https://link.springer.com/article/10.1007/s42001-024-00260-z
doi: "10.1007/s42001-024-00260-z"
arxiv: null
cite: "Graham, T., Hames, S., & Alpert, E. (2024). The coordination network toolkit: a framework for detecting and analysing coordinated behaviour on social media. Journal of Computational Social Science, 7(2), 1139–1160."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: "25 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Introduces the Coordination Network Toolkit, open-source software that builds coordination networks for several behaviours at once: co-tweet (identical text), co-similarity (Jaccard of token sets), co-retweet, co-link and co-reply, each within a sliding time window around every message. Edges are directed and weighted and labelled by behaviour, giving a multi-behaviour multigraph. Re-analysing the 2020 #ReopenAmerica dataset (9,058,611 tweets by 2,949,118 accounts) with a 300-second window and at least five co-actions, it recovers known coordinated groups.

## Contribution

A reusable tool and a methodological fix (sliding windows, directed multigraphs) for the time-window edge effects and flattening problems of earlier co-action networks.

## Key results

- Sliding windows remove edge effects of fixed global time windows.
- In #ReopenAmerica, the largest co-retweet cluster is a counter-public (COVID-safety advocates), not the protest movement; several dense clusters are legitimate news networks, e.g. 28 Global Television outlets forming a complete subgraph (756 edges) and 15 7News accounts with 202 of 210 possible edges and clustering 0.971.
- Directionality exposes leader-follower structure inside coordinated groups, e.g. one 7News account posting before the others.

## Methods and models

Python toolkit with a CSV input of message id, user, timestamp, text and URLs; network construction in SQLite; export to Gephi. Revisits [[magelinski-2021-synchronized]]. I read the abstract, the toolkit design and the case study sections.

## Limitations and open questions

No statistical significance testing; the authors call for a tailored statistical framework. Many detected clusters are benign syndication.

## Relevance to us

A ready tool for co-action networks on any timestamped agent log. Its case study is also a warning: legitimate syndication (one owner, many outlets) looks exactly like a swarm, which is the benign analogue of one operator running many agents.
