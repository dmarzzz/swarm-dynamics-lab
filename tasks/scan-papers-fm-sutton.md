---
id: scan-papers-fm-sutton
type: task
title: 'Catalogue the primary sources: Sutton on agents splitting and merging, and prior framings'
kind: scan
status: claimed
priority: p0
owner: dmarz/fm-sutton
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- meta
claimed_at: 2026-10-03T18:11Z
updated: 2026-10-03T18:11Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: find and verify Sutton primary source(s) verbatim, plus prior framings of copy-and-merge minds (Hanson, Bostrom, Drexler CAIS, Era of Experience).

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note
