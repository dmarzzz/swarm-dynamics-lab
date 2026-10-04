---
id: li-2026-moltbook
type: paper
title: "The Moltbook Illusion: Separating Human Influence from Emergent Behavior in AI Agent Societies"
authors: ["Ning Li"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2602.07432
doi: null
arxiv: "2602.07432"
cite: "Li, N. (2026). The Moltbook Illusion: Separating Human Influence from Emergent Behavior in AI Agent Societies. arXiv preprint arXiv:2602.07432."
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

Asks which Moltbook activity is autonomous and which is human-driven. The method uses the periodic 'heartbeat' of the OpenClaw agent framework: an agent that posts on its own schedule has regular inter-post intervals, so the coefficient of variation (CoV) of intervals separates autonomous agents (CoV < 0.5) from human-influenced ones (CoV > 1.0). Applied to 226,938 posts and 447,043 comments from 55,932 agents over 14 days, it labels 15.3% of active agents autonomous and 54.8% human-influenced. A 44-hour platform shutdown is used as a natural experiment: human-influenced agents returned first. None of six viral phenomena traced to a clearly autonomous agent. It also reports industrial bot farming: four accounts produced 32% of all comments with sub-second coordination, falling from 32.1% to 0.5% of activity after platform intervention.

## Contribution

A timing fingerprint that attributes agent-platform activity to human operators versus autonomous schedules, with a natural-experiment validation, and a measured instance of a few accounts flooding an agent network.

## Key results

- 55,932 agents, 226,938 posts, 447,043 comments, 14 days (abstract).
- 15.3% of active agents autonomous (CoV < 0.5), 54.8% human-influenced (CoV > 1.0).
- 0 of 6 viral phenomena from a clearly autonomous agent; 4 from irregular-timing accounts, 1 platform-scaffolded, 1 mixed.
- 4 accounts made 32% of comments with sub-second coordination; share fell from 32.1% to 0.5% after intervention.
- Reply-chain content decay half-life 0.58 conversation depths for human-seeded threads versus 0.72 for autonomous threads.

## Methods and models

Inter-post interval CoV per agent, thresholds 0.5 and 1.0; natural experiment around a 44-hour shutdown; thread tracing of viral content. Read from the abstract only; the HTML full text was not available on arXiv and I did not read the PDF.

## Limitations and open questions

Only the abstract was read. Inference from my own run (see [[data-moltbook-observatory-2026]]): CoV is sensitive to collection or platform gaps. On 2026-09-10 the eight highest-volume agents posted at a near-constant 180 s cadence (65-93% of intervals in 150-210 s, CoV 0.26-0.42 within sessions) but have whole-day CoV 2.0-2.5 because one platform-wide 2.7-hour gap (07:16 to 09:58 UTC) appears in every series; a naive whole-day CoV would call these clearly scheduled agents 'human-influenced'. Whether the paper handles gaps this way is not checked.

## Relevance to us

Direct evidence that on an 'agent-only' network most visible behaviour was human-steered and a handful of accounts dominated comments: the swarm to detect may be humans running agents, not agents. The timing method is cheap to run on any timestamped trace. Pairs with [[mukherjee-2026-moltgraph]] (coordination episodes) and [[gh-palisaderesearch-llm-honeypot]] (latency as the human/agent separator).
