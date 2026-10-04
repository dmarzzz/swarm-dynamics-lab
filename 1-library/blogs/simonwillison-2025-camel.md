---
id: simonwillison-2025-camel
type: blog
title: "CaMeL offers a promising new direction for mitigating prompt injection attacks"
authors: [Simon Willison]
year: 2025
url: https://simonwillison.net/2025/Apr/11/camel/
site: Simon Willison's Weblog
topics: [fork-merge-security, llm-agent-swarms, sync-consensus]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 5
---

## Summary

Willison walks through Google DeepMind's CaMeL ("Capabilities for Machine Learning"), the design behind the paper "Defeating Prompt Injections by Design". A privileged LLM (P-LLM) sees only the user's request and compiles it into a locked-down subset of Python; a quarantined LLM (Q-LLM) with no tool access does the parsing of untrusted data into typed values. A custom interpreter tracks data provenance (which variables derive from untrusted sources) and enforces capability policies, so untrusted-derived values cannot flow into sensitive tool arguments such as an email recipient. The post is also notable because the DeepMind paper identifies a concrete flaw in Willison's own earlier Dual-LLM pattern: even with planning isolated, the Q-LLM's extraction of a value like a recipient address is still attacker-influenceable, so an exfiltration address can be overridden. CaMeL closes that by making the interpreter, not an LLM, decide whether a tainted value may reach a consequential call.

## Key claims

- Isolating planning (Dual-LLM) is insufficient: a value extracted by the quarantined LLM from untrusted text can still be poisoned, enabling redirection of an action (DeepMind's Figure 1 example).
- Provenance tracking plus capability policies in a deterministic interpreter can block tainted data from reaching sensitive sinks without using more AI for the security decision.
- CaMeL is a design direction, not a complete solution; Willison notes residual limits ("camels have two humps").

## Evidence quality

Practitioner explainer of a peer research paper, with code-level walkthrough. Security properties come from the paper's design, not from the blog's own experiments.

## Relevance to us

Directly on Q1/Q2/Q3. The Dual-LLM flaw is the fork-merge problem in miniature: a sub-task delegated to an untrusted-exposed component returns a value that silently steers the parent's action. CaMeL's answer is a merge discipline: the parent treats everything a returning part produces as tainted and lets only a deterministic policy decide if it may influence a consequential step (Q2-style, a constraint rather than a trust vote). Companion to [[simonwillison-2025-lethal]] and [[simonwillison-2025-design]]; the paper is [[beurer-kellner-2025-design]] and the CaMeL paper itself is [[debenedetti-2025-defeating]].
