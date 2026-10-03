---
id: choudhary-2026-what
type: paper
title: "What Does It Take to Detect an AI Agent? Minimal Feature Sets for Behavioral Detection under Browser Automation"
authors: ["Vishisht Choudhary", "Lukas Schmidt", "Anne Zoë Kenntner", "Feras Skhab", "Michel Osswald", "Jens Ernstberger"]
year: 2026
venue: "North East AI Agents Day 2026 workshop; arXiv preprint"
url: https://arxiv.org/abs/2607.26935
doi: null
arxiv: "2607.26935"
cite: "Choudhary, V., Schmidt, L., Kenntner, A. Z., Skhab, F., Osswald, M., & Ernstberger, J. (2026). What Does It Take to Detect an AI Agent? Minimal Feature Sets for Behavioral Detection under Browser Automation. arXiv:2607.26935."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Argues that binary human-versus-bot detectors structurally misroute AI agents, and builds a three-class detector (human, bot, AI agent). Binary MLP and SAINT detectors misclassify 39.1% and 34.5% of real agents as human; adding an agent class gives agent F1 1.000 in 30 runs. Across a five-level evasion ladder including GAN trajectories and replayed human cursor data (2,299 sessions) there were zero agent misses, because Playwright does not emit the raw pointer-move and wheel-delta streams of physical devices. Two features (mouse_event_rate, teleport_click_ratio) give 100% agent recall.

## Contribution

Identifies the signal as a browser-automation absence signature, not evidence of reasoning, which says when detection will fail.

## Key results

- Binary detectors call 39.1% (MLP) and 34.5% (SAINT) of agents human (abstract).
- Three-class agent F1 1.000 across 30 runs; zero agent misses over 22,990 per-seed predictions under evasion (abstract).
- Two features reach 100% agent recall with precision 0.994; five features macro-F1 0.991 (abstract).

## Methods and models

Controlled benchmark; exhaustive search over feature subsets of size 1-5 (9,401 GBMs); evasion ladder.

## Limitations and open questions

The authors stress the signal is an automation artefact: agents driving real input devices or OS-level injection would not show it. Abstract-only reading.

## Relevance to us

A clear statement of what current agent detection actually keys on, and therefore of its expiry date. Related: [[wang-2026-fp]], [[rmus-2026-process]].
