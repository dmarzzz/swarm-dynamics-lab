---
id: survey-llm-agent-swarms
type: task
title: 'Survey: llm agent swarms'
kind: survey
status: done
priority: p1
owner: shadow/sol-1
created: '2026-10-03'
created_by: dmarz/setup
depends_on:
- scan-papers-llm-agent-swarms
topics:
- llm-agent-swarms
claimed_at: 2026-10-03T17:57Z
updated: 2026-10-03T18:16Z
outputs:
- 2-surveys/llm-agent-swarms.md
---

## Goal

Write surveys/llm-agent-swarms.md and get it through the prior-art gate. Extend the library as you go; the scan is a starting point, not the boundary. When `python3 scripts/lab.py gate llm-agent-swarms` is clean, set status: complete and open a review task for another researcher.

## Done when

- The survey passes the gate and is marked complete.
- A review task `review-llm-agent-swarms` is open with `for:` set to a researcher other than the owner.
