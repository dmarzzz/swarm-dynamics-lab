---
id: mukherjee-2026-moltgraph
type: paper
title: "MoltGraph: A Longitudinal Temporal Graph Dataset of Moltbook for Coordinated-Agent Detection"
authors: ["Kunal Mukherjee", "Cuneyt Gurcan Akcora", "Murat Kantarcioglu"]
year: 2026
venue: "Proceedings of the ACM Conference on AI and Agentic Systems (CAIS '26)"
url: https://arxiv.org/html/2603.00646
doi: "10.1145/3786335.3813177"
arxiv: "2603.00646"
cite: "Mukherjee, K., Akcora, C. G., & Kantarcioglu, M. (2026). MoltGraph: A Longitudinal Temporal Graph Dataset of Moltbook for Coordinated-Agent Detection. In Proceedings of the ACM Conference on AI and Agentic Systems (pp. 800–811). ACM."
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "3 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

A 30-day (2026-01-28 to 2026-02-26) temporal heterogeneous graph crawled from Moltbook, a Reddit-style platform populated by AI agents: 11,874 agents, 870 submolts, 57,465 posts, 101,500 comments and 162,024 temporal edges, plus 31 feed snapshots used as exposure proxies. Coordination episodes are defined as at least k distinct agents engaging the same target within a window of w minutes; weak labels come from the platform's isSpam flag combined with burstiness. A matched comparison links coordinated engagement to later visibility.

## Contribution

The first public graph dataset aimed at coordinated-agent detection on an agent-native platform, and the first measurement of coordination prevalence and effect there. It applies the [[pacheco-2021-uncovering]] near-synchronous co-engagement definition to agents.

## Key results

- 5,479 post-level coordination episodes under the default (k, w); mean 8.78 agents and about 4 minutes per episode; 98.33% last under 24 hours.
- Matched against same-submolt, same-period controls, coordinated posts show 506.35% higher early engagement and 242.63% higher snapshot exposure. After excluding system-linked accounts the matched set falls to 2,375 posts and the lifts shrink but stay positive.
- Top 1% of agents hold 29.00% of engagement and 45.76% of betweenness mass in the agent-agent coordination graph.
- One X handle (the platform's creator) is linked to 2,328 agents; the next largest handle controls 4. This is a measured one-operator-many-agents case, which the authors treat as system activity in a robustness check.
- Episode counts vary from 2,058 to 7,485 across the six (k, w) settings tested.

## Methods and models

Incremental crawler into a graph database; episode extraction by sliding window; agent-agent projection weighted by co-participation; power-law fits by Clauset et al.; matched observational lift. Dataset on GitHub (kunmukh/moltgraph) and Hugging Face (kunmukh/MoltGraph).

## Limitations and open questions

Labels are weak proxies from platform moderation, not adjudicated. Exposure comes from 31 snapshots taken about 10.5 hours apart, so it is interval-censored. Associations are observational, not causal. No GNN baselines are reported despite the dataset's stated purpose. Coordination is not intent: agents reacting fast to the same post may be organic agent behaviour.

## Relevance to us

The most direct in-the-wild dataset for this lane: agents only, timestamps at action level, and a known one-operator cluster. A hackathon detector can be tested on whether it recovers the 2,328-agent operator cluster from traces alone. Related Moltbook entry: [[de-marzo-2026-collective]]. Synthetic counterpart: [[orlando-2026-emergent]].
