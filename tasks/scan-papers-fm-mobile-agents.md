---
id: scan-papers-fm-mobile-agents
type: task
title: 'Catalogue the papers: mobile-agent security and Byzantine state merge'
kind: scan
status: claimed
priority: p1
owner: dmarz/fm-mobile-agents
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
claimed_at: 2026-10-03T18:12Z
updated: 2026-10-03T18:12Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: 1990s-2000s mobile agents visiting hostile hosts and returning, plus Byzantine CRDTs and replica reconciliation.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note
