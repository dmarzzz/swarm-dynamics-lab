---
id: park-2024-llm
type: paper
title: "LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals"
authors: ["Joon Sung Park", "Carolyn Q. Zou", "Jonne Kamphorst", "Niles Egan", "Aaron Shaw", "Benjamin Mako Hill", "Carrie Cai", "Meredith Ringel Morris", "Percy Liang", "Robb Willer", "Michael S. Bernstein"]
year: 2024
venue: "arXiv"
url: https://arxiv.org/abs/2411.10109
doi: null
arxiv: "2411.10109"
cite: "Park, J. S., Zou, C. Q., Kamphorst, J., Egan, N., Shaw, A., Hill, B. M., Cai, C., Morris, M. R., Liang, P., Willer, R., & Bernstein, M. S. (2024). LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals. arXiv preprint arXiv:2411.10109."
topics: [llm-agent-swarms]
added_by: dmarz/sim-envs
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: "321 (Semantic Scholar, 2026-10-03)"
code: [gh-stanfordhci-genagents]
---

## Summary

Earlier versions were titled 'Generative Agent Simulations of 1,000 People'. The authors build agents for 1,052 Americans from two-hour interviews, structured surveys, or both, and test them on held-out General Social Survey items, personality, economic games and experiments. Accuracy normalised by participants' own two-week test-retest consistency is 83% (interview), 82% (survey), 86% (both) versus 74% for demographics-only agents, with smaller accuracy gaps across racial and ideological groups.

## Contribution

Strongest evidence so far that grounding agents in individual self-report data, rather than demographic personas, makes LLM agents track specific people, and that demographic prompting is the weak baseline.

## Key results

- 1,052 participants; normalised accuracy 83% / 82% / 86% (interview / survey / combined) vs. 74% demographics-only (abstract).
- Gains from combining sources are modest, suggesting an asymptote (abstract).
- Reduced accuracy disparities across racial and ideological groups relative to demographics-only agents (abstract).

## Methods and models

Agents built from American Voices Project interview transcripts and/or GSS and Big Five survey responses; evaluated against participants' own retest consistency. Not read beyond the abstract.

## Limitations and open questions

Individual-level prediction, not interaction; no multi-agent dynamics. Interview agents are access-restricted.

## Relevance to us

Supports seeding swarm sims with grounded, heterogeneous personas rather than one-line demographic prompts; the open demographic bank in [[gh-stanfordhci-genagents]] is the 74% condition. Follows [[park-2023-generative]].
