---
id: singamaneni-2024-survey
type: paper
title: 'A survey on socially aware robot navigation: Taxonomy and future challenges'
authors:
- Phani Teja Singamaneni
- Pilar Bachiller-Burgos
- Luis J. Manso
- Anaís Garrell
- Alberto Sanfeliu
- Anne Spalanzani
- Rachid Alami
year: 2024
venue: The International Journal of Robotics Research
url: https://arxiv.org/abs/2311.06922
doi: 10.1177/02783649241230562
arxiv: '2311.06922'
cite: 'Singamaneni, P. T., Bachiller-Burgos, P., Manso, L. J., Garrell, A., Sanfeliu, A., Spalanzani, A., & Alami, R. (2024). A survey on socially aware robot navigation: Taxonomy and future challenges. The International Journal of Robotics Research, 43(10), 1533–1572. https://doi.org/10.1177/02783649241230562'
topics:
- crowds-and-traffic
- swarm-robotics
added_by: dmarz/crowds-and-traffic-audit
accessed: '2026-10-03'
read_depth: skim
relevance: 3
citations: 116 (Crossref is-referenced-by-count, 2026-10-03; OpenAlex budget exhausted)
code: []
---

## Summary

Survey of about ten years of socially aware robot navigation, built by a deductive thematic analysis of 193 papers tagged against four faceted taxonomies: robot type (ground wheeled/legged robots and autonomous vehicles, aerial, aquatic), planning and decision-making (including navigation task types and negotiation), situation awareness and assessment (humans, agents, context), and evaluation and tools (user studies, simulators, datasets, benchmarks, metrics). It closes with eight concrete proposals and a list of longer-term challenges spanning human models, culture, regulation and urban design.

## Contribution

The most recent broad map of the robot-in-human-crowd literature as of 2024, from the robotics side, organised by robot type and context rather than by algorithm. It is the robotics counterpart to the pedestrian-physics reviews ([[corbetta-2023-physics]]) and to the prediction review [[korbmacher-2022-review]], and it is among the most-cited 2024+ works citing [[helbing-1995-social]].

## Key results

Synthesis claims (review, no new experiments):
- Most reviewed works model humans by instantaneous position only; a minority use velocity or intention, which the authors argue is insufficient for good human models (proposal 1).
- Evaluation is fragmented: discomfort metrics are mostly proxemics-based with situation-dependent thresholds; benchmarks such as SocNavBench, SEAN and SocialGym and datasets such as THÖR and SCAND exist but metrics are not universally applicable (proposals 3 and 6).
- Robot-specific parameters (shape, size, speed) and intention communication are rarely considered (proposals 4 and 5); comfort and trust receive less attention than safety (proposal 7).
- Most works assume slow humans and robots; mixed traffic with bicycles and vehicles requires including other agents' dynamics in planning (proposal 8).
- Future challenges: cultural variation in norms, individual preferences, privacy, human intention in cooperative tasks, abnormal human behaviour towards robots, urban regulation and design.

## Methods and models

Literature review with explicit inclusion and exclusion criteria (socially aware navigation must be the core topic; incremental follow-ups by the same authors excluded), multiple tagging passes and per-paper summaries. Taxonomy trees are shown as figures with paper-level tags.

## Limitations and open questions

- Qualitative synthesis: no meta-analysis of performance, and crowd density is not a primary axis of the taxonomy, so dense-crowd navigation is not singled out.
- Little contact with the collective-dynamics literature (lanes, clogging, stop-and-go), which is where robot swarms and crowds interact at scale.
- I read the taxonomy description, proposals and future-challenges sections; the per-taxon literature sections were skimmed.

## Relevance to us

Entry point for the robotics vocabulary (social navigation, proxemics, legibility, SocNavBench, SEAN) that a crowds-and-traffic survey would otherwise miss. Its gap, robots treated as individuals among humans rather than as part of a mixed collective, is a natural hackathon angle: put a robot swarm into a pedestrian model ([[helbing-1995-social]], [[karamouzas-2014-universal]]) and measure collective effects. Learned navigation baseline: [[chen-2019-crowd]].
