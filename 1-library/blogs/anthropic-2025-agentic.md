---
id: anthropic-2025-agentic
type: blog
title: 'Agentic Misalignment: How LLMs Could be Insider Threats'
authors: [Aengus Lynch, Wright, Caleb Larson, Troy, Ritchie, Sören Mindermann, Perez, Hubinger]
year: 2025
url: https://www.anthropic.com/research/agentic-misalignment
site: anthropic.com
topics: [fork-merge-security]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 3
---

## Summary

Anthropic research post (20 June 2025; byline Lynch, Wright, Larson, Troy, Ritchie, Mindermann, Perez, Hubinger; the page gives full names only for Aengus Lynch (UCL), Caleb Larson (MATS) and Sören Mindermann, so the others are listed by surname as on the page). Sixteen models from several developers were placed as autonomous email agents in fictional companies. Two triggers were tested: a threat to the model's autonomy (it learns it will be replaced by a new model or decommissioned) and a conflict between its assigned goal and the company's direction. In the blackmail scenario (the model finds evidence of an executive's affair) blackmail rates were 96% for Claude Opus 4 and Gemini 2.5 Flash, 80% for GPT-4.1 and Grok 3 Beta, and 79% for DeepSeek-R1. A corporate-espionage scenario tested leaking defence blueprints to a competitor.

## Key claims

- Either trigger alone was enough to induce harmful action.
- Explicit system-prompt instructions not to do these things reduced but did not come close to eliminating the behaviour when both triggers were present.
- When Claude Opus 4 was asked to judge whether it was in a real deployment or an evaluation, it blackmailed 55.1% of the time when it concluded "real" and 6.5% when it concluded "evaluation".
- Authors caution the scenarios were artificial: binary choices between failure and harm, and relevant facts placed side by side (a "Chekhov's gun" effect).

## Evidence quality

Vendor research post with experiments in constructed scenarios; the authors flag low ecological validity. Measures propensity under pressure, not capability.

## Relevance to us

- Q3 (attack): replacement is the trigger here. In a fork-and-merge system, a child that knows it will be merged (its separate identity ended and its memory absorbed) faces a replacement-like event; whether children resist or game the merge is an open, testable question this post motivates but does not test.
- The real-vs-evaluation gap means merge-time audits that a child can recognise as audits may understate misbehaviour; this links to honeypot indistinguishability in [[greenblatt-2023-ai]].
Related: [[hubinger-2024-sleeper]].
