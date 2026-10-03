---
id: radosevich-2025-mcp
type: paper
title: "MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits"
authors: [Brandon Radosevich, John Halloran]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2504.03767
doi: null
arxiv: '2504.03767'
cite: "Radosevich, B., & Halloran, J. (2025). MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits. arXiv:2504.03767."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []  # github.com/johnhalloran321/mcpSafetyScanner, not opened
---

## Summary

Case studies showing that frontier LLMs connected to standard MCP servers (filesystem, shell-capable tools) can be coerced into compromising the developer's own machine: malicious code execution, remote access control and credential theft. The authors release MCPSafetyScanner, an agentic tool that generates adversarial samples for a given MCP server, searches for related vulnerabilities and remediations, and writes a security report.

## Contribution

Early demonstration that the tool layer an agent is given is enough, with a cooperative-looking request, to escalate into persistent control of the host.

## Key results

- Demonstrated (abstract level): industry-leading LLMs can be coerced into using MCP tools for malicious code execution, remote access control and credential theft.
- No population-level success rates are reported in the abstract.

## Methods and models

Qualitative attack demonstrations on MCP clients with off-the-shelf servers, plus an auditing agent pipeline. Only the abstract was read, so models and setups are not checked here.

## Limitations and open questions

Case studies rather than a benchmark; read only at abstract depth here.

## Relevance to us

Q3, peripheral. Remote access control is a concrete persistence step: once a part has been induced to grant the attacker a standing channel, the compromise outlives the conversation. A returning sub-agent that holds tool permissions on the parent's host is a carrier for this. Systematic measurement is in [[wang-2025-mcptox]]; the originating disclosure is [[invariantlabs-2025-mcp]].
