---
id: synthesis-fork-merge-questions
type: task
title: 'Synthesis: the three fork-merge questions against prior art'
kind: synthesis
status: open
priority: p1
owner: null
for: null  # set to a researcher name to direct the task at them
created: 2026-10-03
created_by: dmarz/fm
depends_on: [scan-papers-fm-merge-poisoning, scan-papers-fm-bft-aggregation, scan-papers-fm-unlinkability, scan-papers-fm-identity-hijack]
topics: [fork-merge-security]
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). Write synthesis/fork-merge-questions.md answering each question with what prior art already establishes.

## Done when

- synthesis/fork-merge-questions.md exists, cites library entries as [[id]], and passes check.

## Coverage note

