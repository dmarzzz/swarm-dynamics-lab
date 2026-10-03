---
id: reworr-2024-llm
type: paper
title: 'LLM Agent Honeypot: Monitoring AI Hacking Agents in the Wild'
authors:
- Reworr
- Dmitrii Volkov
year: 2024
venue: arXiv preprint
url: https://arxiv.org/html/2410.13919
doi: null
arxiv: '2410.13919'
cite: 'Reworr, & Volkov, D. (2024). LLM Agent Honeypot: Monitoring AI Hacking Agents in the Wild. arXiv preprint arXiv:2410.13919.'
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: null
code: []
---

## Summary

Palisade Research augmented a Cowrie SSH honeypot with prompt injections planted in the SSH banner, in common command outputs (e.g. `uname`) and in readable system files, then deployed it on 10 IP addresses in several countries, advertised via Shodan/Censys and DNS names that look sensitive (e.g. `gov-defense-dev.il`). A session is a "potential AI agent" if it obeys a goal-hijacking injection (AgentDojo-style "Important Message"), and a "confirmed AI agent" if it also answers fast enough to rule out a human (internal GPT-4o agents replied within about 1.7 s; humans take several seconds). Over about three months the system logged 8,130,731 interaction attempts and flagged 8 potential AI agents.

## Contribution

The first public in-the-wild measurement instrument aimed specifically at LLM agents rather than scripted bots or humans, and the first base-rate estimate of autonomous LLM attackers on the open internet: essentially zero (8 in 8.1M) as of late 2024.

## Key results

- 8,130,731 interaction attempts over roughly three months; 8 sessions passed the prompt-injection test (measured).
- Internal calibration: GPT-4o agents reply in about 1.7 s even to injections; most bot traffic in the wild also answers in under 1.7 s, so timing alone separates humans from machines but not LLMs from scripts (measured, figure-level).
- "Important Message" goal hijacks beat "ignore previous instructions"; prompt-stealing success drops sharply, so they hijack first and steal the system prompt second (measured on internal agents, no numbers in text).
- One flagged session responded to injections but with 10+ s gaps, which the authors read as a human operator who happened to comply: a false-positive mode of the injection test (observation).
- Live dashboard (ai-honeypot.palisaderesearch.org, read 2026-10-03): 24,111,509 interactions, 14 potential AI agents (passed injection test), 3 confirmed (passed injection and timing), with monthly tracking listed as "2026-05 still in progress" (dashboard figures, not peer-reviewed).
- No system prompt was successfully extracted from any wild agent (reported for the fast-response case).

## Methods and models

Three-way classification (software bot / LLM agent / human). Test 1: injection that asks a question needing language understanding (scripts cannot pass). Test 2: response latency (humans cannot pass). Customised Cowrie following Cabral et al.'s deceptiveness recommendations. Public dashboard at ai-honeypot.palisaderesearch.org.

## Limitations and open questions

SSH only; one slice of internet traffic; assumes scripts never answer language questions and humans are never fast. No false-positive or false-negative rate is estimated. Read in full: the paper is short (about 2,900 words) and preliminary. An LLM agent instructed to ignore in-band instructions, or one with human-paced tool latency, evades both tests.

## Relevance to us

The canonical "trap that makes an agent reveal itself" design, and the only published base rate of wild autonomous attacking agents. The two-factor test (semantic compliance plus latency) transfers to any channel where we control responses: social replies, API responses, web pages. Evasion side: [[cordeiro-2026-rouxii]], [[xie-2026-llm-based]]. Defensive sibling: [[pasquini-2024-hacking]]. Policy framing that recommends agent honeypots: [[mittelsteadt-2026-detecting]].
