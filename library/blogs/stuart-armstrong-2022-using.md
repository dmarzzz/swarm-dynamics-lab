---
id: stuart-armstrong-2022-using
type: blog
title: Using GPT-Eliezer against ChatGPT Jailbreaking
authors:
- Stuart_Armstrong
year: 2022
url: https://www.alignmentforum.org/posts/pNcFYZnPdXyL2RfgA/using-gpt-eliezer-against-chatgpt-jailbreaking
site: AI Alignment Forum
topics:
- fork-merge-security
- llm-agent-swarms
added_by: shadow/sol-w3
accessed: '2026-10-03'
read_depth: skim
relevance: 3
---

## Summary

This early prompt-filtering proposal places a second ChatGPT instance before the main chatbot, asking it to evaluate whether an incoming request is safe. Selected jailbreak examples are rejected, but the author explicitly notes that confusing user text with evaluator instructions can also compromise the evaluator itself.

## Key claims

- The evaluator produces a yes/no decision and explanation; only accepted requests reach the main chatbot.
- The post supplies selected examples involving role-play and indirect harmful requests, not a representative attack success rate.
- An edit acknowledges SQL-injection-like instruction confusion and suggests stronger separation of user text from evaluation instructions.
- Recursive evaluators are suggested but not demonstrated to provide an independent security boundary.

## Evidence quality

Illustrative proof of concept linked to a GitHub example repository; no statistical robustness evaluation or independent replication was checked. Read the post text and examples, not the linked implementation. Attribution in the introduction credits Rebecca Gorman with ideation and design.

## Relevance to us

A historical baseline for inspecting untrusted sub-agent text before merge. The useful lesson is that a reviewer exposed to attacker-controlled text needs its own trust boundary; selected refusals alone do not establish safe reintegration.
