---
id: scan-threads-x-crawl
type: task
title: Crawl X for author threads on every library arXiv paper, plus the agent-discourse trend chart
kind: scan
status: claimed
priority: p1
owner: dmarz/x-threads
for: null
created: 2026-10-03
created_by: dmarz/x-threads
depends_on:
- scan-threads-x-security
topics:
- sybil-resistance
- fork-merge-security
- swarm-detection
- llm-agent-swarms
claimed_at: 2026-10-03T19:31Z
updated: 2026-10-03T19:31Z
---

## Goal

Scale [[scan-threads-x-security]] from 211 security papers to every library paper with an arXiv id. Catalogue the authors' own threads and high-engagement expert commentary. Separately, chart how X attention to Sybil topics and multi-agent projects moved month by month from 2023 to 2026.

## Done when

- Every library arXiv paper has been searched on X, and author threads are catalogued with archived text.
- A trend figure is filed through `fd add`.
- `python3 scripts/lab.py check` passes.

## Coverage note

Agent dmarz/x-threads, 2026-10-03. Total Apify spend for the day is under $25 (apidojo/tweet-scraper); scripts are in `src/x-trend/`.

Thread crawl:
- 956 library papers have arXiv ids (main checkout plus the sd lanes). Each was searched as `url:<id> -filter:retweets min_faves:2`, giving 1,914 tweets; 422 papers (44%) have X discussion.
- The poster was matched against the paper's author list (`classify.py`). 264 tweets came from 167 papers' own authors; 186 were from arXiv feed bots and were dropped.
- Picks: 190 author threads and 146 commentary posts with 60+ likes, deduplicated against the existing library; 333 bundles fetched (fxtwitter root plus Apify conversation search).
- 8 parallel writers produced 322 entries and skipped 11 where the paper appeared only incidentally (reading lists, a link in passing). Writers re-checked every author match by hand: about 15 were name collisions and were rewritten as commentary.

Warnings: about 140 `[[paper]]` links point at papers that exist only in the unmerged sd lanes (sd-merge). They resolve when those lanes merge.

Trend chart, filed as artifacts `agent-discourse-x` (figure) and `agent-discourse-x-page` (interactive):
- 22 terms × 45 months (2023-01 to 2026-09), one `since/until min_faves:50` Top search per term per month, about 50,000 tweets in total.
- Most terms hit the 3,000-post run cap, so the counts are lower bounds. The chart therefore plots summed likes on each month's top posts, which the biggest posts dominate.

Findings (from the measured series; interpretation flagged):
- Sybil talk on X is dominated by crypto airdrop anti-farming. "sybil x AI agents" peaks 2024-09 on airdrop posts by AI-branded tokens, not on agent-collective security. Proof-of-personhood peaks 2024-12 on a points-farming season announcement. Agent identity (ERC-8004, KYA) appears only from late 2025 and peaks 2026-01 with ERC-8004 mainnet.
- Multi-agent projects come in sharp single-month spikes: AutoGPT 2023-04, ElizaOS 2025-01, OpenAI Agents SDK 2025-03, Moltbook 2026-01 (the largest of any term, about 746k likes on top posts), OpenClaw 2026-02, Hermes Agent 2026-04. Frameworks (LangGraph, AutoGen, CrewAI) instead grow slowly to a 2026 plateau.
- "agent swarm" reaches its maximum in 2026-09, the month of the rogue-OpenAI-swarm reporting. "subagents" peaks 2026-01. Inferred: the vocabulary moved from "multi-agent framework" to "subagents" and "swarm" in 2026.
