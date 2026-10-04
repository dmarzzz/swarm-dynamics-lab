---
id: choi-2025-empirical
type: paper
title: 'An Empirical Study of Group Conformity in Multi-Agent Systems'
authors: [Min Choi, Keonwoo Kim, Sungwon Chae, Sangyeob Baek]
year: 2025
venue: Findings of ACL 2025 (arXiv preprint)
url: https://arxiv.org/abs/2506.01332
doi: 10.18653/v1/2025.findings-acl.265
arxiv: '2506.01332'
cite: 'Choi, M., Kim, K., Chae, S., & Baek, S. (2025). An Empirical Study of Group Conformity in Multi-Agent Systems. Findings of the Association for Computational Linguistics: ACL 2025. arXiv preprint arXiv:2506.01332.'
topics: [llm-agent-swarms, collective-decision]
added_by: shadow/sol-1
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Over 2,500 simulated multi-agent debates on five socially contentious topics, with initially neutral (centrist) LLM agents, to see how stances form and spread. The authors report statistically significant group conformity: agents tend to align with the numerically dominant group, and with agents designated as more intelligent, who exert more influence. The paper frames this as bias amplification risk in anonymous online discussion and calls for diversity and transparency measures. Abstract only; the per-topic numbers and the model list were not read.

## Contribution

A direct Asch-style majority-conformity measurement in LLM debate on contentious (not factual) topics, adding the "more intelligent agent" asymmetry as a second influence channel. Sits with [[weng-2025-do]], [[cho-2025-herd]] and [[bellina-2026-conformity]] in the conformity line, and with [[okawa-2026-emergence]] on bias amplification in debate.

## Key results

- Reported: significant conformity toward numerically dominant groups across 2,500+ debates (abstract; effect sizes not read).
- Reported: agents labelled more intelligent exert greater influence on others' stance adoption.

## Methods and models

Multi-agent debate simulation, five contentious topics, agents assigned a centrist disposition at start, stance tracked over rounds. Models and prompt details not read.

## Limitations and open questions

- Abstract-level read. Unknown whether the "numerically dominant" effect was separated from model prior (the [[zhou-2025-pimmur]] and [[yang-2026-when]] critique applies).
- Contentious topics have no ground truth, so conformity cannot be scored as right or wrong, unlike [[pavlova-2026-flag]].

## Relevance to us

Background for any majority-size manipulation in an LLM population; a cheap replication target (vary majority fraction, measure switch probability) that the hackathon could run with open models.
