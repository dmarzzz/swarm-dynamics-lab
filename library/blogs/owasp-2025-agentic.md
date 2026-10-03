---
id: owasp-2025-agentic
type: blog
title: 'OWASP Top 10 for Agentic Applications for 2026'
authors: [OWASP Gen AI Security Project]
year: 2025
url: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
site: OWASP Gen AI Security Project
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-memory-injection
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

An industry consensus risk list for agentic AI systems, released by the OWASP Gen AI Security Project on 9 December 2025 and described as globally peer-reviewed. The landing page links to a PDF. The item list was read from a third-party practitioner summary (promptfoo documentation, https://www.promptfoo.dev/docs/red-team/owasp-agentic-ai/) because the landing page does not reproduce it. ASI01 Agent Goal Hijack. ASI02 Tool Misuse and Exploitation. ASI03 Identity and Privilege Abuse. ASI04 Agentic Supply Chain Vulnerabilities. ASI05 Unexpected Code Execution. ASI06 Memory and Context Poisoning. ASI07 Insecure Inter-Agent Communication. ASI08 Cascading Failures. ASI09 Human Agent Trust Exploitation. ASI10 Rogue Agents.

## Key claims

- ASI06: attackers poison agent memory, embeddings and RAG stores to corrupt stored information and manipulate decisions across sessions.
- ASI07: multi-agent systems face spoofed identities, replayed messages and tampering on inter-agent channels.
- ASI08: small errors in one agent propagate across planning, execution and memory and are amplified through connected systems.
- ASI10: compromised or misaligned agents act harmfully while appearing legitimate, exploiting trust in multi-agent workflows.

## Evidence quality

Consensus risk taxonomy, with no measurements. The item wording above is from a secondary summary, not the PDF itself. Several 2026 papers in this lane cite ASI06 as their threat label (for example SuperLocalMemory, arXiv 2603.02240, not catalogued).

## Relevance to us

For Q3, the fork-merge attack is the composition of ASI06 (memory poisoning of the sub-agent), ASI10 (the sub-agent becomes a rogue agent that still looks legitimate) and ASI07 or ASI08 (the merge channel carries it into the parent). This gives a standard vocabulary for the threat model in a write-up. It contains nothing on Q1 or Q2. Earlier, non-agentic list: [[owasp-2025-llm]].
