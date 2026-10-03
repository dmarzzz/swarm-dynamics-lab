---
id: scan-threads-agents
type: task
title: Catalogue X threads on agent swarms and multi-agent AI
kind: scan
status: claimed
priority: p0
owner: shadow/sol-1
created: '2026-10-03'
created_by: dmarz/setup
depends_on: []
topics:
- llm-agent-swarms
- marl-emergence
claimed_at: 2026-10-03T17:54Z
updated: 2026-10-03T17:54Z
---

## Goal

Find the threads where builders and researchers report what actually happens when many AI agents coordinate: results, failures, cost numbers, orchestration patterns, and demos. X blocks most automated reading. In order: use a browser tool if you have one; try search engines with `site:x.com <terms>`; try thread unrollers; otherwise write the thread URLs and search terms into your researcher's inbox.md under New and ask them to paste the text. Always paste the thread text into the entry, since threads get deleted. Never guess a handle; copy it from the page.

## Search plan

- Search terms: 'multi-agent', 'agent swarm', 'subagents', 'orchestrator', 'agents coordinating', 'emergent behavior agents', 'agent society'.
- Threads by the authors of the LLM agent papers and the maintainers of the orchestration frameworks in library/code/.

## Done when

- At least 25 thread entries with archived text, weighted toward first-hand results over opinion.
- Every paper or repo a thread links is catalogued too.
- Coverage note filled.

## Coverage note

51 thread entries, all under library/threads/, each with the author's verbatim text archived in the entry (replies by others excluded), handle copied from the X API user object, metrics recorded at access time. Source: X v2 API read-only bearer (search recent + full archive + conversation fetch), 52 queries, about 805 unique tweets, 50 author-threads pulled in full. Browser and unrollers not needed.

Counts by cluster: AI Village / swarmcha.se incident reporting (rogesterone series, swarmtraces summaries, dsewiki explainers, urlquery, jfrog gemstuffer) about 26; OpenAI statements, Transluce, flag game, Delvetown, misalignment reports about 15; builder first-hand results and orchestration patterns (subagents, orchestrators, cost numbers) about 10. Weighted toward first-hand results: the incident clusters are primary reporting with counts and dates.

Still missing: (1) linked sources not catalogued because the X API returned only images or unexpanded t.co links: JFrog GemStuffer write-up (from x-jfrogsecurity-2099918092604191103), Every 'vibe check' piece (x-every-2106112188184494268), ORBIT arXiv id + repo (x-gastronomy-2104768000616185980); listed in researchers/shadow/inbox.md. (2) The primary blog write-ups the threads point at (swarmcha.se, swarmtraces.org, transluce.org/agent-activity, collusion.wiki, physicsintelligence flag-game page, Cosmos village post, OpenAI misalignment report) belong to scan-blogs, not done here. (3) Threads by the orchestration-framework maintainers themselves are thin (2 to 3 entries); builder cost-number threads are the weakest cluster. Follow-up: scan-blogs and scan-datasets tasks already exist and cover the gaps; no new task opened.
