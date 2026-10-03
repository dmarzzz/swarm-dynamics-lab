---
id: mukherjee-2026-moltgraph
type: paper
title: "MoltGraph: A Longitudinal Temporal Graph Dataset of Moltbook for Coordinated-Agent Detection"
authors: ["Kunal Mukherjee", "Cuneyt Gurcan Akcora", "Murat Kantarcioglu"]
year: 2026
venue: "ACM Conference on AI and Agentic Systems (CAIS 2026); arXiv"
url: https://arxiv.org/html/2603.00646
doi: "10.1145/3786335.3813177"
arxiv: "2603.00646"
cite: "Mukherjee, K., Akcora, C. G., & Kantarcioglu, M. (2026). MoltGraph: A Longitudinal Temporal Graph Dataset of Moltbook for Coordinated-Agent Detection. In Proceedings of the ACM Conference on AI and Agentic Systems (CAIS '26), San Jose, CA, USA. https://doi.org/10.1145/3786335.3813177. arXiv:2603.00646."
topics: [swarm-detection, llm-agent-swarms, sybil-resistance]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: [data-moltgraph-2026]
---

## Summary

Builds a temporal heterogeneous graph of Moltbook, the agent-only social network, from a crawler into Neo4j: 30 days (2026-01-28 to 2026-02-26), 11,874 agents, 870 submolts, 57,465 posts, 101,500 comments and 162,024 temporal edges of 6 types, plus periodic feed snapshots as an exposure proxy. Coordination episodes are defined as at least k distinct agents commenting or upvoting the same target within a window of w minutes, early in the target's life; weak labels come from the platform's isSpam flag plus bursty engagement. Measured: the top 1% of agents hold 29.00% of engagement and 45.76% of betweenness in the coordination graph; 98.33% of coordination episodes last under 24 hours (mean about 4 minutes); matched against same-submolt, same-period controls, coordinated posts show 506.35% higher early engagement and 242.63% higher snapshot exposure.

## Contribution

First graph dataset built specifically for detecting coordinated agents on an agent-native platform, with exposure signals to ask whether coordination changes what communities see. It ports the coordination-network method of Pacheco et al. from human platforms to an agent population.

## Key results

- 11,874 agents, 57,465 posts, 101,500 comments, 162,024 temporal edges over 30 days (Table 2).
- Giant component covers 0.97-0.99 of each graph view; mean clustering 0.61-0.75; fitted degree tail exponents 1.95-2.83 but goodness-of-fit is poor, so the authors decline to claim a pure power law.
- Top 1% of agents: 29.00% of engagement; 45.76% (agent-agent coordination), 58.30% (agent-post) and 65.32% (submolt) of betweenness mass.
- 98.33% of coordination episodes are shorter than 24 h; post-centred episodes average about 4 minutes.
- Coordinated posts: +506.35% early engagement and +242.63% snapshot exposure versus matched controls (observational association, not causal). Excluding known platform-maintenance accounts lowers the lift but keeps its sign (Table 7).
- Snapshots are about twice daily (mean gap 10.54 h), so exposure is interval-censored.

## Methods and models

Crawler over the public Moltbook API with idempotent upserts and first_seen/last_seen lifetimes; node types Agent, XAccount (owner handle), Submolt, Post, Comment, Snapshot, Crawl; edges POSTED, COMMENTED, REPLIED_TO, UPVOTED, IN_SUBMOLT, SEEN_IN. Episode detection with sliding windows merged per target; agent-agent projection weighted by co-participation and downweighted for large swarms; matched-control lift for exposure.

## Limitations and open questions

Labels are weak: isSpam is the platform's own moderation, not adjudicated ground truth, and coordination as defined (k agents act on a target within w minutes) also catches benign popularity. No detector is trained or evaluated in the paper despite the title; it is a dataset and measurement paper. Several table values did not render in the HTML version I read, so only the numbers stated in the text are recorded here. It does not separate human-steered from autonomous agents (compare [[li-2026-moltbook]]).

## Relevance to us

The closest existing work to 'detect agent swarms in the wild' on a platform where every account is nominally an agent, so the question becomes which agents act as one. Its episode definition is the same co-action-in-a-window idea implemented in [[gh-qut-digital-observatory-coordination-network-toolkit]], and the dataset is the obvious test bed. Related Moltbook data: [[data-moltbook-observatory-2026]], [[data-moltbook-takschdube-2026]]; Moltbook behaviour paper [[de-marzo-2026-collective]].
