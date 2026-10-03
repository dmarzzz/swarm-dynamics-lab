---
id: anthropic-2025-detecting
type: blog
title: "Detecting and countering malicious uses of Claude: March 2025"
authors: [Anthropic]
year: 2025
url: https://www.anthropic.com/news/detecting-and-countering-malicious-uses-of-claude-march-2025
site: Anthropic news
topics: [swarm-detection, llm-agent-swarms]
added_by: dmarz/sd-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Vendor threat report (published 23 April 2025) with four case studies of banned Claude accounts. The headline case is a financially motivated "influence-as-a-service" operation that ran over 100 social media bot accounts on X and Facebook for clients in several countries. Claude was used not only to write posts but as an orchestrator: it kept persona consistency across platforms, decided whether each bot should like, share, comment on or ignore specific posts by authentic users according to client political objectives, generated replies in the right language, and wrote and judged prompts for image generators. The network engaged with tens of thousands of authentic accounts. No content went viral; the operator favoured sustained, moderate engagement over virality. Detection used Anthropic's Clio and hierarchical summarization over conversation data plus input and output classifiers, then manual investigation and bans. Other cases: IoT camera credential scraping, recruitment fraud using Claude for "language sanitization", and a novice building malware.

## Key claims

- "Users are starting to use frontier models to semi-autonomously orchestrate complex abuse systems that involve many social media bots"; Anthropic expects this to grow as agentic systems improve.
- The operation's attribution to a state was not confirmed; narratives were "consistent with what we expect from state affiliated campaigns".
- Detection came from the provider's view of prompts, not from the platforms.

## Evidence quality

Vendor blog summarising a longer PDF report (linked from the page; the PDF was not opened this session). No account lists, no platform-side confirmation, no false-positive rates. OpenAI later linked this operator to its 2024 "A2Z" case [[openai-2025-disrupting-update]].

## Relevance to us

The clearest public case of an LLM acting as the decision layer of a bot swarm in the wild (an agent swarm in the hackathon's sense, with one model controlling 100+ personas). It suggests two detection vantage points: the model provider (prompt logs, clustering of persona-management conversations) and the platform (accounts whose engagement decisions are driven by one policy). The "moderate, non-viral" strategy also means virality-based detection would miss it. Companion cases in [[openai-2025-disrupting]] and the later autonomous cyber case [[anthropic-2025-disrupting]].
