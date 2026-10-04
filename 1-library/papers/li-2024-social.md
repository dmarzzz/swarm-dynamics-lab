---
id: li-2024-social
type: paper
title: "Social bots spoil activist sentiment without eroding engagement"
authors: [Linda C. Li, Orsolya Vásárhelyi, Balázs Vedres]
year: 2024
venue: Scientific Reports
url: https://www.nature.com/articles/s41598-024-74032-0
doi: 10.1038/s41598-024-74032-0
arxiv: null
cite: "Li, L. C., Vásárhelyi, O., & Vedres, B. (2024). Social bots spoil activist sentiment without eroding engagement. Scientific Reports, 14. https://doi.org/10.1038/s41598-024-74032-0"
topics: [swarm-detection, collective-decision]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: null  # Semantic Scholar rate-limited at access time
code: []
---

## Summary

Observational study of X (Twitter) discourse around Extinction Rebellion protests in November and December 2019, asking how direct interaction with social bots (replying to, mentioning or commenting on a bot) changes humans' subsequent activity and sentiment, as opposed to merely seeing bot content. Bots were identified by combining Botometer (CAP at or above 0.65) with the authors' own trained classifiers, with all analyses repeated at other thresholds in the supplement. Of 93,499 accounts, 44,121 (48%) were classed as bots. Information-flow results: 81% of tweets were replies or retweets, 51% of retweets originated from bots; bot activity was mostly original posting and retweeting other bots (71% of bot retweets were of bots, 35% of all retweets were bot-to-bot), with only 29% of bot retweets amplifying humans; humans retweeted bot and human content in roughly equal measure (54% bot, 46% human). At a stricter threshold (CAP 0.75) bots still accounted for 48% of retweets and 45% of human retweets were of bot content. Seven protest topics were identified with biterm topic models and the flow between bots and humans was found to be strongly topic-dependent. The headline finding (from the title and introduction; the detailed results section was beyond our fetch) is that direct bot encounters shift humans' expressed sentiment toward climate activism, in a direction that depends on the user's initial support, without reducing their tweeting activity, and that the effect on activity depends on bot type.

## Contribution

Moves from macro-level bot prevalence to the micro-level causal question of what happens to a human after talking to a bot during a protest wave, and finds a sentiment effect without an engagement effect.

## Key results

- 48% of accounts (44,121 of 93,499) classified as bots in the XR protest discourse.
- 51% of retweets originated from bots; 71% of bot retweets were of other bots (astroturf-style mutual amplification).
- Humans spread bot-origin and human-origin content about equally (54% versus 46%).
- Direct interaction with bots altered users' climate sentiment conditional on prior stance, while tweeting activity did not erode; bot type moderated the activity effect.

## Methods and models

Twitter data for XR protest period, late 2019; bot detection by Botometer plus custom supervised models with threshold sensitivity analysis; biterm topic modelling for seven topics; comparison of users who directly interacted with bots against those who did not; sentiment and activity measured before and after encounters. Details of the matching or causal design were not in the portion read.

## Limitations and open questions

Bot labels come from classifiers with a chosen threshold, so "48% bots" inherits detector error; one movement, one platform, one two-month window; observational, so the sentiment effect is associational unless the (unread) design controls for selection into bot interaction. Predates LLM-driven bots.

## Relevance to us

A quantitative picture of a pre-LLM bot population at work: half the accounts, mutual retweeting at 71%, humans amplifying bot content as readily as human content. The bot-to-bot amplification ratio is a structural swarm signature usable in detection, and the topic-dependence of bot flow suggests coordination is event-triggered. Useful as a 2019 baseline against which to compare 2026 agent swarms, which coordinate through side channels rather than visible retweets ([[elasky-2026-encoded]]). Related: [[moller-2026-impact]] for an experimental counterpart on perception, [[flood-2026-finding]] for why visible-platform signals may not transfer.
