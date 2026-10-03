---
id: kahlhofer-2024-honeyquest
type: paper
title: 'Honeyquest: Rapidly Measuring the Enticingness of Cyber Deception Techniques with Code-based Questionnaires'
authors:
- Mario Kahlhofer
- Stefan Achleitner
- Stefan Rass
- René Mayrhofer
year: 2024
venue: 27th International Symposium on Research in Attacks, Intrusions and Defenses (RAID 2024)
url: https://arxiv.org/abs/2408.10796
doi: 10.1145/3678890.3678897
arxiv: '2408.10796'
cite: 'Kahlhofer, M., Achleitner, S., Rass, S., & Mayrhofer, R. (2024). Honeyquest: Rapidly Measuring the Enticingness of Cyber Deception Techniques with Code-based Questionnaires. In Proceedings of the 27th International Symposium on Research in Attacks, Intrusions and Defenses (RAID 2024). https://doi.org/10.1145/3678890.3678897'
topics:
- swarm-detection
added_by: dmarz/sd-honeypots
accessed: '2026-10-03'
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Translates 13 previously studied and 12 new deception techniques (honeytokens and similar) into a machine-readable specification. The open-source Honeyquest tool presents participants with code-based questionnaires instead of live systems. In an experiment with 47 humans testing 25 deception techniques and 19 true security risks, the presence of deception reduced the chance that an adversary finds a true risk by about 22% on average.

## Contribution

A cheap, repeatable way to measure how enticing a trap is without building it. [[cordeiro-2026-rouxii]] later adapted it to LLM attackers.

## Key results

- 25 deception techniques and 19 true risks; 47 human participants; deception reduced true-risk discovery by about 22% on average (abstract).

## Methods and models

Code-based questionnaires; specification language for deception techniques. Abstract-level read.

## Limitations and open questions

Human participants only in this paper; enticingness for LLM agents differs ([[ayzenshteyn-2025-cloak]] reports agents follow blatant lures).

## Relevance to us

A ready protocol for ranking candidate swarm baits before deployment: run the questionnaire on LLM agents and on humans and pick baits with the largest gap. Background in [[zhang-2021-three]].
