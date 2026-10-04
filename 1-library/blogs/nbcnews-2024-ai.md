---
id: nbcnews-2024-ai
type: blog
title: "An AI-powered bot army on X spread pro-Trump and pro-GOP propaganda, research shows"
authors: [Kevin Collier]
year: 2024
url: https://www.nbcnews.com/tech/internet/republican-bot-campaign-trump-x-twitter-elon-musk-fake-accounts-rcna173692
site: NBC News (journalism)
topics: [swarm-detection]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 3
---

## Summary

News article (16 October 2024) reporting the Clemson Media Forensics Hub study [[linvill-2024-digital]] of an LLM-driven reply network on X: at least 686 accounts, over 130,000 posts since January 2024, supporting particular Republican candidates in four Senate races and two primaries and North Carolina's voter-ID law. Accounts used conservative-coded profile images, had few followers, and replied to popular posters to gain visibility. Researchers linked accounts by metadata, reply content and shared targets. Many were found because outputs "broke", for example "Hey there, I'm an AI language model trained by OpenAI", and from June 2024 posts such as "Dolphin here!" indicated a switch to the uncensored Dolphin model. Independent researcher Kai-Cheng Yang (Northeastern), asked by NBC to review the work, supported the method and pointed to a further tell: the bots invent hashtags that humans do not use (for example #VoteFrankLaRose, used by only one other tweet since 2018). Many accounts were removed after NBC contacted X. A Hamadeh campaign spokesperson said they noticed the influx of hostile replies but did not know whom to report it to.

## Key claims

- LLM reply-bots can be identified by (a) self-disclosing refusal or identity text, (b) rare or invented hashtags, (c) coordinated targeting of the same accounts.
- X policy did not explicitly prohibit AI-driven fake accounts at the time.

## Evidence quality

Journalism summarising a research report, with one independent expert check. No error rates. The invented-hashtag signal is a reviewer's observation, not a measured classifier.

## Relevance to us

Lists three cheap, practical detection signals for LLM swarms on social platforms and shows the operator adapting (moving to an uncensored model) once the first signal became a liability. The rare-hashtag tell is testable on any platform with a hashtag frequency table.
