---
id: scan-papers-sd-web-agents
type: task
title: 'Catalogue the papers: detecting browser agents, computer-use agents and AI crawlers on the web'
kind: scan
status: claimed
priority: p0
owner: dmarz/sd-web-agents
for: null
created: '2026-10-03'
created_by: dmarz/sd
depends_on: []
topics:
- swarm-detection
claimed_at: 2026-10-03T18:19Z
updated: 2026-10-03T18:19Z
---

## Goal

Context from dmarz: find all papers and results on detecting AI agent swarms in the wild: many LLM or autonomous agents (possibly coordinated, possibly Sybils of one operator) acting on social platforms, the web, markets, chains or other agents. One idea of many is honeypots that attract and identify swarms; treat it as one branch, not the frame. Look for detection methods, measured base rates of agent activity in the wild, evasion results, and negative results that show detection fails. This task: Distinguishing automated browser and computer-use agents and AI crawlers from humans: bot management, behavioural and TLS/browser fingerprinting, CAPTCHAs and their failure against multimodal models, agent authentication schemes (signed agent requests), and traffic measurements of AI crawlers.

## Done when

- At least 15 entries catalogued with topic `swarm-detection`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note
