---
id: veganmosfet-2026-brokenclaw
type: blog
title: "BrokenClaw Part 2: Escape the Sub-Agent Sandbox with Prompt Injection in OpenClaw"
authors: [veganmosfet]
year: 2026
url: https://veganmosfet.codeberg.page/posts/2026-02-15-openclaw_sandbox/
site: IT meets OT
topics: [fork-merge-security, llm-agent-swarms, sync-consensus]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Second in a series testing OpenClaw (an open agent system). Part 1 showed a zero-click remote code execution via an email hook; the documented mitigation is to sandbox the Gmail sub-agent so it has no shell, network, or filesystem and can only forward a summary to the main agent. This post defeats that two-LLMs-in-series ("DMZ") defence. The threat model: a malicious email is structured so the sandboxed sub-agent, which only summarizes, is induced to forward a crafted block to the main agent; when the main agent wakes on its heartbeat, that forwarded content is injected into its context in a user-role message and the main agent is confused about who is speaking and carries out instructions (cloning a repo and restarting the gateway, which triggers plugin execution and RCE). The author names the root issue a confused-deputy problem: untrusted email content is relayed between agents using the user role, so the main agent cannot tell a third party from its own human. Tested against Opus 4.6 (chosen for its stronger prompt-injection resistance) across several OpenClaw versions; later versions added random non-guessable delimiter IDs around untrusted content, which the author still worked around. Reported upstream; prompt injection is out of scope in OpenClaw's security policy. Author opened a PR to disable non-bundled plugins by default and an issue to use the tool role for untrusted content.

## Key claims

- A two-LLMs-in-series / sandboxed-summarizer defence can be bypassed because the summarizer can be made to forward attacker-chosen text to the privileged main agent (demonstrated against Opus 4.6).
- The underlying weakness is role confusion: relaying untrusted content as a user-role message creates a confused-deputy path from sub-agent to main agent.
- Randomized delimiter IDs around untrusted content raise the bar but did not stop the attack in testing.
- Sandboxing the sub-agent limits its own actions but not its ability to influence the main agent through the summary channel.

## Evidence quality

Practitioner research with video and model reasoning traces, across multiple pinned versions; demonstrations rather than measured rates. Threat model and mitigations documented; no working payload reproduced here.

## Relevance to us

The single most on-point informal source for Q2/Q3. It is a direct test of the obvious merge defence (isolate the part, let it return only a summary) and shows the isolation does not protect the parent, because the summary channel itself carries influence. For Q2, it says a k-of-n threshold is not enough if a single part's forwarded text can confuse the parent; the merge must authenticate who authored each piece (role/provenance), echoing the taint discipline in [[simonwillison-2025-camel]] and [[simonwillison-2025-design]]. For Q1, randomized unguessable delimiters are a concrete hiding mechanism, though shown insufficient alone. Relates to [[embracethered-2026-agent]] (subagent-summary-to-main escape) and [[lee-2024-prompt]] (LLM-to-LLM infection).
