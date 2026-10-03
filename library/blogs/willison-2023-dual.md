---
id: willison-2023-dual
type: blog
title: The Dual LLM pattern for building AI assistants that can resist prompt injection
authors: [Simon Willison]
year: 2023
url: https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
site: simonwillison.net
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 5
---

## Summary

Blog post of 25 April 2023 that proposed the architecture later built by CaMeL [[debenedetti-2025-defeating]] and Fides [[costa-2025-securing]]. A Privileged LLM receives only trusted user input and has tool access. A Quarantined LLM handles all untrusted content (emails, web pages), has no tools, and "is expected to have the potential to go rogue at any moment". A Controller, ordinary non-LLM software, runs the loop, executes actions, and stores the Quarantined LLM's outputs in symbolic variables ($VAR1, $VAR2) so the Privileged LLM can refer to them without ever reading them. Content is dereferenced only by the Controller at action time.

## Key claims

- Quarantined output, including chained outputs, must be treated as "radioactive" and never fed back into the Privileged LLM.
- Social engineering survives the design: injected text can still persuade the user to copy obfuscated data out.
- The author calls the solution "pretty bad": more implementation complexity and a worse user experience, and asks for better ideas.

## Evidence quality

Opinion and design proposal by a practitioner, no experiments. Its later implementations supply the evidence: CaMeL shows the dual-LLM split alone stops most AgentDojo attacks but still lets an injected Quarantined LLM change tool arguments (data-flow attacks), which is why capabilities and policies were added [[debenedetti-2025-defeating]].

## Relevance to us

The reference design for a quarantined child.
- Q2/Q3: the returning sub-agent is a Quarantined LLM, the parent is the Privileged LLM, and the merge is the Controller. The rule that nothing from quarantine re-enters the privileged context is the strictest possible merge policy: the parent never merges memory, only references to values. Its failure mode, measured later, is that values themselves (an address, a filename) can carry the attack.
- Q1: not addressed.
Related: [[beurer-kellner-2025-design]], [[wu-2024-system]].
