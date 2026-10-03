---
id: ariyarathne-2026-behavior
type: paper
title: "Behavior Change as a Signal for Identifying Social Media Manipulation"
authors: ["Isuru Ariyarathne", "Gangani Ariyarathne", "Alessandro Flammini", "Filippo Menczer", "Alexander C. Nwala"]
year: 2026
venue: "Proceedings of the 18th ACM Web Science Conference (WebSci)"
url: https://arxiv.org/abs/2603.03128
doi: "10.1145/3795766.3799748"
arxiv: "2603.03128"
cite: "Ariyarathne, I., Ariyarathne, G., Flammini, A., Menczer, F., & Nwala, A. C. (2026). Behavior Change as a Signal for Identifying Social Media Manipulation. In Proceedings of the 18th ACM Web Science Conference (pp. 349–358). ACM."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Represents each account's behaviour as a string in the Behavioral Languages for Online Characterization (BLOC), segments it, measures change between consecutive segments, and uses the distribution of change values as features for supervised classifiers. Applied to bot detection and to information-operation detection. Authentic accounts show consistent change distributions; bots show very low or very high change; coordinated inauthentic accounts share similar change distributions within a campaign that differ across campaigns.

## Contribution

Uses within-campaign similarity of behavioural drift, rather than co-action, as a coordination signature.

## Key results

- Coordinated accounts in the same campaign have highly similar behaviour-change distributions (abstract).
- "Good accuracy" on both tasks (abstract; no numbers there).

## Methods and models

BLOC symbolic encoding of actions and content, segment-wise change measures, supervised classifiers.

## Limitations and open questions

Abstract only. Supervised; needs labelled campaigns.

## Relevance to us

Agents run from one prompt or policy update would change behaviour together; shared drift is a signature that survives paraphrase. Related: [[seckin-2024-labeled]].
