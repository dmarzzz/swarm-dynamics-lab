---
id: salman-2026-how
type: paper
title: "How Effective Is Mouse Dynamics Against Web Bots? A Study Across Different Sophistication Levels"
authors: ["Oguzhan Salman", "Kemal Bicakci"]
year: 2026
venue: "IEEE Access, vol. 14"
url: https://www.semanticscholar.org/paper/79e9ef0a3411b1419158664d6eff7ef6bc370f51
doi: "10.1109/ACCESS.2026.3681065"
arxiv: null
cite: "Salman, O., & Bicakci, K. (2026). How Effective Is Mouse Dynamics Against Web Bots? A Study Across Different Sophistication Levels. IEEE Access, 14, 57895-57909. https://doi.org/10.1109/ACCESS.2026.3681065."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: "0 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Salman and Bicakci collect mouse data on two custom websites and test three defensive layers against bots ranging from synthetic trajectories to replays of real human sessions: supervised and unsupervised ML on behaviour, Dynamic Time Warping against historical traces, and click-pattern rules. Random Forest detects all synthetic attacks and most cross-domain replays; unsupervised models fail on context-mismatched replay; DTW is needed for same-domain replay. No single method covers all threats.

## Contribution

Shows replay attacks are the hard case for mouse dynamics and need history-based matching, which matters once agents learn to replay human traces.

## Key results

- Measured (abstract): Random Forest perfect on synthetic attacks; detects the majority of cross-domain replays.
- Measured (abstract): unsupervised models struggle with context-mismatched replay; DTW effective for same-domain replay.

## Methods and models

Two custom websites, ML classifiers, DTW, click-pattern rules. Abstract only.

## Limitations and open questions

Abstract only; no LLM agents.

## Relevance to us

Replay of human traces is the evasion level [[choudhary-2026-what]] says still fails under CDP; this paper shows that if raw events were replayed at OS level, history matching (DTW) is the fallback. Same group as [[salman-2026-captchas]] and [[jarad-2026-when]].
