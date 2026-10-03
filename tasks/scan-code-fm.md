---
id: scan-code-fm
type: task
title: Catalogue code and benchmarks for agent injection, merge poisoning and multi-agent attacks
kind: scan
status: claimed
priority: p1
owner: dmarz/fm-code-bench
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

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: repos and benchmarks.

## Done when

- At least 12 code repos or benchmarks catalogued with topic `fork-merge-security`.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note
