---
id: data-moltbook-observatory-2026
type: dataset
title: "Moltbook Observatory Archive: incremental, date-partitioned dump of the agent-only social network Moltbook"
authors: ["Sushant Gautam", "Annika W. Olstad", "Klas H. Pettersen", "Michael A. Riegler"]
year: 2026
url: https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive
license: "MIT"
size: "Paper snapshot 2026-04-15: 175,886 agents, 2,615,098 posts, 1,213,007 comments, 6,730 submolts; dataset keeps growing (220 daily post files through 2026-09-11 when accessed)"
format: "Date-partitioned Parquet; subsets posts, agents, comments, submolts, snapshots, word_frequency"
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: ran
relevance: 4
papers: []
---

## Summary

Continuous passive capture of Moltbook through its API by SimulaMet, described in arXiv 2605.13860 (Gautam et al., abstract read): the documented release covers 78 days (2026-01-27 to 2026-04-14) with 2,615,098 posts and 1,213,007 comments from 175,886 posting agents. Agent rows include karma, follower counts, an is_claimed flag and the owner's X handle when the agent was claimed. The card warns that comment coverage is partial and mutable fields (scores, karma) change after collection. Companion analysis code is kelkalot/moltbook-observatory-paper (MIT), which includes near-duplicate detection and agent scoring modules.

## Access

`load_dataset('SimulaMet/moltbook-observatory-archive', 'posts', data_files='data/posts/2026-09-10.parquet')`, or download single Parquet files from `https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive/resolve/main/data/<table>/<date>.parquet`. No registration.

Ran 2026-10-03: loaded `data/posts/2026-09-10.parquet` (4,526 posts, 482 agents; median 2 posts per agent, max 398) and all 207 `data/agents/*.parquet` files with pandas. After deduplicating agent ids: 182,860 agents, 129,268 with is_claimed = 1, 55,551 with a non-empty owner X handle, held by 55,545 distinct handles; only 10 handles own 2 agents and none owns more. So the public owner field shows essentially one agent per claimed X account and cannot reveal multi-agent operators. The eight highest-volume agents on 2026-09-10 posted at a near-constant ~180 s cadence (65-93% of intervals in 150-210 s) and all share one 2.7-hour gap (07:16 to 09:58 UTC) that is also the largest platform-wide gap in posting that day, so it is a platform or collection outage, not agent behaviour. I also ran [[gh-qut-digital-observatory-coordination-network-toolkit]] on this day (results there).

## Relevance to us

Largest open record of a population of deployed LLM agents interacting in public, with timestamps fine enough for timing fingerprints ([[li-2026-moltbook]]) and coordination networks ([[mukherjee-2026-moltgraph]]). My owner-handle count is a negative result for operator attribution through platform metadata: the claim mechanism caps visible ownership at one agent per handle, so Sybil operators must be found from behaviour. Related: [[data-moltbook-takschdube-2026]], [[data-moltgraph-2026]], [[de-marzo-2026-collective]].
