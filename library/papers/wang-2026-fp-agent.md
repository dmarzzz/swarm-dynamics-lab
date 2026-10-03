---
id: wang-2026-fp-agent
type: paper
title: 'FP-Agent: Fingerprinting AI Browsing Agents'
authors:
- Ethan Wang
- Zubair Shafiq
- Yash Vekaria
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.01247
doi: null
arxiv: '2605.01247'
cite: 'Wang, E., Shafiq, Z., & Vekaria, Y. (2026). FP-Agent: Fingerprinting AI Browsing Agents. arXiv preprint arXiv:2605.01247.'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

A controlled measurement of seven AI browsing agents and human users on an instrumented honey website, each performing three tasks (flight booking, online shopping, forum interaction). Browser and behavioural (typing, scrolling, mouse) fingerprints feed a multi-class classifier, FP-Agent. Browser fingerprints separate agents poorly when several agents share the same browser stack; behavioural fingerprints separate agents from humans and from each other. In a case study, FP-Agent detected all seven agents while Cloudflare's bot detection detected one.

## Contribution

Shows that behaviour on a honeysite, not static browser fingerprints, is what identifies browser-native LLM agents, and that a major commercial bot defence missed six of seven.

## Key results

- 7 agents, 3 tasks, plus human baseline on a honey website (abstract).
- Behavioural features (typing, scrolling, mouse) distinguish agents from humans and from each other; browser fingerprints alone are limited when shared (abstract).
- Cloudflare detected 1 of 7 agents; FP-Agent 7 of 7 (abstract, case study).

## Methods and models

Instrumented honey website; browser and behavioural fingerprint collection; multi-class classifier. Abstract-level read; found by backward citation from [[fayolle-2026-internet]].

## Limitations and open questions

Abstract only; lab-driven agents, not wild traffic.

## Relevance to us

Complements [[fayolle-2026-internet]] (single-request network/TLS/browser layers): behaviour is the layer that survives when agents run in real browsers. For swarms, behavioural similarity across sessions is also a same-operator signal. Shares an author (Shafiq) with [[farooqi-2020-canarytrap]].
