---
id: strobel-2026-how
type: paper
title: "How foundation models will revolutionize robot swarms"
authors: ["Volker Strobel", "Marco Dorigo", "Mario Fritz"]
year: 2026
venue: "Science Robotics"
url: https://doi.org/10.1126/scirobotics.adz1543
doi: "10.1126/scirobotics.adz1543"
arxiv: null
cite: "Strobel, V., Dorigo, M., & Fritz, M. (2026). How foundation models will revolutionize robot swarms. Science Robotics, 11(113), eadz1543. https://doi.org/10.1126/scirobotics.adz1543"
topics: [swarm-robotics, llm-agent-swarms]
added_by: dmarz/swarm-robotics-recent-audit
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "0 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex search budget exhausted during this audit)"
code: []
---

## Summary

A Science Robotics perspective arguing that foundation models running on board could change how robot swarms are built and run. Today, swarm controllers are hand-coded before the mission, which is slow and rigid. The authors sketch two complementary roles for foundation models: as swarm designers that synthesise robot controllers and do high-level planning, and as swarm operators that mediate robot-robot collaboration and human-swarm interaction.

## Contribution

An agenda-setting viewpoint from the authors of LLM2Swarm ([[strobel-2024-llm2swarm]]) and one of the founders of swarm robotics. It frames the LLM-swarm literature ([[ji-2026-genswarm]], [[rahman-2025-llm-powered]], [[schuck-2025-swarmgpt]]) as two design patterns: FM-as-designer and FM-as-operator.

## Key results

- No experimental results; this is a perspective. Claims (per the abstract): on-board FMs can reduce controller development effort and add flexibility, via the two roles above.

## Methods and models

Perspective/opinion article. Read only through the Europe PMC abstract record; the Science page was not accessible from this machine.

## Limitations and open questions

Abstract only. The obvious tension with classical swarm robotics, that swarms are supposed to be simple, cheap and decentralised while FMs are large and costly, is presumably discussed in the full text but not verified here. Robustness, latency and verification of FM-generated controllers remain open.

## Relevance to us

A citable framing for any hackathon project that puts an LLM in the loop of a swarm (designer vs operator). Sits next to [[strobel-2024-llm2swarm]], [[ji-2026-genswarm]] and [[dorigo-2021-swarm]].
