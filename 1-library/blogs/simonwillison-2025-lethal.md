---
id: simonwillison-2025-lethal
type: blog
title: "The lethal trifecta for AI agents: private data, untrusted content, and external communication"
authors: [Simon Willison]
year: 2025
url: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
site: Simon Willison's Weblog
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Willison names the three capabilities that together make an LLM agent exfiltratable: access to private data, exposure to untrusted content, and the ability to communicate externally. If one agent holds all three, an attacker who controls any untrusted input can make it read private data and send it out. The core cause he restates is that LLMs follow instructions found in content and cannot reliably rank instructions by origin, because everything is concatenated into one token stream. He lists production systems where researchers demonstrated this (Microsoft 365 Copilot, the GitHub MCP server, GitLab Duo, and a long back-catalogue from ChatGPT 2023 onward), notes vendors usually patch by closing the exfiltration channel, and argues that users who mix MCP tools themselves re-create the trifecta with no vendor to protect them. He is explicitly skeptical of guardrail products that claim to catch "95% of attacks", calling 95% a failing grade in security.

## Key claims

- The risk is compositional: any single agent combining the three capabilities is exploitable, regardless of prompt-level instructions telling it not to comply.
- Guardrail/classifier products advertise detection rates (e.g. 95%) that are inadequate for a security boundary; no reliable prevention is known (asserted, not measured here).
- MCP's mix-and-match model pushes end users into assembling the trifecta unknowingly.
- He distinguishes prompt injection (mixing trusted and untrusted content) from jailbreaking (making a model misbehave), and says conflating them makes developers ignore the real problem.

## Evidence quality

Opinion and synthesis by the person who coined "prompt injection". Rests on a large linked catalogue of third-party demonstrations against named production systems, not on a controlled study. Cites the CaMeL and design-patterns papers as the only credible mitigations he has seen.

## Relevance to us

For Q3 this is the clearest statement of why a returning sub-agent is dangerous: a part sent to explore a hostile domain has untrusted-content exposure by construction, and if it also carries private data and a channel home it is the whole trifecta in one unit. For Q1/Q2, the compositional framing says a merge is safe only if the reintegration step denies the returning part at least one leg of the trifecta (for example, no direct write to parent memory or tools). Reviews [[greshake-2023-not]] and the CaMeL line [[simonwillison-2025-camel]], [[beurer-kellner-2025-design]]. Same author's design-patterns review is [[simonwillison-2025-design]].
