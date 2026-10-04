---
id: magelinski-2021-synchronized
type: paper
title: "A Synchronized Action Framework for Responsible Detection of Coordination on Social Media"
authors: ["Thomas Magelinski", "Lynnette Hui Xian Ng", "Kathleen M. Carley"]
year: 2021
venue: "arXiv preprint"
url: https://arxiv.org/abs/2105.07454
doi: null
arxiv: "2105.07454"
cite: "Magelinski, T., Ng, L. H. X., & Carley, K. M. (2021). A Synchronized Action Framework for Responsible Detection of Coordination on Social Media. arXiv:2105.07454."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "15 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Proposes detecting automated coordination as synchronized action: accounts performing the same action type within a short time window, captured in multi-view networks with one layer per action type. Applied to the 2020 Reopen America conversation on Twitter it finds three coordinated campaigns and a cluster of users who push protest hashtags at very similar times while each focuses on a different US state. The paper also discusses how deploying coordination detectors shifts power.

## Contribution

Defines coordination by synchronized action across multiple action types, the basis for the multi-behaviour toolkit of [[graham-2024-coordination]], and adds a responsible-deployment discussion.

## Key results

- Three coordinated campaigns discovered in the Reopen America data (abstract).
- Covert coordination around the protests is "far more complex" than prior examples, motivating multi-view analysis (abstract).

## Methods and models

Multi-view networks of synchronized actions (same hashtag, URL, mention etc. within a time window), clustering on the multi-view graph. Window sizes are not in the abstract; [[graham-2024-coordination]] reports the original used 300 seconds.

## Limitations and open questions

Abstract only. Case-study validation, no ground-truth accuracy.

## Relevance to us

Synchronized action is the cheapest signal for agent swarms on a shared clock (cron jobs, same orchestrator). Re-analysed with directed multigraphs in [[graham-2024-coordination]].
