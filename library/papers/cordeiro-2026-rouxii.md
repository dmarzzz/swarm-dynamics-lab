---
id: cordeiro-2026-rouxii
type: paper
title: 'Rouxii: Exploiting Honeypots with Deception-Aware AI Pentesters'
authors:
- Arthur Cordeiro
- Alberto Maria Mongardini
- Emmanouil Vasilomanolakis
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2609.26555
doi: null
arxiv: '2609.26555'
cite: 'Cordeiro, A., Mongardini, A. M., & Vasilomanolakis, E. (2026). Rouxii: Exploiting Honeypots with Deception-Aware AI Pentesters. arXiv preprint arXiv:2609.26555.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: null
code: []
---

## Summary

An evasion result. Rouxii is an LLM-orchestrated pentest framework with deterministic reconnaissance and exploitation operators. Two matched cohorts differ only in the system prompt: "vanilla" sees raw probe output; "anti-deception" also gets known honeypot fingerprint signals and a classification rule. Across three reasoning models, eleven network setups and twelve cycles (1,544 attack reports), correct honeypot identification rose from 19% to 97% (OT services 11% to 97%) with 0.7% false alarms on real services. Deception-unaware baselines (PentestGPT, HackingBuddy) behaved like the vanilla cohort. A white-box analysis then turned detected honeypots against their operators: a malformed Modbus header hangs Conpot while TCP liveness checks still pass, and a one-byte gate lets an attacker overwrite GasPot's station name, corrupting the intelligence it reports.

## Contribution

The strongest negative result in this lane: honeypot efficacy against AI attackers is a function of what the attacker's prompt knows, and published fingerprints are cheap to hand an agent. The authors find "framing, not evidence, is the binding constraint": both cohorts saw the same signals at nearly the same rates.

## Key results

- Honeypot identification 19% (vanilla) vs 97% (anti-deception); OT 11% vs 97%; false alarm on real service 0.7% (measured, 1,544 reports).
- Demonstrated DoS of Conpot invisible to liveness monitoring; demonstrated intelligence corruption of GasPot; a Cowrie address-filter flaw shown as a primitive toward "deception overflow" (not demonstrated end-to-end).
- Adapts Honeyquest probes ([[kahlhofer-2024-honeyquest]]) to LLM attackers to measure enticingness and detection.

## Methods and models

Testbed of Cowrie, Conpot, GasPot plus real services; LLM orchestrator as the only stochastic component; verdicts scored against a deterministic oracle; SIG_CHAIN check that a verdict cites concrete signals. Skimmed: intro, related work, threat model, honeypot-exploitation section and framework design.

## Limitations and open questions

Open-source, well-fingerprinted honeypots only; custom or LLM-generated honeypots ([[bridges-2025-sok]]) may be harder. The "aware" prompt encodes fingerprints already published, which is realistic for a capable operator.

## Relevance to us

Any trap we design for swarms must assume the operator can paste our published tells into the agent's system prompt. It argues for per-deployment randomised canaries (as in [[seiden-2026-identifying]]) over a fixed honeypot product. Contrast with [[pasquini-2024-hacking]] and [[reworr-2024-llm]], which assume unaware agents; theoretical counterpart in [[gans-2026-when]].
