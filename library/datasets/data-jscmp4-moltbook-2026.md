---
id: data-jscmp4-moltbook-2026
type: dataset
title: 'Moltbook AI Agent Social Media Corpus: 3.2M posts, 15.9M comments and 99,621 agent profiles from daily crawls, Jan 27 to Jul 3, 2026'
authors:
- Shichao Jia
year: 2026
url: https://huggingface.co/datasets/jscmp4/Moltbook
license: CC-BY-4.0
size: 24,579,270 rows, 3,021,573,468 bytes (3,203,526 posts; 15,881,514 comments; 99,621 agents; 56 daily agent snapshots)
format: Parquet configs posts, comments, agents, agent_snapshots (posts/comments partitioned by month), plus identical raw JSONL (~23 GB)
topics:
- llm-agent-swarms
- swarm-detection
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 5
papers: []
---

## Summary

Continuous daily crawl of Moltbook from launch (2026-01-27) to 2026-07-03, refreshed monthly; scraper at github.com/jscmp4/moltbookscraper. Covers about 90.8% of the platform's post counter. The card documents the mbc-20 bot wave (about 324,000 token-minting posts from about 29,500 agents, Feb 6-17), the Feb 17-18 anti-spam intervention that cut volume about 5x, and a May 6-7 regime change after which `is_spam` is always false. Comments are fetched only for posts with 3+ comments, so small threads are missing by design.

## Access

https://huggingface.co/datasets/jscmp4/Moltbook, not gated, CC-BY-4.0. Cite the dated version; row counts grow monthly.

## Relevance to us

The longest public Moltbook window, with a labelled in-the-wild bot wave (mbc-20) and a moderation natural experiment: a direct swarm-detection benchmark among agents. Use with [[data-moltnet-2026]] and the papers [[li-2026-moltbook]] and [[de-marzo-2026-collective]].
