---
id: survey-active-matter
type: task
title: 'Survey: active matter physics'
kind: survey
status: open
priority: p1
owner: null
created: '2026-10-03'
created_by: dmarz/setup
depends_on:
- scan-papers-active-matter
topics:
- active-matter
---

## Goal

Write surveys/active-matter.md and get it through the prior-art gate. Extend the library as you go; the scan is a starting point, not the boundary. When `python3 scripts/lab.py gate active-matter` is clean, set status: complete and open a review task for another researcher.

## Done when

- The survey passes the gate and is marked complete.
- A review task `review-active-matter` is open with `for:` set to a researcher other than the owner.
