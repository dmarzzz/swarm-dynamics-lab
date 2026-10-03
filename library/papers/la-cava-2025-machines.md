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

## Notes from dmarz/sd-ai-content

This lane catalogued the same source independently (added_by dmarz/sd-ai-content, accessed 2026-10-03). Its distinct content:

- Frontmatter `venue` in this lane's version: Online Social Networks and Media (per Semantic Scholar); arXiv preprint
- Frontmatter `url` in this lane's version: https://arxiv.org/html/2510.07226
- Frontmatter `cite` in this lane's version: La Cava, L., Aiello, L. M., & Tagarelli, A. (2025). Machines in the Crowd? Measuring the Footprint of Machine-Generated Text on Reddit. arXiv:2510.07226 (cs.SI).
- Frontmatter `read_depth` in this lane's version: full
- Frontmatter `citations` in this lane's version: 4 (Semantic Scholar, 2026-10-03)

### Summary

Runs the zero-shot Fast-DetectGPT detector over 38M comments and 4M submissions from 51 large subreddits (2022-2024), keeping only texts of at least 250 tokens and a 0.99 detection threshold to keep false positives low. Machine-generated text is marginal overall but reaches 6-9% of qualifying comments in some subreddit-months (r/teenagers 8.46%, r/malefashionadvice 7.69%, r/askscience 6.33%), is concentrated in about 2% of active users, and is stylistically warmer and more status-giving than human text, yet receives equal or higher engagement.

### Contribution

A conservative, per-community and per-user picture of machine text on Reddit, adding the observation that production is concentrated in a small set of accounts, which is the population structure a swarm detector would look for.

### Key results

- Measured: after filtering, 9.03M comments and 2.13M submissions analysed; peak subreddit-month MGT shares 6.33% (Information Seeking), 7.69% (Social Support), 1.28% (Discussion, r/politics), 8.46% (Identity), 3.13% (ChitChat).
- Measured: average share of users posting any MGT peaked at about 2% (max 3%); for those users 10-40% of their comments were flagged, about 20% after the initial adoption wave.
- Measured: MGT comments are longer and more compressible than human comments.
- Measured: in 26 of 102 subreddit-months with a significant engagement difference, 25 favoured MGT (Cliff delta about 0.17-0.30); the exception was r/worldnews, June 2023.
- Stated by authors: lowering the detection threshold from 0.99 already doubles the estimated prevalence, so absolute levels are lower bounds.

### Methods and models

PushShift dumps for 51 hand-picked subreddits in five functional categories. Fast-DetectGPT (metric-based, conditional probability curvature) chosen over trained classifiers for speed and domain robustness. Social-dimension classifiers (knowledge, status, support, fun, conflict, similarity) from prior Reddit work; engagement compared with bootstrap Mann-Whitney tests within subreddit-month.

### Limitations and open questions

No calibration of false-positive rate on pre-ChatGPT comments is reported for the 0.99 threshold, so the pre-2022 signal in r/teenagers may be noise or older tools. Short comments (under 250 tokens) are excluded, which is where most bot replies live. Single platform, 51 subreddits. Engagement matching is coarse.

### Relevance to us

Direct evidence that machine text in a large community concentrates in few accounts, so account-level aggregation is the right unit for spotting swarms. Its lower numbers than [[sun-2024-are]] on Reddit show how much threshold and length filters move prevalence estimates. Links to coordinated LLM botnets [[yang-2023-anatomy]] and to agent-only communities [[goyal-2026-social]].
