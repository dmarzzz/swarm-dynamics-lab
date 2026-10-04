---
id: gh-ethanbwang-fp-agent
type: code
title: "fp-agent: honey website, agent data collection and XGBoost classifiers for fingerprinting AI browsing agents"
repo: ethanbwang/fp-agent
url: https://github.com/ethanbwang/fp-agent
authors: ["Ethan Wang", "Zubair Shafiq", "Yash Vekaria"]
year: 2026
language: "Python"
license: "none stated"
stars: 4
last_commit: 2026-08-28
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: skim
relevance: 4
papers: [wang-2026-fp-agent]
---

## Summary

Code for [[wang-2026-fp-agent]], in three parts per the README: `honey_website` (site and web server with FingerprintJS plus a custom behavioural event logger), `data_collection` (automation that drives each browsing agent through flight, shopping and forum tasks), and `classifier_training` (featurisation, XGBoost training, saved classifiers for browser, behavioural and combined feature sets, held-out-agent and figure scripts). Data is on OSF.

## What it can do for us

Gives typing, scrolling and pointer-teleport features and trained classifiers that separate seven commercial browsing agents from humans. A starting point for a per-session "is this an agent" flag in a swarm honeypot.

## Run notes

Not run. I read the README and the file tree only.

## Limitations

No licence file. Classifiers are closed-world over the seven 2026 agent versions studied; behavioural features degrade on unseen tasks per the paper.
