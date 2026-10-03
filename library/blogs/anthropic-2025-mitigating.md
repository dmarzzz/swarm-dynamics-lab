---
id: anthropic-2025-mitigating
type: blog
title: "Mitigating the risk of prompt injections in browser use"
authors: [Anthropic]
year: 2025
url: https://www.anthropic.com/research/prompt-injection-defenses
site: Anthropic
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Vendor post (24 November 2025) announcing Claude Opus 4.5's improved robustness to prompt injection and expanding the Claude for Chrome extension from research preview to beta. The threat example is an email with hidden white-text instructions directing the agent to forward confidential emails to an external address. Anthropic reports, against an internal adaptive "Best-of-N" attacker given 100 attempts per environment, that the shipping configuration reaches about a 1% attack success rate, which they stress still represents meaningful risk and does not mean the problem is solved. Their defenses: (1) reinforcement learning during training that rewards Claude for refusing injected instructions even when they look authoritative or urgent; (2) classifiers that scan all untrusted content entering the context for hidden text, manipulated images, and deceptive UI, adjusting behavior on detection; (3) "visible thinking" so users and classifiers can inspect reasoning; (4) privilege curtailment via domain restrictions and action confirmations; and (5) scaled human red teaming plus external Arena-style challenges.

## Key claims

- Opus 4.5 reaches ~1% ASR against an internal adaptive 100-attempt attacker (vendor-measured, internal benchmark), described as improved but still risky.
- Defense-in-depth: RL hardening + input classifiers + visible thinking + privilege limits + red teaming.
- No browser agent is immune; the post explicitly declines to claim the problem is solved.

## Evidence quality

Vendor announcement with a single headline metric from an internal, undisclosed benchmark and attacker; methodology is described qualitatively, numbers not independently reproducible. Honest about residual risk.

## Relevance to us

Q1/Q2. The relevant primitives for a merge are privilege curtailment (domain restriction, action confirmation) and classifiers on untrusted content: these are the parent-side controls that would gate what a returning part can do, independent of whether the part is corrupted. The ~1% residual ASR is a useful baseline for Q2 reasoning: if a single part fails ~1% of the time, a k-of-n merge needs enough honest parts that correlated failure stays below tolerance. Vendor counterpart to [[deepmind-2025-advancing]]; the design-pattern framing is [[simonwillison-2025-design]].
