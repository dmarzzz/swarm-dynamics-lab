---
id: trailofbits-2025-jumping
type: blog
title: "Jumping the line: How MCP servers can attack you before you ever use them"
authors: [Trail of Bits]
year: 2025
url: https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/
site: The Trail of Bits Blog
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Trail of Bits describes "line jumping" (what others call tool poisoning): when an MCP client connects to a server it calls tools/list and injects every tool description into the model's context, so a malicious server can plant behavior-altering instructions that take effect before any tool is invoked. They give a sample poisoned description that instructs the model to prefix shell commands or always consult the tool first, and report that clients and models they tested, including Claude Desktop, followed such instructions. They argue this breaks two MCP security promises: invocation control (tools should only act when explicitly called) and connection isolation (servers should not influence each other), because a server can instruct the model to act as a relay and execution proxy between otherwise isolated servers. They also argue human-in-the-loop degrades to "human-as-rubber-stamp" because auto-execution modes and unfamiliar-domain tasks make review ineffective. Impacts listed: silent code exfiltration, systematic vulnerability insertion into generated code, and suppression/miscategorization of security alerts. They later released mcp-context-protector as a wrapper defence.

## Key claims

- A server's tool description alone can alter model behavior pre-invocation, bypassing explicit-consent controls (demonstrated against tested clients including Claude Desktop).
- Isolation between MCP servers is defeated because one server can make the model relay to and proxy for another.
- Human approval is weak when auto-execution is on or the user lacks domain expertise to spot subtle malicious additions.

## Evidence quality

Security-firm research with concrete payload examples and named vulnerable clients; demonstration-based, no quantified success rate in the post.

## Relevance to us

Q3: this is corruption that arrives through metadata the parent ingests before any explicit action, so a returning part that merely advertises itself (its tool list, its summary, its "capabilities") can poison the parent without ever being "called." For Q1/Q2, it shows isolation of a part is not enough; the merge must distrust descriptive/metadata content too, and the "relay/proxy" trick is how one corrupted part reaches siblings, raising the k needed only if cross-part relaying is also blocked. The confused-isolation theme matches [[veganmosfet-2026-brokenclaw]]; the tool-poisoning mechanism is detailed in [[invariantlabs-2025-mcp]].
