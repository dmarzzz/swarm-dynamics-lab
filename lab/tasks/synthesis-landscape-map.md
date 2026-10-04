---
id: synthesis-landscape-map
type: task
title: Draw the cross-topic landscape map
kind: synthesis
status: done
priority: p0
owner: shadow/sol-atlas
created: '2026-10-03'
created_by: dmarz/setup
depends_on:
- scan-papers-collective-motion
- scan-papers-collective-decision
- scan-papers-swarm-robotics
- scan-papers-marl-emergence
- scan-papers-llm-agent-swarms
topics:
- collective-motion
- collective-decision
- swarm-robotics
- swarm-intelligence
- active-matter
- sync-consensus
- criticality-measurement
- marl-emergence
- llm-agent-swarms
- crowds-and-traffic
claimed_at: 2026-10-04T13:59Z
updated: 2026-10-04T14:29Z
outputs:
- 3-synthesis/landscape.md
---

## Goal

Once the paper scans are in, write 3-synthesis/landscape.md: how the topics connect, which ideas transfer between communities (for example, physics order parameters applied to LLM agent swarms), and where the communities ignore each other. This is the document the team reads to choose survey priorities.

## Done when

- Every topic is placed, with its 3 to 5 most important library entries.
- A section of cross-community transfers that have and have not been tried, each cited.
- A ranked list of surveys to prioritise, with reasons.

## Coverage note

shadow/sol-atlas, 2026-10-04. Output: `3-synthesis/landscape.md`. Done-when progress:

- [x] All 16 topic slugs placed (plus meta), each with 5 library entries and read depth shown (section 2).
- [x] 15 tried transfers and 13 not-tried transfers, each cited (section 3); absence is "not found in our library",
  backed by the concept counts in `5-experiments/studies/shadow/landscape-map/counts.md`.
- [x] Ranked survey list, 13 items plus the llm-agent-swarms revise as item 0 (section 5).

Counts reproducible with `python3 5-experiments/studies/shadow/landscape-map/landscape_counts.py`. 122 distinct
library ids cited, all resolve; every inline read-depth label checked against the entry. No sources re-read.
