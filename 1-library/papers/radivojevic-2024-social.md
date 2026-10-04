---
id: radivojevic-2024-social
type: paper
title: 'Social Media Bot Policies: Evaluating Passive and Active Enforcement'
authors:
- Kristina Radivojevic
- Christopher McAleer
- Catrell Conley
- Cormac Kennedy
- Paul Brenner
year: 2024
venue: arXiv preprint
url: https://arxiv.org/abs/2409.18931
doi: null
arxiv: '2409.18931'
cite: 'Radivojevic, K., McAleer, C., Conley, C., Kennedy, C., & Brenner, P. (2024). Social Media Bot Policies: Evaluating Passive and Active Enforcement. arXiv preprint arXiv:2409.18931.'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

The authors read the bot and AI-content policies of eight platforms (X, Instagram, Facebook, Threads, TikTok, Mastodon, Reddit, LinkedIn) and then tried to operate a multimodal-foundation-model bot built with Selenium on each. Despite explicit anti-bot policies, none of the platforms detected or stopped their bots.

## Contribution

An active audit of platform-side detection: a field test, not a classifier benchmark, and the result is that deployed defences missed a simple agent on every platform tested.

## Key results

- 8 of 8 platforms failed to detect and prevent the authors' MFM bots (abstract).
- Policies exist on all platforms; enforcement did not catch the test bots.

## Methods and models

Policy review plus deployment of a Selenium-driven bot using a multimodal model on each platform. Abstract-level read.

## Limitations and open questions

Few bots, short time window, and platforms may act later or on scale; a single bot is not a swarm. Preprint.

## Relevance to us

A negative result for platform detection of single agents in 2024, so swarm detection cannot assume platforms already filter them. Same group: [[radivojevic-2024-llms]].
