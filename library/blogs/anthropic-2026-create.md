---
id: anthropic-2026-create
type: blog
title: Create custom subagents (Claude Code documentation)
authors: [Anthropic]
year: 2026
url: https://code.claude.com/docs/en/sub-agents
site: Claude Code docs (code.claude.com), page as served on 2026-10-03 (markdown at https://code.claude.com/docs/en/sub-agents.md); undated living document
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-sutton
accessed: 2026-10-03
read_depth: skim
relevance: 4
---

## Summary

Vendor documentation for the fork-join primitives in Claude Code, read in the sections on context, tools, memory, output scanning, nesting and forks. A subagent "runs in its own context window with a custom system prompt, specific tool access, and independent permissions" and "returns only the summary". Subagents may nest "up to three layers below the main conversation". A "fork" is a subagent "that inherits the entire conversation so far instead of starting fresh", which the page says "drops the input isolation that subagents otherwise provide"; "only its final result comes back", and "A fork can't spawn further forks". Optional `isolation: worktree` gives a subagent an isolated git checkout. A `memory` field gives a subagent "a persistent directory that survives across conversations", whose `MEMORY.md` (first 200 lines or 25KB) is loaded into the subagent's system prompt at start. The "Subagent output scanning" section (v2.1.210 or later) is a merge-time control: the harness "scans each subagent's final report before Claude reads it" because a subagent "may have read files, web pages, or command output you never reviewed, and text from those sources can carry instructions aimed at the main conversation". The scan escapes text imitating harness tags or `Human:`/`Assistant:` turns and prepends a marker line when it matches instruction-shaped patterns, but "doesn't judge whether content is malicious"; the returned report also arrives under a header stating that instructions inside it "carry no authority" from the user.

## Key claims

- Subagents isolate context and tools; forks share full context but return only a result.
- Child output is treated as untrusted at the merge boundary, with pattern-based marking, not filtering.
- Downstream tool calls the report induces still pass the session's permission checks and sandbox.

## Evidence quality

Product documentation describing shipped behaviour; no measurements of how often the scan catches injected instructions or how often marked reports still steer the parent.

## Relevance to us

A deployed fork-merge system that already treats Sutton's concern ([[sutton-2025-father]]) as a security boundary, at the text level. Q3: the documented threat model is exactly the child-to-parent injection path (a child reads attacker-controlled web pages and its report carries instructions to the parent), and the page states the defence is marking plus permission checks, not detection. Persistent subagent memory creates the dmarz scenario of overwriting a sub-agent's memory: whatever a child writes into its `MEMORY.md` is injected into the system prompt of every future instance of that subagent, so a single successful injection persists across forks. Q1 and Q2: the parent merges every child's report and there is no built-in quorum; forks inheriting the full context are identical copies, which per [[bostrom-2023-propositions]] share vulnerabilities. Compare [[anthropic-2025-how]] (the research-agent architecture) and [[gh-anthropics-claude-agent-sdk-python]].
