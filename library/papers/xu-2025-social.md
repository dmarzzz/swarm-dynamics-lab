---
id: xu-2025-social
type: paper
title: "Social media warfare: investigating human-bot engagement in English, Japanese and German during the Russo-Ukrainian war on Twitter and Reddit"
authors: [Wentao Xu, Kazutoshi Sasahara, Jianxun Chu, Bin Wang, Wenlu Fan, Zhiwen Hu]
year: 2025
venue: "EPJ Data Science"
url: https://epjdatascience.springeropen.com/articles/10.1140/epjds/s13688-025-00528-y
doi: 10.1140/epjds/s13688-025-00528-y
arxiv: null
cite: "Xu, W., Sasahara, K., Chu, J., Wang, B., Fan, W., & Hu, Z. (2025). Social media warfare: investigating human-bot engagement in English, Japanese and German during the Russo-Ukrainian war on Twitter and Reddit. EPJ Data Science, 14(1), 10. https://doi.org/10.1140/epjds/s13688-025-00528-y"
topics: [swarm-detection]
added_by: shadow/sol-w5
accessed: 2026-10-03
read_depth: skim
relevance: 2
citations: "3 (Crossref, 2026-10-03)"
code: []
---

## Summary

Measurement study of bot activity around one event, the Bucha killings, in the first month of the Russo-Ukrainian war (28 Mar to 30 Apr 2022), compared across language communities. X data: 2.34M English tweets (86.7% retweets, 554k users) and 418k Japanese tweets (88.7% retweets, 89.5k users) collected with twarc; Reddit: about 1.05M English and 13k German comments from Pushshift. Stance on X from Louvain communities on the 3-core retweet network (coder check kappa 0.70); stance on Reddit from a T5-small labelling agent with few-shot examples (coder kappa 0.73). Bots on X from Botometer v4 (CAP for English, universal score for Japanese) at threshold 0.7; on Reddit from an open-source rule-based detector. Headline numbers: in the Japanese X retweet network (27k nodes), 67.4% pro-Ukraine bots, 19.2% pro-Ukraine humans, 11.0% pro-Russia bots, 2.4% pro-Russia humans; English (100k nodes) 57.7%, 31.6%, 7.5%, 3.2%. Bot cascades are larger and deeper than human ones; Japanese bots reach further into human engagement than English ones on retweet pervasiveness, reply rate and human-to-bot rate; English activity Granger-causes Japanese (X) and German (Reddit) activity. On Reddit humans dominate (76.5% German, 79.9% English) but bots act as reply hubs. Co-retweet networks in 15-55 s windows are mostly bots.

## Contribution

Cross-language comparison of bot share and bot-human engagement during a conflict, extending the English-only literature with Japanese and German communities, and borrowing engagement metrics (RTP, RR, H2BR) from earlier election-bot work.

## Key results

- Bot share at Botometer > 0.7 is a majority of X users in both language communities; Japanese users score significantly more bot-like than English ones (t-test p < 0.01).
- Bots exceed humans on cascade size and depth on X; Japanese bots exceed English bots on both.
- Co-retweet networks (15-55 s windows) dominated by pro-Ukraine bots; up to 2850 pro-Ukraine bots in the 15 s English window.
- English toxicity higher than Japanese overall (Perspective API on machine-translated text).

## Methods and models

Retweet and reply networks, k-core plus Louvain stance, Botometer v4 thresholding, cascade size/depth, Granger causality, co-action networks in short time windows, Perspective API toxicity after machine translation.

## Limitations and open questions

The bot labels are the weak point. A Botometer threshold of 0.7 applied to a whole population yields "majority bots", which is exactly the base-rate failure documented in [[gallwitz-2022-investigating]] and [[rauchfleisch-2020-false]]; the Japanese universal score was never validated on Japanese accounts here. Labelling top accounts such as the Kyiv Independent and Ukraine's foreign minister as "top-indegree bots" is a red flag. The Reddit detector is a six-feature GitHub tool with no reported validation. Treat bot-share numbers as Botometer-score distributions, not prevalence.

## Relevance to us

Low as evidence, useful as a cautionary example: a 2025 peer-reviewed study still reports bot prevalence from thresholded Botometer scores, so our swarm-detection survey should flag this pattern. The co-retweet-in-short-windows construction is the same coordination signal formalised in [[pacheco-2021-uncovering]] and implemented in [[gh-qut-digital-observatory-coordination-network-toolkit]]. LLM-era botnet contrast: [[yang-2023-anatomy]].
