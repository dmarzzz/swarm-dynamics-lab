---
id: marro-2025-permission
type: paper
title: "Permission Manifests for Web Agents"
authors: ["Samuele Marro", "Alan Chan", "Xinxing Ren", "Lewis Hammond", "Jesse Wright", "Gurjyot Wanga", "Tiziano Piccardi", "Nuno Campos", "Tobin South", "Jialin Yu", "Sunando Sengupta", "Eric Sommerlade", "Alex Pentland", "Philip Torr", "Jiaxin Pei"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2601.02371
doi: "10.48550/arXiv.2601.02371"
arxiv: "2601.02371"
cite: "Marro, S., Chan, A., Ren, X., Hammond, L., Wright, J., Wanga, G., Piccardi, T., Campos, N., South, T., Yu, J., et al. (2025). Permission Manifests for Web Agents. arXiv preprint arXiv:2601.02371."
topics: ["swarm-detection", "llm-agent-swarms"]
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: "4 (Semantic Scholar, 2026-10-03)"
code: []
---

## Summary

Marro, Chan, Ren, Hammond, Wright and ten co-authors (Lightweight Agent Standards Working Group) propose agent-permissions.json, a robots.txt-style manifest in which a site lists which interactions LLM web agents may perform, with API references where available. The goal is to replace blanket blocking and CAPTCHAs with a cooperative rule set, so sites can focus enforcement on agents that do not comply.

## Contribution

A cooperative-signalling proposal for agents, the agent-era counterpart of robots.txt.

## Key results

- Proposal only (abstract); no measurements.

## Methods and models

Specification of a JSON manifest. Abstract only.

## Limitations and open questions

Abstract only. Compliance is voluntary; measured compliance with analogous signals is partial ([[kim-2025-scrapers]], [[munirathinam-2026-will]]).

## Relevance to us

If adopted, non-compliance with the manifest becomes a detection signal: agents that ignore it self-select as suspect. Related identity work: [[south-2025-authenticated]], [[gh-cloudflare-web-bot-auth]].
