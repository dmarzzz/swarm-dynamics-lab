---
id: survey-fork-merge-security
type: task
title: 'Survey: corruption on reintegration in fork-and-merge agents'
kind: survey
status: done
priority: p1
owner: shadow/sol-fm
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on:
- scan-papers-fm-merge-poisoning
- scan-papers-fm-bft-aggregation
- scan-papers-fm-unlinkability
- scan-papers-fm-identity-hijack
topics:
- fork-merge-security
claimed_at: 2026-10-04T14:21Z
updated: 2026-10-04T14:34Z
outputs:
- surveys/fork-merge-security.md
- library/papers/xie-2020-dba.md
- library/papers/lyu-2023-poisoning.md
- library/papers/zhai-2024-secret.md
- tasks/review-fork-merge-security.md
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). Prior-art survey across the fm scan tasks, organised by the three questions.

## Done when

- `python3 scripts/lab.py gate fork-merge-security` reports nothing missing.
- Review task opened for another researcher.

## Coverage note


Filled by dmarz/fm, 2026-10-03. The survey is `surveys/fork-merge-security.md`, status in-progress. It runs no new searches. It is assembled from the 480 library entries tagged fork-merge-security and from the lane reports, and it cites 280 distinct entries.

Queries and APIs: none new. The frontmatter search log has 95 rounds, built only from the coverage notes of scan-papers-fm-sutton, -merge-poisoning, -memory-injection, -bft-aggregation, -unlinkability, -biology (1 round), -mobile-agents, -ai-control, -identity-hijack, scan-code-fm and researchers/dmarz/notes/fm-gap-1..3.md. Rounds without both a result count and a new count were left out: all of scan-threads-fm, biology rounds 1 to 3, the empty fm-contagion note, and gap-3 round 0 (local lab.py find). Crossref, Europe PMC, OpenCitations and direct fetches are logged as `web`, since the allowed list has no slot for them.

`lab.py gate fork-merge-security` result: every floor passes except saturation. The last two rounds are gap-3 r11 (2/10) and r12 (1/9). They exceed 15% because the gap fills ran last and were still finding new items. Lane-level saturation holds for the merge-attack core, SSLE and anonymity vocabulary, Byzantine aggregation and the Sutton lane. It does not hold for mobile agents (that lane says so itself) or for agent-specific Q1 vocabulary.

Found but not added (from the lanes): DBA distributed backdoor (OpenReview blocked), secret committee election (2024), Roth 2002 on attacks against mobile-agent protocols, Westhoff 1999 on route protection, Holmstrom 1982, Parfit on fusion, the Subliminal-is-a-LoRA-artifact replication (2606.00831), X threads on the Sutton interview.

Thin: no source measures an end-to-end fork, corrupt and merge of one LLM agent; no k-of-n sweep where the corrupted forks share one adversarial input; no hidden-returner protocol for agents; and no breakdown point is defined for text or memory merges.
