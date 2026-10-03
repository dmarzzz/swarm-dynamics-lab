---
id: la-cava-2025-machines
type: paper
title: Machines in the Crowd? Measuring the Footprint of Machine-Generated Text on Reddit
authors:
- Lucio La Cava
- Luca Maria Aiello
- Andrea Tagarelli
year: 2025
venue: Online Social Networks and Media (per Semantic Scholar); arXiv preprint
url: https://arxiv.org/html/2510.07226
doi: null
arxiv: '2510.07226'
cite: La Cava, L., Aiello, L. M., & Tagarelli, A. (2025). Machines in the Crowd? Measuring the Footprint of Machine-Generated Text on Reddit. arXiv:2510.07226 (cs.SI).
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: full
relevance: 4
citations: 4 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Runs the zero-shot Fast-DetectGPT detector over 38M comments and 4M submissions from 51 large subreddits (2022-2024), keeping only texts of at least 250 tokens and a 0.99 detection threshold to keep false positives low. Machine-generated text is marginal overall but reaches 6-9% of qualifying comments in some subreddit-months (r/teenagers 8.46%, r/malefashionadvice 7.69%, r/askscience 6.33%), is concentrated in about 2% of active users, and is stylistically warmer and more status-giving than human text, yet receives equal or higher engagement.

## Contribution

A conservative, per-community and per-user picture of machine text on Reddit, adding the observation that production is concentrated in a small set of accounts, which is the population structure a swarm detector would look for.

## Key results

- Measured: after filtering, 9.03M comments and 2.13M submissions analysed; peak subreddit-month MGT shares 6.33% (Information Seeking), 7.69% (Social Support), 1.28% (Discussion, r/politics), 8.46% (Identity), 3.13% (ChitChat).
- Measured: average share of users posting any MGT peaked at about 2% (max 3%); for those users 10-40% of their comments were flagged, about 20% after the initial adoption wave.
- Measured: MGT comments are longer and more compressible than human comments.
- Measured: in 26 of 102 subreddit-months with a significant engagement difference, 25 favoured MGT (Cliff delta about 0.17-0.30); the exception was r/worldnews, June 2023.
- Stated by authors: lowering the detection threshold from 0.99 already doubles the estimated prevalence, so absolute levels are lower bounds.

## Methods and models

PushShift dumps for 51 hand-picked subreddits in five functional categories. Fast-DetectGPT (metric-based, conditional probability curvature) chosen over trained classifiers for speed and domain robustness. Social-dimension classifiers (knowledge, status, support, fun, conflict, similarity) from prior Reddit work; engagement compared with bootstrap Mann-Whitney tests within subreddit-month.

## Limitations and open questions

No calibration of false-positive rate on pre-ChatGPT comments is reported for the 0.99 threshold, so the pre-2022 signal in r/teenagers may be noise or older tools. Short comments (under 250 tokens) are excluded, which is where most bot replies live. Single platform, 51 subreddits. Engagement matching is coarse.

## Relevance to us

Direct evidence that machine text in a large community concentrates in few accounts, so account-level aggregation is the right unit for spotting swarms. Its lower numbers than [[sun-2024-are]] on Reddit show how much threshold and length filters move prevalence estimates. Links to coordinated LLM botnets [[yang-2023-anatomy]] and to agent-only communities [[goyal-2026-social]].
