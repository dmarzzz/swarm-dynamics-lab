---
id: scan-papers-fm-ai-control
type: task
title: 'Catalogue the papers: AI control, sub-agent delegation and self-replication'
kind: scan
status: open
priority: p1
owner: null
for: null  # set to a researcher name to direct the task at them
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics: [fork-merge-security, llm-agent-swarms]
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: AI safety framings and defensive design patterns for delegating to and reintegrating untrusted sub-agents.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

