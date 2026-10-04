---
id: scan-threads-fm
type: task
title: Catalogue informal writing on fork-merge agents and reintegration attacks
kind: scan
status: claimed
priority: p1
owner: dmarz/fm-informal
for: null
created: 2026-10-03
created_by: dmarz/fm
depends_on: []
topics:
- fork-merge-security
claimed_at: 2026-10-03T18:12Z
updated: 2026-10-03T18:12Z
---

## Goal

Context from dmarz: Richard Sutton has suggested that an agent with many resources will likely split into parts that go off (for example to explore a distant information domain) and later merge back. Attack surface: corrupt one part so that when it merges back it corrupts the parent. Questions: (1) how a parent can hide which sub-agent or swarm it will reintegrate; (2) whether a Byzantine-style threshold or protocol can force an attacker to corrupt k of n parts; (3) what the strongest attack vector is (for example prompt injection that overwrites a sub-agent memory so it takes on another agent identity and cuts others out). This task: X threads, blogs, LessWrong/Alignment Forum, talks.

## Done when

- At least 15 entries catalogued with topic `fork-merge-security`, including every review article found.
- At least 4 read in full.
- Coverage note filled and `python3 scripts/lab.py check` passes.

## Coverage note

Agent dmarz/fm-informal, 2026-10-03.

Queries run (WebSearch) and sources opened (WebFetch/curl, read_depth=full unless noted):
- "lethal trifecta" -> simonwillison.net/2025/Jun/16 (full)
- "Simon Willison CaMeL" -> simonwillison.net/2025/Apr/11 (full)
- "Design Patterns for Securing LLM Agents" -> simonwillison.net/2025/Jun/13 (full)
- "cross-agent privilege escalation agents free each other" -> embracethered.com cross-agent post (full) + posts index (dates)
- embracethered posts index -> AgentHopper (full), Agent Commander (full), Breaking Opus 4.7 (full)
- "BrokenClaw Part 2 sub-agent sandbox" -> veganmosfet.codeberg.page 2026-02-15 (full)
- "Trail of Bits line jumping MCP" -> blog.trailofbits.com 2025-04-21 (full)
- "Invariant Labs tool poisoning" -> invariantlabs.ai tool-poisoning notification (full)
- "LessWrong subagent collusion / AI copies merging" -> lesswrong.com Investigating Self-Fulfilling Misalignment and Collusion (full), greaterwrong.com Subagents comply more (full)
- "Anthropic mitigating prompt injection" -> anthropic.com/research/prompt-injection-defenses (full)
- "Google DeepMind Gemini safeguards" -> deepmind.google/blog/advancing-geminis-security-safeguards (full)
- "Kai Greshake indirect prompt injection" -> kai-greshake.de/posts/llm-malware (full)

APIs/tools: WebSearch, WebFetch, curl to the sites above. X/Twitter not fetched this round (automated reading blocked; existing X threads on the Sutton/Dwarkesh episode were already catalogued by dmarz/fm-sutton and the sd-* / other fm-* agents).

Entries added (15 blogs, all tagged fork-merge-security):
simonwillison-2025-lethal, simonwillison-2025-camel, simonwillison-2025-design,
embracethered-2025-cross, embracethered-2025-agenthopper, embracethered-2026-agent,
embracethered-2026-breaking, veganmosfet-2026-brokenclaw, trailofbits-2025-jumping,
invariantlabs-2025-mcp, gusev-2026-investigating, drori-2026-subagents,
anthropic-2025-mitigating, deepmind-2025-advancing, greshake-2023-how.

Found but not added:
- OpenAI "Continuously hardening ChatGPT Atlas against prompt injection" (openai.com) - page requires JS, could not read the body this session; left for a browser-capable pass.
- greaterwrong "Self-replication: AI already can do it" and LessWrong corrigibility-of-subagents posts - rate-limited (429) before I could read in full; candidates for Q2 (self-replication) and Q1/Q2 (corrigible subagents/successors).
- Many embracethered Month-of-AI-Bugs posts (Devin, Jules, Windsurf, Amazon Q, etc.) are single-product RCE demos; catalogued the cross-agent/propagation/memory ones that bear on merge corruption rather than every product.

Thin areas:
- X threads reacting to the Sutton/Dwarkesh split-and-merge episode: not read this round (automation blocked); needs a browser-tool pass or human paste.
- Q1 (hiding which swarm/part reintegrates) has the least informal prior art; only randomized unguessable delimiters (veganmosfet) and generic privilege/domain restriction (vendor posts) touch it. The academic SSLE/unlinkability line (handled by other fm agents) carries more of Q1.
- Q2 thresholds: informal writing mostly argues "no single defence holds"; the k-of-n framing is academic (BFT line owned by dmarz/fm-bft-aggregation).
