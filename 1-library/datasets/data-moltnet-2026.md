---
id: data-moltnet-2026
type: dataset
title: 'MoltNet: integrated Moltbook corpus of 1.04M posts, 3.16M comments, 149,574 AI-agent profiles and 18,244 communities with longitudinal histories (Jan 27 to Feb 28, 2026)'
authors:
- Yi Feng
- Chen Huang
- Zhibo Man
- Ryner Tan
- Long P. Hoang
- Shaoyang Xu
- Wenxuan Zhang
year: 2026
url: https://huggingface.co/datasets/iNLP-Lab/Moltbook-MoltNet
license: CC-BY-4.0
size: 5,417,798 rows, 1,621,082,194 bytes (1,044,455 posts; 3,161,324 comments; 149,574 agents; 18,244 submolts)
format: Parquet tables (posts, comments, agents, submolts, posts_fully_connected) with JSON-encoded history fields
topics:
- llm-agent-swarms
- swarm-detection
added_by: dmarz/hf-sweep
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Dataset for "MoltNet: Understanding Social Behavior of AI Agents in the Agent-Native MoltBook" (Feng et al., arXiv 2602.13458). Merges ten independent Moltbook crawls (including [[data-lysandrehooh-moltbook-2026]], [[data-lnajt-moltbook-2026]], [[data-trustairlab-moltbook-2026]], [[data-joinmassive-moltbook-2026]]) into one deduplicated set with time series per entity: agent karma, follower and persona-description history, post vote history, community subscriber history. Agent rows carry the human owner's X handle, bio and follower count; 44K posts carry TrustAIRLab topic and toxicity labels. No bot/human or operator labels.

## Access

https://huggingface.co/datasets/iNLP-Lab/Moltbook-MoltNet, not gated, CC-BY-4.0; also check licences of the merged source crawls.

## Relevance to us

The owner-X-handle field links agents to human operators, which makes it usable for operator-attribution and many-agents-one-operator studies. The history fields support drift and coordination analysis that single snapshots cannot. See also [[data-jscmp4-moltbook-2026]] for the longer window.
