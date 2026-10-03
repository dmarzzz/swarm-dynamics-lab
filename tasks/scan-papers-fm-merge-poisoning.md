---
id: scan-papers-fm-merge-poisoning
type: task
title: 'Catalogue the papers: poisoning through model merging, federated aggregation and distillation'
kind: scan
status: claimed
priority: p0
owner: dmarz/fm-merge-poisoning
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- marl-emergence
claimed_at: 2026-10-03T18:11Z
updated: 2026-10-03T18:11Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: model-merging backdoors, federated learning poisoning, distillation and subliminal transfer as the ML analogue of a corrupted part merging back.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note
