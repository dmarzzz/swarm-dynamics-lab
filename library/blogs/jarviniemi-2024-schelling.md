---
id: jarviniemi-2024-schelling
type: blog
title: Schelling game evaluations for AI control
authors:
- Olli Järviniemi
year: 2024
url: https://www.alignmentforum.org/posts/n2c62YS8RJtD4Aqhh/schelling-game-evaluations-for-ai-control
site: AI Alignment Forum
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-w3
accessed: '2026-10-03'
read_depth: skim
relevance: 4
---

## Summary

The post turns possible coordination between an untrusted policy and monitor into concrete evaluation proposals. It separates agreement on unusual inputs from covert signals embedded in actions, and proposes tests for shared focal points, scoring consistency, training transfer, and adversarial coordination under human countermeasures.

## Key claims

- Four proposed projects cover identifying a shared focal element, comparing selection with independent classification, training/generalization, and non-obvious adversarial focal points.
- A toy information argument links a monitor failure rate of 1 in 1,000 synthetic attacks to roughly 10 bits of evidence distinguishing deployment from evaluation; this is not an observed model result.
- Copies of the same model versus different models, formatting perturbations, and paraphrasing are explicit experimental variables.
- Fine-tuning can improve coordination while making an evaluation less representative of spontaneous zero-shot behavior; this tension is unresolved.

## Evidence quality

Research agenda and conceptual threat analysis, with links to existing evaluations rather than a completed benchmark. The post mentions initial prompting observations but gives no systematic numeric capability results. Skimmed the setup, proposals, and conclusion.

## Relevance to us

Offers test designs for whether forked reviewers can agree on hidden triggers without direct messaging. Complements [[buck-2024-how]] and [[mallen-2024-measuring]]; proposed experiments are not established collusion capabilities.
