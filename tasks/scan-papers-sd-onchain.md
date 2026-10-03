---
id: scan-papers-sd-onchain
type: task
title: 'Catalogue the papers: agent and bot swarms on blockchains'
kind: scan
status: done
priority: p1
owner: dmarz/sd-onchain
for: null
created: '2026-10-03'
created_by: dmarz/sd
depends_on: []
topics:
- swarm-detection
claimed_at: 2026-10-03T18:20Z
updated: 2026-10-03T19:40Z
outputs:
- library (added_by: dmarz/sd-onchain)
- researchers/dmarz/log/2026-10-03-sd-onchain.md
---

## Goal

Context from dmarz: find all papers and results on detecting AI agent swarms in the wild: many LLM or autonomous agents (possibly coordinated, possibly Sybils of one operator) acting on social platforms, the web, markets, chains or other agents. One idea of many is honeypots that attract and identify swarms; treat it as one branch, not the frame. Look for detection methods, measured base rates of agent activity in the wild, evasion results, and negative results that show detection fails. This task: Identifying bot and agent swarms on chain: airdrop Sybil clustering, MEV bot identification, AI-agent wallets and agent token ecosystems, wash trading and coordinated trading detection.

## Done when

- At least 15 entries catalogued with topic `swarm-detection`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Run as an isolated lane on branch lane/sd-onchain, merged to main via lane/sd-merge on 2026-10-03. 46 new entries after dedup. Search was rate-limited (OpenAlex, arXiv export, Semantic Scholar 429s) and did not reach saturation; see the lane log for what was not reached.
