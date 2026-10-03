---
id: wang-2026-fp-agent
type: paper
title: "FP-Agent: Fingerprinting AI Browsing Agents"
authors: ["Ethan Wang", "Zubair Shafiq", "Yash Vekaria"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.01247
doi: "10.48550/arXiv.2605.01247"
arxiv: "2605.01247"
cite: "Wang, E., Shafiq, Z., & Vekaria, Y. (2026). FP-Agent: Fingerprinting AI Browsing Agents. arXiv preprint arXiv:2605.01247."
topics: ["swarm-detection", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: "2 (Semantic Scholar, 2026-10-03)"
code: ["gh-ethanbwang-fp-agent"]
---

## Summary

Wang, Shafiq and Vekaria (UC Davis) ran seven browsing agents (OpenAI Atlas Agent, ChatGPT Agent, Claude for Chrome, Perplexity Comet, Manus, Browser Use, Skyvern) for 1,000 trials each across flight-booking, shopping and forum tasks on an instrumented honey website, and collected 546 human sessions from 56 students. They collected FingerprintJS browser fingerprints and custom behavioural features (typing latencies, change and input events, scroll bursts, mouse curvature) and trained XGBoost classifiers. Browser fingerprints alone give F1 around 0.8 because several agents share one fingerprint on the same OS; behavioural and combined features are near perfect. Every agent teleports the pointer to click targets with no continuous mouse movement. With Cloudflare's free AI Crawl Control and Block AI Bots enabled, only Manus (a self-declared verified bot) was blocked; FP-Agent detected all seven.

## Contribution

First controlled measurement of browser plus behavioural fingerprints for commercial browsing agents, and a direct comparison with a deployed commercial bot defence. Behavioural signals beat static fingerprints, the opposite emphasis from [[fayolle-2026-internet]].

## Key results

- Measured: browser-fingerprint classifier F1 about 0.8; behavioural and combined classifiers near-perfect (Table 2).
- Measured: no agent produced continuous mouse movement; each click is a single mousemove then mousedown/mouseup at the target.
- Measured: typing styles differ by agent: ChatGPT Agent, Atlas and Comet paste; Browser Use, Skyvern and Manus type with mean inter-key latency 5.31, 9.52 and 1.39 ms; ChatGPT Agent pastes with Ctrl+V even when reporting MacIntel.
- Measured: ChatGPT Agent reports 13 CPU cores and only the Calibri font; Manus reports Linux x86_64, 4 GB RAM, 6 cores, no fonts.
- Measured: Cloudflare free bot management blocked 1 of 7 agents (Manus); FP-Agent detected 7 of 7.
- Measured: held-out-task generalisation drops behavioural F1 by up to 0.369 while the combined classifier drops at most 0.0684.
- Measured: real-time F1 plateaus after about 1 minute (combined) and 3 minutes (behavioural).

## Methods and models

Visitor-specific random-path subpages for ground truth; 1,000 trials per agent split over tasks and OSes (macOS, Ubuntu, Windows); XGBoost with SHAP; Mann-Whitney U and Brown-Forsythe tests on feature differences. Code: https://github.com/ethanbwang/fp-agent; data on OSF.

## Limitations and open questions

Closed-world; humans are undergraduates on their own machines; three task types; agents run with default settings, so no adversarial humanisation. The authors expect the arms race to erode the mouse and typing signals once agents imitate human motion. Cloudflare comparison uses only the free tier.

## Relevance to us

The teleporting-cursor and paste-typing signatures are cheap to collect and, today, separate every tested agent from humans. That gives a swarm detector a per-session agent flag; clustering identical behavioural fingerprints across sessions would then expose many sessions from one agent product. The Cloudflare result is a measured negative for deployed defences. See also [[choudhary-2026-what]], which explains the same absence-of-motion signal as a CDP artifact, and [[fayolle-2026-internet]], [[kang-2026-whose]].
