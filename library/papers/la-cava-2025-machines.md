---
id: la-cava-2025-machines
type: paper
title: Machines in the Crowd? Measuring the Footprint of Machine-Generated Text on Reddit
authors:
- Lucio La Cava
- Luca Maria Aiello
- Andrea Tagarelli
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2510.07226
doi: null
arxiv: '2510.07226'
cite: La Cava, L., Aiello, L. M., & Tagarelli, A. (2025). Machines in the Crowd? Measuring the Footprint of Machine-Generated Text on Reddit. arXiv preprint arXiv:2510.07226.
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

A large measurement of machine-generated text on Reddit across 51 subreddits from 2022 to 2024, using a statistical MGT detector with a deliberately conservative threshold. Synthetic text is marginal overall but reaches up to 9% of content in some communities in some months, is concentrated in technical and social-support subreddits, and is produced by a small fraction of users; it gets engagement comparable to human posts.

## Contribution

A platform-scale base rate for LLM text in a discussion community, plus the finding that MGT is concentrated in few accounts, which is the signature one would expect from operated agents.

## Key results

- Conservative estimate: MGT marginal overall, peaks up to 9% in some communities and months.
- MGT is more prevalent in technical-knowledge and social-support subreddits and concentrated in a small fraction of users.
- MGT carries warmth and status-giving signals typical of assistant language, and receives engagement comparable to or above human text.

## Methods and models

Statistical zero-shot MGT detection over two years of posts and comments in 51 subreddits; concentration and engagement analyses. Abstract-level read.

## Limitations and open questions

Text detector false positive and negative rates in the wild are uncertain; a per-text estimate does not separate humans using LLMs from autonomous agents. Unreviewed preprint.

## Relevance to us

Gives a Reddit base rate to set beside the Twitter image-based rates in [[ricker-2024-ai]] and [[yang-2024-characteristics]]. The concentration-in-few-users finding suggests pivoting from text to account clusters, as in [[yang-2023-anatomy]].
