---
id: synthesis-swarm-detection-methods
type: task
title: 'Synthesis: taxonomy of swarm-detection methods and the honeypot design space'
kind: synthesis
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

Context from dmarz: find all papers and results on detecting AI agent swarms in the wild: many LLM or autonomous agents (possibly coordinated, possibly Sybils of one operator) acting on social platforms, the web, markets, chains or other agents. One idea of many is honeypots that attract and identify swarms; treat it as one branch, not the frame. Look for detection methods, measured base rates of agent activity in the wild, evasion results, and negative results that show detection fails. Write 3-synthesis/swarm-detection-methods.md: a taxonomy of every detection approach found, what each has measured in the wild versus in the lab, known evasions, and a section on the honeypot design space (what bait attracts agents, what tells them apart from humans, what links many agents to one operator).

## Done when

- 3-synthesis/swarm-detection-methods.md exists, cites library entries as [[id]], and passes check.

## Coverage note
