---
id: simonwillison-2025-design
type: blog
title: "Design Patterns for Securing LLM Agents against Prompt Injections"
authors: [Simon Willison]
year: 2025
url: https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/
site: Simon Willison's Weblog
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Willison reviews the 14-author paper (IBM, Invariant Labs, ETH Zurich, Google, Microsoft) that proposes six design patterns constraining agents so untrusted input cannot trigger consequential actions. The patterns he lists: Action-Selector (agent can fire tools but never sees their responses), Plan-Then-Execute (fix the plan before touching untrusted data), LLM Map-Reduce, Dual LLM, Code-Then-Execute (the CaMeL approach), and Context-Minimization. He endorses the paper's guiding principle, quoted in full: once an agent has ingested untrusted input it must be constrained so that input cannot trigger actions with negative side effects. He underlines the paper's own admission that general-purpose agents on current models cannot give reliable safety guarantees, so the useful question is which restricted agents still do useful work.

## Key claims

- Six named patterns each trade away some agent generality for prompt-injection resistance; none is a universal fix (from the paper).
- The "taint" principle: any exposure to malicious tokens should be treated as giving the attacker control of the subsequent output and tool calls.
- General-purpose agents and their current-model defenses cannot offer meaningful safety guarantees (quoted from the paper).

## Evidence quality

Practitioner review of a multi-institution paper; the patterns and their guarantees are the paper's, summarized approvingly. No new experiments.

## Relevance to us

Q1/Q2. The six patterns are a menu of merge disciplines: Plan-Then-Execute fixes the parent's plan before any returning part's data arrives (so a corrupted part cannot rewrite the goal); Action-Selector denies the return channel any feedback path into the parent; Dual LLM / Code-Then-Execute quarantine what a part brings home. These are structural (constrain-the-merge) answers, complementary to a k-of-n threshold (Q2). Reviews the paper [[beurer-kellner-2025-design]]; same author on the trifecta [[simonwillison-2025-lethal]] and CaMeL [[simonwillison-2025-camel]].
