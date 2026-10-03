---
id: gh-tamsiuhin-botpercent
type: code
title: "BotPercent: community-level estimate of the share of bots among a set of Twitter accounts"
repo: TamSiuhin/BotPercent
url: https://github.com/TamSiuhin/BotPercent
authors: ["Zhaoxuan Tan", "Shangbin Feng", "Melanie Sclar", "Herun Wan", "Minnan Luo", "Yejin Choi", "Yulia Tsvetkov"]
year: 2023
language: Python
license: "none stated"
stars: 22
last_commit: 2023-02-02
topics: [swarm-detection]
added_by: dmarz/sd-code-data
accessed: 2026-10-03
read_depth: skim
relevance: 4
papers: []
---

## Summary

Demo code for 'BotPercent: Estimating Bot Populations in Twitter Communities' (arXiv 2302.00381, abstract read). It trains on the merge of nine public bot datasets (Cresci-15, Gilani-17, Cresci-17, Midterm-18, Cresci-stock-18, Cresci-rtbust-19, Botometer-feedback-19, TwiBot-20, TwiBot-22), combines feature-, text- and graph-based models, and calibrates confidence across models so that the averaged probability estimates the bot fraction of a community rather than labelling individuals. The paper reports bot rates that vary strongly across communities and over time.

## What it can do for us

The right target for 'how many agents are in this population', a base-rate question that individual classifiers answer badly because of calibration. The calibration-across-models idea transfers to estimating agent prevalence on a platform.

## Run notes

Not run (needs a Twitter API key and a Random Forest checkpoint from Google Drive; the Twitter API is no longer available on those terms).

## Limitations

Pre-LLM training data; no evidence it estimates LLM-agent populations. Marked 'work in progress', last commit 2023-02-02, no licence file.
