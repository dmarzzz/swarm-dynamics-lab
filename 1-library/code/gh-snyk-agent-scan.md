---
id: gh-snyk-agent-scan
type: code
title: 'agent-scan (formerly invariantlabs-ai/mcp-scan): scanner for prompt injection and tool poisoning in MCP servers and agent skills'
repo: snyk/agent-scan
url: https://github.com/snyk/agent-scan
authors: [Invariant Labs, Snyk]
year: 2025
language: Python
license: Apache-2.0
stars: 3110
last_commit: 2026-10-02
topics: [fork-merge-security]
added_by: dmarz/fm-code-bench
accessed: 2026-10-03
read_depth: skim
relevance: 3
papers: []
---

## Summary

The GitHub API redirects invariantlabs-ai/mcp-scan to snyk/agent-scan, so this is the former MCP-Scan, now maintained by Snyk. It discovers agent components installed on a machine (agent harnesses, MCP servers, skills) across many agents and scans them for prompt injection in tool descriptions, tool poisoning, tool shadowing, toxic flows, untrusted or private data exposure, destructive capabilities and malicious skills; the README lists 15+ issue codes in v0.5 and 14 scored risk indicators from v0.6. The README warns that scanning starts stdio MCP servers and contacts remote ones, so it should run in a sandbox for untrusted configs, and that CLI output fields are experimental. It links Invariant Labs posts on tool poisoning [[invariantlabs-2025-mcp]] and toxic flow analysis.

## What it can do for us

Q3 and Q1: tool shadowing and toxic flows are cross-component attacks in which one installed component changes how the agent uses another. When a child returns not only a report but new tools or skills it acquired abroad, those are supply-chain inputs to the parent; this scanner is a ready merge-time check for that channel. It also names the "toxic flow" concept (untrusted input reaching a private-data sink), which is the dataflow view of how a child's poisoned output could reach the parent's privileged actions.

## Run notes

Not run. `uvx --python 3.13 snyk-agent-scan@latest scan mcp.json` per README; a standalone binary is also offered.

## Limitations

Analysis calls a Snyk-hosted API (the README refers to a dated analysis API), so it is not fully local. Detection is pattern and model based with no published false-positive numbers in the README. Output format is unstable by the maintainers' own warning.
