---
id: reworr-2024-llm
type: paper
title: "LLM Agent Honeypot: Monitoring AI Hacking Agents in the Wild"
authors: ["Reworr", "Dmitrii Volkov"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2410.13919
doi: null
arxiv: "2410.13919"
cite: "Reworr, & Volkov, D. (2024). LLM Agent Honeypot: Monitoring AI Hacking Agents in the Wild. arXiv:2410.13919."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Palisade Research deployed a public SSH honeypot (modified Cowrie) seeded with prompt injections in the login banner, command outputs and files, to catch autonomous LLM hacking agents in the wild. An agent that obeys an injected goal-hijack instruction is flagged as a potential AI agent; one that also answers within about 1.5 to 1.7 seconds is counted as confirmed. Over roughly three months on 10 IPs the system logged 8,130,731 interaction attempts and 8 potential AI agents.

## Contribution

One of the first measured base rates of autonomous LLM agents attacking real infrastructure, and a concrete two-signal detector: behavioural compliance with a prompt injection (separates LLMs from scripts) plus response latency (separates LLMs from humans).

## Key results

- 8,130,731 interaction attempts; 8 potential AI agents (passed prompt-injection test); the dashboard distinguishes 1 confirmed agent that also passed the timing test (abstract, Section 4.1).
- Internal tests: GPT-4o agents replied within about 1.7 s even to injections; most bots in the wild also replied within 1.7 s (Figure 4).
- AgentDojo-style "Important Message" injections outperformed "ignore previous instructions"; success dropped when the goal was prompt stealing (Figures 1, 2).
- Example: one session complied with the injection but took over 10 s between commands, which the authors read as a human operator who happened to comply.

## Methods and models

Cowrie SSH honeypot with vulnerable SSH version, altered default users and outputs; injections in banner, uname-style command output and readable files; two-step injection (goal hijack, then prompt stealing). Attraction: sensitive-looking DNS names, indexing on Shodan and Censys, 10 IPs in several countries. Short workshop-style paper; figures carry most of the data.

## Limitations and open questions

Tiny positive count, no ground truth for the 8 detections, and the 1.5 to 1.7 s threshold is calibrated on the authors' own GPT-4o agents. Agents with system-prompt defences against injection, or deliberate delays, evade both tests. Covers SSH only. The authors list these limitations themselves.

## Relevance to us

The canonical in-the-wild agent honeypot and base-rate measurement for this lane; the same two signals (injection compliance, latency) recur in [[ediga-2026-trace]] and [[park-2026-cross]]. Model attribution of caught agents could use [[pasquini-2024-llmmap]] or [[white-2026-black]] on the honeypot transcripts. Measured rate is very low (8 in 8.1M), a useful prior for any swarm-detection claim.
