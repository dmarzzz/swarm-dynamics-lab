---
id: scan-code-sd-code-data
type: task
title: 'Catalogue the code: code, datasets and benchmarks for detecting agent swarms'
kind: scan
status: done
priority: p1
owner: dmarz/sd-code-data
for: null
created: '2026-10-03'
created_by: dmarz/sd
depends_on: []
topics:
- swarm-detection
updated: 2026-10-03T19:40Z
outputs:
- library (added_by: dmarz/sd-code-data)
- researchers/dmarz/log/2026-10-03-sd-code-data.md
---

## Goal

Context from dmarz: find all papers and results on detecting AI agent swarms in the wild: many LLM or autonomous agents (possibly coordinated, possibly Sybils of one operator) acting on social platforms, the web, markets, chains or other agents. One idea of many is honeypots that attract and identify swarms; treat it as one branch, not the frame. Look for detection methods, measured base rates of agent activity in the wild, evasion results, and negative results that show detection fails. This task: Repositories, datasets and benchmarks: bot-detection datasets and tools, LLM-agent honeypot frameworks, coordination-detection libraries, AI-text detectors and agent-traffic datasets. Record stars, licence and last commit; run what is cheap to run.

## Done when

- At least 12 entries catalogued with topic `swarm-detection`, including every review article found.
- At least 3 read in full or run.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Run as an isolated lane on branch lane/sd-code-data, merged to main via lane/sd-merge on 2026-10-03. 35 new entries after dedup. Search was rate-limited (OpenAlex, arXiv export, Semantic Scholar 429s) and did not reach saturation; see the lane log for what was not reached.
