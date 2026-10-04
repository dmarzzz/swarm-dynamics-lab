---
id: iliou-2021-detection
type: paper
title: "Detection of Advanced Web Bots by Combining Web Logs with Mouse Behavioural Biometrics"
authors: ["Christos Iliou", "Theodoros Kostoulas", "Theodora Tsikrika", "Vasilis Katos", "Stefanos Vrochidis", "Ioannis Kompatsiaris"]
year: 2021
venue: "Digital Threats: Research and Practice"
url: https://www.semanticscholar.org/paper/9dfafc50d4723ac01f3b2c67dc94a11e914c0214
doi: "10.1145/3447815"
arxiv: null
cite: "Iliou, C., Kostoulas, T., Tsikrika, T., Katos, V., Vrochidis, S., & Kompatsiaris, I. (2021). Detection of Advanced Web Bots by Combining Web Logs with Mouse Behavioural Biometrics. Digital Threats: Research and Practice, 2(3), 1-26. https://doi.org/10.1145/3447815."
topics: ["swarm-detection"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "28 (Crossref, 2026-10-03)"
code: []
---

## Summary

Iliou, Kostoulas, Tsikrika, Katos, Vrochidis and Kompatsiaris build a two-module web bot detector: one module on web server logs and one on mouse movements, fused to capture the temporal patterns of logs and the spatial and temporal patterns of mouse traces. Tested on moderate bots (browser-like fingerprint) and advanced bots (browser fingerprint plus humanlike behaviour), the combined detector is more effective and more robust to evasion than either module alone.

## Contribution

Widely cited baseline for combining server logs with behavioural biometrics against humanlike bots; [[choudhary-2026-what]] uses its bot archetypes.

## Key results

- Measured (abstract): combining logs and mouse movements beats either alone on advanced humanlike bots; numeric results not in the abstract.

## Methods and models

Web-log features and mouse-movement features, separate classifiers, fusion. Abstract from Crossref record.

## Limitations and open questions

Abstract only; synthetic bot populations; pre-LLM.

## Relevance to us

Multi-modal fusion is the pattern all three 2026 agent papers converge on ([[fayolle-2026-internet]], [[kang-2026-whose]], [[wang-2026-fp-agent]]).
