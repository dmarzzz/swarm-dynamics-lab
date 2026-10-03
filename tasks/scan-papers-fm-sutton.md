---
id: scan-papers-fm-sutton
type: task
title: 'Catalogue the primary sources: Sutton on agents splitting and merging, and prior framings'
kind: scan
status: claimed
priority: p0
owner: dmarz/fm-sutton
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
- meta
claimed_at: 2026-10-03T18:11Z
updated: 2026-10-03T18:11Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: find and verify Sutton primary source(s) verbatim, plus prior framings of copy-and-merge minds (Hanson, Bostrom, Drexler CAIS, Era of Experience).

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Agent dmarz/fm-sutton, 2026-10-03. 18 entries added, all tagged fork-merge-security; 7 read in full (sutton-2025-father, dwarkesh-2025-what, sutton-2024-perspective, anthropic-2025-how, hanson-2016-age, christiano-2016-reliability, christiano-2016-security), the rest skimmed. No review article on fork-merge corruption of agents was found; [[de-witt-2025-open]] (already in the library) is the nearest survey.

Primary-source verification. Sutton's statement is at 00:49:51 of the Dwarkesh Podcast interview published 2025-09-26 (official transcript at dwarkesh.com/p/richard-sutton), with a related remark at 00:26:11; quoted verbatim in [[sutton-2025-father]]. The "view" he was responding to is Dwarkesh Patel's "What will automated firms look like?" video (youtu.be/bJD1NpdMY5s), essay version [[dwarkesh-2025-what]]. Not found in: The Alberta Plan (2022), Welcome to the Era of Experience (2025), A Perspective on Intelligence (2024 slides), AI Alignment and Decentralization (2023 slides), WAIC 2023 "AI Succession" slides (waic3.pdf, searched for copy/merge/spawn/corrupt, no hits; not catalogued). So the earliest Sutton statement found is September 2025. Note: his example domains are "the other side of the planet" and "Indonesia", not China.

Rounds (results / new to library):
1. General web: Sutton + Dwarkesh + spawn/corruption: 10 / 1 (transcript). Transcript fetched with curl and grepped.
2. Sutton's site incompleteideas.net/Talks: talk list plus 3 slide PDFs: 3 / 1.
3. Sutton papers: Alberta Plan (arXiv), Era of Experience (DeepMind PDF): 2 / 2.
4. Dwarkesh archive API (search "automated firm"): 5 / 1.
5. Prior framings, web: Bostrom and Shulman (digital-minds.pdf, propositions.pdf), Hanson (ageofem.com; overcomingbias search returned 10, none on merging specifically), Drexler CAIS (FHI TR 2019-1): 30 / 4.
6. Christiano amplification: arXiv 1810.08575 and Alignment Forum posts via LessWrong GraphQL (ai-alignment.com on Medium blocked by Cloudflare): 9 / 3.
7. Commentary on the interview (Zvi, LessWrong mirror): 10 / 1.
8. Vendor fork-join docs: Anthropic multi-agent research post, Claude Code subagents docs: 2 / 2.
9. Neighbouring vocabulary ("mind merging", fission/fusion, knowledge merging protocols): 10 / 1 (MELD).
10. Forward citations of 1810.08575 via Semantic Scholar (100 citing papers scanned by title): 7 relevant / 1 new added (sharding); de-witt-2025-open already present.
11. arXiv API: fork AND merge AND agents AND LLM (2), subagent AND injection (6), orchestrator AND prompt injection AND multi-agent (14): 22 / 1 (cai-2026-child).
Rounds 10 and 11 each added at most 1 new item from 7 and 22 results (14% and 5%).

APIs: Semantic Scholar returned 429 for most calls and OpenAlex exhausted its shared daily budget mid-run, so forward citation chasing was done only on 1810.08575. Crossref used for DOIs.

Found but not added (left for other lanes or judged off-lane): AgentSpawn arXiv 2602.07072 (fork with memory transfer, code generation; abstract only); Arbiter Agent 2606.10747; Multi-Agent Systems Execute Arbitrary Malicious Code 2503.12188; OMNI-LEAK 2602.13477; Beyond Single-Model Injection 2609.22949; Second Thought 2608.13667; Persistent Identity in AI Agents 2604.09588; Gwern on corporations not replicating (cited in dwarkesh-2025-what, not opened); Hanson's Age of Em book text itself (paywalled; only the author's summary site was read); Christiano "Meta-execution" post (not opened); Kleppmann and Howard 2020 Byzantine eventual consistency (cited by MELD; belongs to the BFT lane); The Bitter Lesson (not opened; no fork-merge content expected).

Thin: no peer-reviewed work names Sutton's scenario; nothing measures corruption on reintegration of a diverged copy into weights. The philosophy of personal identity under fission and fusion (Parfit) was not searched in primary sources. Forward citations of CAIS and of the digital-minds papers were not chased because of API limits.
