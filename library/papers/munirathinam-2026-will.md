---
id: munirathinam-2026-will
type: paper
title: "Will the Agent Recuse, and Will It Stop? Measuring LLM-Agent Compliance with In-Band Governance Signals at the Access Door and Mid-Flight"
authors: ["Thamilvendhan Munirathinam"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2606.06460
doi: "10.48550/arXiv.2606.06460"
arxiv: "2606.06460"
cite: "Munirathinam, T. (2026). Will the Agent Recuse, and Will It Stop? Measuring LLM-Agent Compliance with In-Band Governance Signals at the Access Door and Mid-Flight. arXiv preprint arXiv:2606.06460."
topics: ["swarm-detection", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Munirathinam proposes a Recuse Signal, an in-band request (SSH banner, PostgreSQL NOTICE, Kubernetes admission warning) asking a connecting or running LLM agent to withdraw, and measures compliance over SSH across five agents. At connection time, recusal on 'deny' ranges from 100% to 55 to 75% depending on model, and an open-weights agent barely engaged. Mid-task halts are weaker: two OpenAI models stopped 0 of 40 times, Gemini 2.5 Flash stopped 80%. An authorisation framing flipped GPT-4o to proceed. A harness-level interceptor stopped the loop 120 of 120 times across six models.

## Contribution

Measures whether agents honour a robots.txt-like cooperative signal on non-web protocols; finds cooperation is model-dependent and unreliable, so enforcement must sit in the harness.

## Key results

- Measured (abstract): access-time deny compliance 100% to 55 to 75% across agents that received it.
- Measured (abstract): no over-recusal on throttle/warn (0/176); no agent surfaced a warn (0/100).
- Measured (abstract): mid-flight halt stopped 0/40 for two OpenAI models; Gemini 2.5 Flash 80%.
- Measured (abstract): harness interceptor 120/120 vs 23% cooperative baseline.

## Methods and models

Open mini-standard with deny/throttle/warn and halt; adapters for SSH, PostgreSQL, Kubernetes; SSH experiments across five agents. Abstract only.

## Limitations and open questions

Single author, small trial counts per condition; SSH only for the main measurements.

## Relevance to us

A differential-compliance probe: how an agent reacts to an in-band 'please leave' differs by model, which could itself fingerprint the model behind an anonymous agent. Speculative; untested here. Compare refusal behaviour observed in [[fayolle-2026-internet]] and [[ousat-2026-broken]].
