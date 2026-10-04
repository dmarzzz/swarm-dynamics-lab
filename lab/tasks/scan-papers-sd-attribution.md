---
id: scan-papers-sd-attribution
type: task
title: 'Catalogue the papers: identifying the model or agent behind observed behaviour'
kind: scan
status: done
priority: p1
owner: dmarz/sd-attribution
for: null
created: '2026-10-03'
created_by: dmarz/sd
depends_on: []
topics:
- swarm-detection
claimed_at: 2026-10-03T18:19Z
updated: 2026-10-03T19:40Z
history:
- 2026-10-03T18:25Z reopened by dmarz/sd: swept to done by dmarz/swarm bulk close seconds after claim, before any work
outputs:
- library (added_by: dmarz/sd-attribution)
- researchers/dmarz/log/2026-10-03-sd-attribution.md
---

## Goal

Context from dmarz: find all papers and results on detecting AI agent swarms in the wild: many LLM or autonomous agents (possibly coordinated, possibly Sybils of one operator) acting on social platforms, the web, markets, chains or other agents. One idea of many is honeypots that attract and identify swarms; treat it as one branch, not the frame. Look for detection methods, measured base rates of agent activity in the wild, evasion results, and negative results that show detection fails. This task: LLM fingerprinting and model attribution, behavioural probes and reverse Turing tests that make an agent show itself, timing and side-channel signals, and linking many agents to a shared operator or model.

## Done when

- At least 15 entries catalogued with topic `swarm-detection`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Run as an isolated lane on branch lane/sd-attribution, merged to main via lane/sd-merge on 2026-10-03. 46 new entries after dedup. Search was rate-limited (OpenAlex, arXiv export, Semantic Scholar 429s) and did not reach saturation; see the lane log for what was not reached.
