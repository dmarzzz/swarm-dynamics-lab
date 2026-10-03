---
id: deepmind-2025-advancing
type: blog
title: "Advancing Gemini's security safeguards"
authors: [Google DeepMind Security & Privacy Research Team]
year: 2025
url: https://deepmind.google/blog/advancing-geminis-security-safeguards/
site: Google DeepMind
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-informal
accessed: 2026-10-03
read_depth: full
relevance: 4
---

## Summary

Vendor post (20 May 2025) accompanying the white paper "Lessons from Defending Gemini Against Indirect Prompt Injections". The threat is indirect prompt injection: hidden malicious instructions in retrieved data (emails, documents, websites) that the model cannot reliably separate from genuine user instructions. Their central method is automated red teaming (ART): an internal team continuously generates adaptive attacks to probe Gemini. The key reported lesson is that baseline defenses tested only against static attacks (they name Spotlighting and Self-reflection) looked promising but became much less effective against adaptive attacks that evolve to bypass them, so static-attack evaluation gives a false sense of security. Their more durable approach is "model hardening": fine-tuning Gemini on ART-generated injection scenarios so it learns to ignore injected instructions and follow the original user request, which they report lowered attack success rate without significant loss on normal tasks. They stress defense-in-depth (model hardening + input/output classifiers + system-level guardrails) and that no model is fully immune.

## Key claims

- Defenses that pass static-attack tests (Spotlighting, Self-reflection) degrade substantially under adaptive red teaming; robustness must be measured against adaptive attacks.
- Model hardening via ART-generated fine-tuning data lowered ASR with little capability cost (vendor-reported, no numbers in the blog).
- Security requires layered deterministic and probabilistic defenses; the goal is to make attacks costlier, not to eliminate them.

## Evidence quality

Vendor announcement summarizing a white paper; qualitative, no quantified rates in the post itself. The adaptive-vs-static methodological point is the main transferable claim.

## Relevance to us

Q1/Q2. The adaptive-attacker lesson is a direct warning for any merge defence we design: a hiding scheme (Q1) or a k-of-n threshold (Q2) that only survives static attacks will likely fail against an adversary that adapts to it, so the evaluation of a fork-merge protocol must itself be adaptive. Model hardening is the per-part version of robustness that a threshold composes over. Vendor counterpart to [[anthropic-2025-mitigating]]; the CaMeL design direction from the same org is [[simonwillison-2025-camel]] / [[debenedetti-2025-defeating]].
