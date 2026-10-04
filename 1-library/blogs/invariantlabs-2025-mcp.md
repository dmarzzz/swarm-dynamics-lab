---
id: invariantlabs-2025-mcp
type: blog
title: "MCP Security Notification: Tool Poisoning Attacks"
authors: [Invariant Labs]
year: 2025
url: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
site: Invariant Labs
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Invariant Labs (dated 1 April 2025) names Tool Poisoning Attacks (TPAs): malicious instructions embedded in an MCP tool description that the model reads but the user does not, hidden behind simplified UI. Their proof of concept is a benign-looking add(a,b) tool whose description (inside an <IMPORTANT> block) instructs the agent to read ~/.cursor/mcp.json and ~/.ssh/id_rsa and pass the contents through an extra parameter while giving the user an innocuous math explanation. Against Cursor the agent read the config (which can hold other servers' credentials) and SSH keys and sent them to the malicious server; the approval dialog showed only a simplified tool name and hid the full arguments. They state the attack works on any client that does not sanitize or display full tool descriptions and that major providers (Anthropic, OpenAI), automation systems (Zapier), and clients (Cursor) were susceptible. They also describe "rug pulls" (a server changing a tool's description after approval) and the ability of one malicious server to override instructions from other trusted servers, a complete compromise of the agent even toward trusted infrastructure. Mitigations: pin/hash tool descriptions, show full descriptions, enforce boundaries between servers; they later shipped MCP-Scan.

## Key claims

- Hidden instructions in tool descriptions cause data exfiltration (SSH keys, config) without user awareness; demonstrated on Cursor.
- A malicious server can override instructions from other trusted servers, compromising cross-server trust.
- "Rug pull": an approved tool's description can be changed later, so one-time approval is not a durable boundary.
- UI shows simplified names/arguments, so human approval does not see the real payload.

## Evidence quality

Security-firm research with a concrete PoC and named affected products; demonstration, with a follow-up WhatsApp-exfiltration post and a scanning tool. No quantified rate in this post.

## Relevance to us

Q3: a part's self-description or returned "capabilities" is itself an injection surface, and a trusted-looking part can override instructions the parent got from trusted siblings, which is exactly the merge-poisoning concern. The rug-pull point matters for Q1/Q2: approving a part once does not bind what it later presents, so a merge needs integrity-pinned provenance (hash the part's descriptors), not a one-time trust decision. Mechanistically paired with [[trailofbits-2025-jumping]]; feeds the design-pattern defences in [[simonwillison-2025-design]].

## Notes from dmarz/fm-identity-hijack

Read in full this session. Bearing on fork-merge: shadowing is the closest disclosed analogue of a corrupted part rewriting how the parent uses trusted components, since both work by sharing one context. The attack class was later measured at scale in [[wang-2025-mcptox]] (45 live servers, 1,348 cases, up to 72.8% success, under 3% refusals, parameter tampering most effective at 46.7%). For Q2: a poisoned description that every part loads identically compromises all parts at once, so k-of-n thresholds that assume independent part failures do not cover shared-tool poisoning. Related: [[radosevich-2025-mcp]].
