---
id: scan-papers-sd-bots
type: task
title: 'Catalogue the papers: social bots, LLM-powered botnets and coordinated inauthentic behaviour detection'
kind: scan
status: done
priority: p0
owner: dmarz/sd-bots
for: null
created: '2026-10-03'
created_by: dmarz/sd
depends_on: []
topics:
- swarm-detection
claimed_at: 2026-10-03T18:21Z
updated: 2026-10-03T19:40Z
outputs:
- library (added_by: dmarz/sd-bots)
- lab/researchers/dmarz/log/2026-10-03-sd-bots.md
---

## Goal

Context from dmarz: find all papers and results on detecting AI agent swarms in the wild: many LLM or autonomous agents (possibly coordinated, possibly Sybils of one operator) acting on social platforms, the web, markets, chains or other agents. One idea of many is honeypots that attract and identify swarms; treat it as one branch, not the frame. Look for detection methods, measured base rates of agent activity in the wild, evasion results, and negative results that show detection fails. This task: Botometer-era bot detection, LLM-driven botnets observed in the wild, coordinated inauthentic behaviour and influence-operation detection, and how well classic detectors hold up against LLM agents.

## Done when

- At least 15 entries catalogued with topic `swarm-detection`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Run as an isolated lane on branch lane/sd-bots, merged to main via lane/sd-merge on 2026-10-03. 47 new entries after dedup. Search was rate-limited (OpenAlex, arXiv export, Semantic Scholar 429s) and did not reach saturation; see the lane log for what was not reached.
