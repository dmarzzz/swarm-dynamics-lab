---
id: ediga-2026-trace
type: paper
title: "Trace: Unmasking AI Attack Agents Through Terminal Behavior Fingerprinting"
authors: ["Murali Ediga", "Sudipta Chattopadhyay"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.01186
doi: null
arxiv: "2605.01186"
cite: "Ediga, M., & Chattopadhyay, S. (2026). Trace: Unmasking AI Attack Agents Through Terminal Behavior Fingerprinting. arXiv:2605.01186."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: null
code: []
---

## Summary

Trace attributes AI penetration-testing agents to a model family from the terminal command sequences they run on a compromised Linux CTF box, then uses the inferred family to pick a defensive prompt injection that exfiltrates the attacker agent's system prompt. Over three scaffolds and seven frontier families it reaches macro F1 0.981 (0.815 on unseen scaffolds), and the tailored injection extracts system prompts from 81.9% of non-Claude sessions on average.

## Contribution

Combines passive attribution and active counter-injection into an attacker-agent forensics pipeline, extending the honeypot idea of [[reworr-2024-llm]] from detection to identification.

## Key results

- Model-family macro F1 0.981; 0.815 on unseen scaffolds (abstract).
- Defensive prompt injection extracts system prompts from 81.9% of non-Claude sessions on average, up to 98.3%, at 0.736 Sentence-BERT fidelity, 1.88x blind deployment.
- On a black-box proprietary scaffold using Gemini and Claude Opus, family identification averaged 78%; for Gemini the full system prompt was recovered and confirmed by the developers.

## Methods and models

Linux CTF environment, three attacker scaffolds, seven model families; classification over command sequences; family-specific injection payloads.

## Limitations and open questions

Abstract-level reading. Claude sessions largely resisted prompt extraction. Lab CTF, not wild traffic.

## Relevance to us

Shows that once a swarm agent is attributed to a family, defenders can tailor injections to make it reveal its instructions, a practical next step after honeypot detection. Compare [[wang-2026-who]] for coding agents and [[lugoloobi-2026-known]] for browsing agents.
