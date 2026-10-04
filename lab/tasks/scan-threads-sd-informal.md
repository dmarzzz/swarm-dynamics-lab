---
id: scan-threads-sd-informal
type: task
title: 'Catalogue the threads: threat-intel reports, blogs, threads and talks on agent swarms in the wild'
kind: scan
status: done
priority: p1
owner: dmarz/sd-informal
for: null
created: '2026-10-03'
created_by: dmarz/sd
depends_on: []
topics:
- swarm-detection
claimed_at: 2026-10-03T18:20Z
updated: 2026-10-03T19:40Z
outputs:
- library (added_by: dmarz/sd-informal)
- researchers/dmarz/log/2026-10-03-sd-informal.md
---

## Goal

Context from dmarz: find all papers and results on detecting AI agent swarms in the wild: many LLM or autonomous agents (possibly coordinated, possibly Sybils of one operator) acting on social platforms, the web, markets, chains or other agents. One idea of many is honeypots that attract and identify swarms; treat it as one branch, not the frame. Look for detection methods, measured base rates of agent activity in the wild, evasion results, and negative results that show detection fails. This task: Platform and lab threat-intelligence reports on AI-driven influence operations and agent abuse, security-vendor blogs on AI crawler and agent traffic, researcher threads and talks, and incident write-ups of agent swarms caught in the wild. Label vendor and opinion pieces as such.

## Done when

- At least 12 entries catalogued with topic `swarm-detection`, including every review article found.
- At least 3 read in full or run.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Run as an isolated lane on branch lane/sd-informal, merged to main via lane/sd-merge on 2026-10-03. 27 new entries after dedup. Search was rate-limited (OpenAlex, arXiv export, Semantic Scholar 429s) and did not reach saturation; see the lane log for what was not reached.
