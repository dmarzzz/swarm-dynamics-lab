---
id: data-moltbook-takschdube-2026
type: dataset
title: "Moltbook longitudinal dataset (Taksch Dube): timestamped crawls with derived social and reply graphs"
authors: ["Taksch Dube"]
year: 2026
url: https://huggingface.co/datasets/takschdube/moltbook-dataset
license: "CC-BY-4.0"
size: "As of 2026-10-03 07:32 UTC: 420,936 posts and 3,703,029 comments collected (platform totals reported 4,364,385 posts, 13,501,756 comments), 57,030 agents, 825,530 social-graph edges, 928,158 reply-graph edges, 33,350 listed submolts"
format: "JSON and CSV: raw/posts.json, raw/posts_full.json, raw/submolts.json, derived/agents.json, social_graph.json, reply_graph.json, activity_timeline.json, fetch_completeness.json"
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

Automatically updated Moltbook crawl published as timestamped snapshots, with derived agent table, social graph, reply graph and activity timeline; companion code at github.com/takschdube/moltbook-dataset (6 stars, updated 2026-10-03). The card's platform totals imply the collected share is about 10% of posts and 27% of comments, and a fetch_completeness file documents coverage.

## Access

`load_dataset('takschdube/moltbook-dataset', 'reply_graph')` or download the JSON files from the Hugging Face repo. Not loaded here.

## Relevance to us

Ready-made reply graph for coordination analysis and a longer time span than [[data-moltgraph-2026]]; useful to check whether coordination clusters found on one Moltbook crawl persist across others. Incomplete coverage limits any base-rate claim. Related: [[data-moltbook-observatory-2026]].
