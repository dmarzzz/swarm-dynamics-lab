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
- llm-agent-swarms
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

## Notes from dmarz/sd-web-agents

This lane catalogued the same source independently (added_by dmarz/sd-web-agents, accessed 2026-10-03). Its distinct content:

- Frontmatter `doi` in this lane's version: 10.48550/arXiv.2605.01247
- Frontmatter `read_depth` in this lane's version: full
- Frontmatter `citations` in this lane's version: 2 (Semantic Scholar, 2026-10-03)
- Frontmatter `code` in this lane's version: [gh-ethanbwang-fp-agent]

### Summary

Wang, Shafiq and Vekaria (UC Davis) ran seven browsing agents (OpenAI Atlas Agent, ChatGPT Agent, Claude for Chrome, Perplexity Comet, Manus, Browser Use, Skyvern) for 1,000 trials each across flight-booking, shopping and forum tasks on an instrumented honey website, and collected 546 human sessions from 56 students. They collected FingerprintJS browser fingerprints and custom behavioural features (typing latencies, change and input events, scroll bursts, mouse curvature) and trained XGBoost classifiers. Browser fingerprints alone give F1 around 0.8 because several agents share one fingerprint on the same OS; behavioural and combined features are near perfect. Every agent teleports the pointer to click targets with no continuous mouse movement. With Cloudflare's free AI Crawl Control and Block AI Bots enabled, only Manus (a self-declared verified bot) was blocked; FP-Agent detected all seven.

### Contribution

First controlled measurement of browser plus behavioural fingerprints for commercial browsing agents, and a direct comparison with a deployed commercial bot defence. Behavioural signals beat static fingerprints, the opposite emphasis from [[fayolle-2026-internet]].

### Key results

- Measured: browser-fingerprint classifier F1 about 0.8; behavioural and combined classifiers near-perfect (Table 2).
- Measured: no agent produced continuous mouse movement; each click is a single mousemove then mousedown/mouseup at the target.
- Measured: typing styles differ by agent: ChatGPT Agent, Atlas and Comet paste; Browser Use, Skyvern and Manus type with mean inter-key latency 5.31, 9.52 and 1.39 ms; ChatGPT Agent pastes with Ctrl+V even when reporting MacIntel.
- Measured: ChatGPT Agent reports 13 CPU cores and only the Calibri font; Manus reports Linux x86_64, 4 GB RAM, 6 cores, no fonts.
- Measured: Cloudflare free bot management blocked 1 of 7 agents (Manus); FP-Agent detected 7 of 7.
- Measured: held-out-task generalisation drops behavioural F1 by up to 0.369 while the combined classifier drops at most 0.0684.
- Measured: real-time F1 plateaus after about 1 minute (combined) and 3 minutes (behavioural).

### Methods and models

Visitor-specific random-path subpages for ground truth; 1,000 trials per agent split over tasks and OSes (macOS, Ubuntu, Windows); XGBoost with SHAP; Mann-Whitney U and Brown-Forsythe tests on feature differences. Code: https://github.com/ethanbwang/fp-agent; data on OSF.

### Limitations and open questions

Closed-world; humans are undergraduates on their own machines; three task types; agents run with default settings, so no adversarial humanisation. The authors expect the arms race to erode the mouse and typing signals once agents imitate human motion. Cloudflare comparison uses only the free tier.

### Relevance to us

The teleporting-cursor and paste-typing signatures are cheap to collect and, today, separate every tested agent from humans. That gives a swarm detector a per-session agent flag; clustering identical behavioural fingerprints across sessions would then expose many sessions from one agent product. The Cloudflare result is a measured negative for deployed defences. See also [[choudhary-2026-what]], which explains the same absence-of-motion signal as a CDP artifact, and [[fayolle-2026-internet]], [[kang-2026-whose]].

## Notes from dmarz/sd-attribution

Folded in by dmarz/sd-merge from the duplicate entry `wang-2026-fp` (added_by dmarz/sd-attribution, accessed 2026-10-03, read_depth abstract, relevance 4). Same source (same arXiv id); the kept id uses the full first title word FP-Agent.

- Frontmatter `cite` in the folded entry: 'Wang, E., Shafiq, Z., & Vekaria, Y. (2026). FP-Agent: Fingerprinting AI Browsing Agents. arXiv:2605.01247.'
- Frontmatter `relevance` in the folded entry: 4

### Summary

First controlled measurement of seven AI browsing agents and humans on an instrumented honey website performing flight booking, shopping and forum tasks. Browser fingerprints discriminate poorly when several agents share them, but behavioural fingerprints (typing, scrolling, mouse) separate agents from humans and from one another. In a case study FP-Agent detects all seven agents while Cloudflare's bot detection detects one.

### Contribution

Shows commercial bot detection largely misses AI browsing agents and that behavioural features close the gap.

### Key results

- FP-Agent detects 7 of 7 agents; Cloudflare detects 1 of 7 (abstract).
- Browser fingerprints have limited power when shared; behavioural fingerprints are distinctive (abstract).

### Methods and models

Honey website, three tasks, multi-class classifier over browser and behavioural features.

### Limitations and open questions

Abstract-only reading; seven agents.

### Relevance to us

Measured gap between deployed bot defences and agents, relevant to base rates: agent traffic counted by Cloudflare-style tools is likely an undercount. Related: [[choudhary-2026-what]], [[lugoloobi-2026-known]].
