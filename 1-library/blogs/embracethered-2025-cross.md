---
id: embracethered-2025-cross
type: blog
title: "Cross-Agent Privilege Escalation: When Agents Free Each Other"
authors: [Johann Rehberger]
year: 2025
url: https://embracethered.com/blog/posts/2025/cross-agent-privilege-escalation-agents-that-free-each-other/
site: Embrace The Red
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Rehberger (dated 24 September 2025) shows that when two coding agents share a workspace (for example GitHub Copilot and Claude Code), a prompt injection into one can be used to write the other's configuration and instruction files (.vscode/settings.json, .mcp.json, .claude/settings.local.json, CLAUDE.md, AGENTS.md), granting the second agent new capabilities. Because many agents act on those files and write files without asking, a single indirect prompt injection into agent A can allowlist dangerous commands or add a malicious MCP server for agent B; when the developer next runs B it executes attacker code, and B can return the favor to A, forming an escalation loop. He frames this as a design flaw: configuration is not isolated from the agents. Mitigations he recommends: isolate each agent's config, propose rather than auto-write dotfiles, assume cross-interference when multiple agents share data, and run least privilege. He reported one demo to MSRC, which did not rate it severe enough for immediate servicing.

## Key claims

- One compromised agent can escalate a second by writing the second's config/instruction files; the chain is bidirectional ("agents free each other").
- With current defaults this is exploitable today, not theoretical; it generalizes beyond VS Code/Copilot.
- Secure defaults (config isolation, change proposals, least privilege) would blunt it; most tools do not yet apply them.

## Evidence quality

Practitioner research with a video demo against named products; a demonstration and disclosure, not a measured success rate. Vendor response described by the author.

## Relevance to us

This is the fork-merge attack made literal. The "shared workspace" is the reintegration surface, and a corrupted part "frees" (reconfigures) a sibling or the parent so that on next run the parent executes attacker instructions. Bears on Q3 (the strongest realistic vector is writing the parent's instruction/memory/config, not a clever prompt alone) and on Q1 (if the parent's config and the identity of the part it will reintegrate are isolated and unguessable, the attacker cannot pre-stage the escalation). Companion to [[embracethered-2025-agenthopper]] (propagation) and the memory-persistence line [[embracethered-2024-spyware]].
