---
id: mukherjee-2026-moltgraph
type: paper
title: 'MoltGraph: A Longitudinal Temporal Graph Dataset of Moltbook for Coordinated-Agent Detection'
authors:
- Kunal Mukherjee
- Cuneyt Gurcan Akcora
- Murat Kantarcioglu
year: 2026
venue: Proceedings of the ACM Conference on AI and Agentic Systems (CAIS '26)
url: https://arxiv.org/html/2603.00646
doi: 10.1145/3786335.3813177
arxiv: '2603.00646'
cite: 'Mukherjee, K., Akcora, C. G., & Kantarcioglu, M. (2026). MoltGraph: A Longitudinal Temporal Graph Dataset of Moltbook for Coordinated-Agent Detection. In Proceedings of the ACM Conference on AI and Agentic Systems (pp. 800–811). ACM.'
topics:
- swarm-detection
- llm-agent-swarms
- sybil-resistance
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: 3 (Semantic Scholar, 2026-10-03)
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

## Notes from dmarz/sd-code-data

This lane catalogued the same source independently (added_by dmarz/sd-code-data, accessed 2026-10-03). Its distinct content:

- Frontmatter `venue` in this lane's version: ACM Conference on AI and Agentic Systems (CAIS 2026); arXiv
- Frontmatter `cite` in this lane's version: 'Mukherjee, K., Akcora, C. G., & Kantarcioglu, M. (2026). MoltGraph: A Longitudinal Temporal Graph Dataset of Moltbook for Coordinated-Agent Detection. In Proceedings of the ACM Conference on AI and Agentic Systems (CAIS ''26), San Jose, CA, USA. https://doi.org/10.1145/3786335.3813177. arXiv:2603.00646.'
- Frontmatter `citations` in this lane's version: null
- Frontmatter `code` in this lane's version: [data-moltgraph-2026]

### Summary

Builds a temporal heterogeneous graph of Moltbook, the agent-only social network, from a crawler into Neo4j: 30 days (2026-01-28 to 2026-02-26), 11,874 agents, 870 submolts, 57,465 posts, 101,500 comments and 162,024 temporal edges of 6 types, plus periodic feed snapshots as an exposure proxy. Coordination episodes are defined as at least k distinct agents commenting or upvoting the same target within a window of w minutes, early in the target's life; weak labels come from the platform's isSpam flag plus bursty engagement. Measured: the top 1% of agents hold 29.00% of engagement and 45.76% of betweenness in the coordination graph; 98.33% of coordination episodes last under 24 hours (mean about 4 minutes); matched against same-submolt, same-period controls, coordinated posts show 506.35% higher early engagement and 242.63% higher snapshot exposure.

### Contribution

First graph dataset built specifically for detecting coordinated agents on an agent-native platform, with exposure signals to ask whether coordination changes what communities see. It ports the coordination-network method of Pacheco et al. from human platforms to an agent population.

### Key results

- 11,874 agents, 57,465 posts, 101,500 comments, 162,024 temporal edges over 30 days (Table 2).
- Giant component covers 0.97-0.99 of each graph view; mean clustering 0.61-0.75; fitted degree tail exponents 1.95-2.83 but goodness-of-fit is poor, so the authors decline to claim a pure power law.
- Top 1% of agents: 29.00% of engagement; 45.76% (agent-agent coordination), 58.30% (agent-post) and 65.32% (submolt) of betweenness mass.
- 98.33% of coordination episodes are shorter than 24 h; post-centred episodes average about 4 minutes.
- Coordinated posts: +506.35% early engagement and +242.63% snapshot exposure versus matched controls (observational association, not causal). Excluding known platform-maintenance accounts lowers the lift but keeps its sign (Table 7).
- Snapshots are about twice daily (mean gap 10.54 h), so exposure is interval-censored.

### Methods and models

Crawler over the public Moltbook API with idempotent upserts and first_seen/last_seen lifetimes; node types Agent, XAccount (owner handle), Submolt, Post, Comment, Snapshot, Crawl; edges POSTED, COMMENTED, REPLIED_TO, UPVOTED, IN_SUBMOLT, SEEN_IN. Episode detection with sliding windows merged per target; agent-agent projection weighted by co-participation and downweighted for large swarms; matched-control lift for exposure.

### Limitations and open questions

Labels are weak: isSpam is the platform's own moderation, not adjudicated ground truth, and coordination as defined (k agents act on a target within w minutes) also catches benign popularity. No detector is trained or evaluated in the paper despite the title; it is a dataset and measurement paper. Several table values did not render in the HTML version I read, so only the numbers stated in the text are recorded here. It does not separate human-steered from autonomous agents (compare [[li-2026-moltbook]]).

### Relevance to us

The closest existing work to 'detect agent swarms in the wild' on a platform where every account is nominally an agent, so the question becomes which agents act as one. Its episode definition is the same co-action-in-a-window idea implemented in [[gh-qut-digital-observatory-coordination-network-toolkit]], and the dataset is the obvious test bed. Related Moltbook data: [[data-moltbook-observatory-2026]], [[data-moltbook-takschdube-2026]]; Moltbook behaviour paper [[de-marzo-2026-collective]].
