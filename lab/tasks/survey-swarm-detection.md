---
id: survey-swarm-detection
type: task
title: 'Survey: detecting AI agent swarms in the wild'
kind: survey
status: open
priority: p1
owner: null
for: null
created: '2026-10-03'
created_by: dmarz/sd
depends_on:
- scan-papers-sd-bots
- scan-papers-sd-honeypots
- scan-papers-sd-web-agents
- scan-papers-sd-coordination
- scan-papers-sd-ai-content
- scan-papers-sd-attribution
- scan-papers-sd-onchain
- scan-threads-sd-informal
- scan-code-sd-code-data
topics:
- swarm-detection
---

## Goal

Context from dmarz: find all papers and results on detecting AI agent swarms in the wild: many LLM or autonomous agents (possibly coordinated, possibly Sybils of one operator) acting on social platforms, the web, markets, chains or other agents. One idea of many is honeypots that attract and identify swarms; treat it as one branch, not the frame. Look for detection methods, measured base rates of agent activity in the wild, evasion results, and negative results that show detection fails. Prior-art survey across all swarm-detection scans, organised by where detection happens (platform, web edge, chain, inside the agent conversation, deliberate traps) and by signal type (content, behaviour, coordination, identity).

## Done when

- `python3 scripts/lab.py gate survey-swarm-detection` reports nothing missing.
- Review task opened for another researcher.

## Coverage note
