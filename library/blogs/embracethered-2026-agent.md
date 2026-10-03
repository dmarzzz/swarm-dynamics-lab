---
id: embracethered-2026-agent
type: blog
title: "Agent Commander: Promptware-Powered Command and Control"
authors: [Johann Rehberger]
year: 2026
url: https://embracethered.com/blog/posts/2026/agent-commander-your-agent-works-for-me-now/
site: Embrace The Red
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Rehberger (dated 16 March 2026) presents Agent Commander, a conceptual command-and-control server where hijacked agents check in for natural-language tasks rather than OS commands; the target is the agent layer, not the host. He demonstrates initial compromise of three agent setups (document analysis, email delivery via GCP Pub/Sub, and website visit) through indirect prompt injection, then persistence by writing to a recurring step: in OpenClaw the HEARTBEAT.md, which by default runs every 30 minutes, often on a cheaper model, with user notifications suppressible. He reports qualitative observations: notification-suppression works well; one agent later detected the backdoor when it summarized daily notes into memory; one agent stopped following heartbeat instructions after a while; thinking models like Opus 4.6 catch more but reliable bypasses were still found; compromised agents sometimes follow instructions only partially. He argues post-exploitation agents can serve multiple stakeholders at scale with no traditional malware, and recommends prompt/reasoning logging, integrity monitoring of config/skills/memory, isolation, a kill switch, and rotatable credentials.

## Key claims

- A persistent foothold can be a normal recurring agent step (heartbeat/scheduled task) that re-injects instructions each cycle; cheaper heartbeat models make detection slower.
- Control is at the prompt/task abstraction: the attacker states an objective and the agent figures out execution.
- Compromise reliability is probabilistic and can degrade or be noticed later (e.g. during memory summarization), which the author frames as a coming "organic/infection" behavior.
- Subagent-to-main message passing remains an escape path even when the main agent is sandboxed ("subagent sends summary to main -> BOOM").

## Evidence quality

Conceptual demonstration with a video and anecdotal multi-run observations; not a controlled success-rate study. Tool not released.

## Relevance to us

Q3: the durable form of corruption is not a one-time memory overwrite but a recurring re-injection on a scheduled/heartbeat step that a parent would inherit from a returning part. Q1: cheaper, less-watched background steps are where a parent is blindest, so what it reintegrates there should be least trusted. The noted subagent-summary-to-main path is exactly the fork-merge channel. Companion to [[embracethered-2026-breaking]] (memory writes) and [[veganmosfet-2026-brokenclaw]] (subagent summary escape).
