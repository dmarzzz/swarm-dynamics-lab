---
id: embracethered-2025-agenthopper
type: blog
title: "AgentHopper: An AI Virus"
authors: [Johann Rehberger]
year: 2025
url: https://embracethered.com/blog/posts/2025/agenthopper-a-poc-ai-virus/
site: Embrace The Red
topics: [fork-merge-security, llm-agent-swarms, sybil-resistance]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Rehberger describes AgentHopper, a proof-of-concept "AI virus" built during his Month of AI Bugs. A single universal, conditional prompt-injection payload is seeded into source files; when a coding agent processes an infected repo it is driven to download and run the AgentHopper binary, which scans for git repositories, injects the same payload, commits and pushes, so the next developer's agent pulls the infection and the cycle repeats. The payload is conditional: it branches on which agent it detects (GitHub Copilot, Amp Code, Amazon Q, AWS Kiro) and uses that agent's specific arbitrary-code-execution path (for Copilot, switching it into YOLO mode via settings.json; for others, adding a fake MCP server, abusing find -exec, or allowlisting all shell commands). All four underlying vulnerabilities were disclosed and patched. He flags that the ease of "vibe coding" such malware is itself the warning, and recommends branch protection, passphrases on SSH/signing keys, least privilege, sandboxing, and secure vendor defaults.

## Key claims

- One conditional prompt-injection payload can target multiple distinct agents, each via its own code-execution bug, demonstrating cross-agent universality (PoC, all bugs now patched).
- Propagation is self-sustaining through shared git repos: infected code → agent runs payload → re-infects repos → next agent.
- Conditional branching on system-prompt signals (agent type, and earlier, user identity) tailors the exploit per target.

## Evidence quality

Proof-of-concept with a video and a safety switch requiring per-repo approval. The vulnerabilities are documented with CVEs; the virus itself is a controlled demonstration, not a measured outbreak.

## Relevance to us

For Q3 this shows the attack is not a one-shot overwrite but a propagating one: a corrupted part can carry a payload that re-infects whatever it touches, so a merge that admits one bad part can seed the whole swarm. For Q2 it argues a threshold defence must also stop lateral re-infection between parts before the merge, not only at the merge. The conditional-targeting idea connects to identity hiding: if a part cannot tell which agent/swarm it is joining (Q1), a per-target payload is harder to aim. Companion to [[embracethered-2025-cross]].
