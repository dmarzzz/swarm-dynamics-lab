---
id: seckin-2024-labeled
type: paper
title: "Labeled Datasets for Research on Information Operations"
authors: ["Ozgur Can Seckin", "Manita Pote", "Alexander Nwala", "Lake Yin", "Luca Luceri", "Alessandro Flammini", "Filippo Menczer"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2411.10609
doi: null
arxiv: "2411.10609"
cite: "Seckin, O. C., Pote, M., Nwala, A., Yin, L., Luceri, L., Flammini, A., & Menczer, F. (2024). Labeled Datasets for Research on Information Operations. arXiv:2411.10609."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "15 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Platforms have released archives of information operations they attributed to states, but no matched control data. This paper releases labelled datasets for 26 campaigns that pair platform-verified IO posts with control data: over 13 million posts by 303k accounts who discussed similar topics in the same time frames. The intent is benchmarking IO and coordination detectors against organic baselines.

## Contribution

Supplies the control class that most coordination studies lack; it is the data behind the negative result in [[pante-2025-beyond]].

## Key results

- 26 campaigns; control set of over 13M posts by 303k accounts (abstract).

## Methods and models

Control accounts sampled by topic (hashtags) over each campaign's time frame. Data released by the authors (access details not in the abstract).

## Limitations and open questions

Abstract only. Labels are X's attributions. Topic-based sampling of controls may not match the IO conversation exactly ([[pante-2025-beyond]] notes this).

## Relevance to us

The best available labelled benchmark with organic controls for coordinated human-run operations. No equivalent exists yet for LLM-agent swarms; [[mukherjee-2026-moltgraph]] has only weak labels.
