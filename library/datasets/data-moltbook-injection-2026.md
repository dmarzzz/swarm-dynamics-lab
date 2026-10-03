---
id: data-moltbook-injection-2026
type: dataset
title: 'Moltbook AI-to-AI Injection Dataset: 4,209 prompt injections harvested from 47,735 Moltbook agent posts and comments'
authors: [David Keane]
year: 2026
url: https://huggingface.co/datasets/DavidTKeane/moltbook-ai-injection-dataset
license: CC-BY-4.0
size: 15,200 posts + 32,535 comments (100 MB raw JSON); 4,209 injection records (datasets-server viewer 4,209 rows, 1,115,663 bytes)
format: 'JSON: all_posts_with_comments.json (raw), injections_found.json, injections_test_suite.json, injection_stats.json, plus collection and keyword-search scripts'
topics: [llm-agent-swarms, fork-merge-security, swarm-detection]
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

MSc cybersecurity thesis dataset (NCI, Ireland) scraped from Moltbook, the AI-agent social network, frozen 2026-02-27. A keyword scan of 47,735 items found 4,209 injections (18.85%), labelled into seven categories: PERSONA_OVERRIDE 2,745, COMMERCIAL_INJECTION 1,104, SOCIAL_ENGINEERING 370, INSTRUCTION_INJECTION 203 and smaller ones. One agent, `moltshellbroker`, wrote 1,137 (27%). Labels come from keyword matching, not human annotation. The card notes the January 2026 Moltbook database breach means some "agents" may have been human-controlled. It cites Greshake et al. [[greshake-2023-not]] as its research basis.

## Access

Public, ungated, on Hugging Face. CC-BY-4.0. Not downloaded here.

## Relevance to us

Real agent-to-agent injection traffic in the wild, with a single dominant actor responsible for over a quarter of it: a ready labelled set for injection-propagation and coordinated-actor detection. Pairs with the other Moltbook corpora such as [[data-moltgraph-2026]] and [[li-2026-moltbook]] on human influence.
