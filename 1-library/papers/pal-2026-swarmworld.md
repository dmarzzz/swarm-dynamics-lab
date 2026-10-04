---
id: pal-2026-swarmworld
type: paper
title: "SwarmWorld: Stigmergic technological evolution in societies of language-model agents"
authors:
- "Subhadeep Pal"
- "Fiona Y. Wang"
- "Markus J. Buehler"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2608.26081
doi: null
arxiv: "2608.26081"
cite: "Pal, S., Wang, F. Y., & Buehler, M. J. (2026). SwarmWorld: Stigmergic technological evolution in societies of language-model agents. arXiv preprint arXiv:2608.26081."
topics:
- llm-agent-swarms
- swarm-intelligence
- collective-decision
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: "not retrieved (OpenAlex and Semantic Scholar both HTTP 429, 2026-10-03)"
code: []
---
## Summary

Initially identical LLM agents (50 to 200 per society, per a search snippet) live in a persistent, modifiable spatial world without assigned roles or recipes. They explore, process resources, test materials, build persistent artifacts and write executable controllers that a deterministic simulator evaluates under unseen disturbances after the agents are removed, so function is judged by the world rather than by the agents. Shared societies develop broader and more resilient technology portfolios than a strong best-of-N isolated-search baseline, though isolated search stays competitive for the single best artifact. Agents differentiate into exploration, construction, maintenance and coordination behaviours as the world matures, and most reuse starts from physical observation of artifacts rather than from messages.

## Contribution

A direct test of stigmergy (coordination through a shared environment rather than conversation) for LLM agents, with an external, deterministic evaluator that avoids LLM self-assessment. Sits between the classical stigmergy literature in swarm intelligence and conversation-centred LLM multi-agent systems ([[qian-2025-scaling]], [[li-2025-swarmsys]]).

## Key results

- Claimed (abstract): societies beat best-of-N isolated search on breadth and resilience of technology portfolios, not on the best single artifact.
- Claimed: role differentiation emerges and shifts over time; reuse begins mostly through observation.
- Claimed: explicit cultural mechanisms amplify collaboration, but functional benefits depend on outcome and timescale; physical stigmergy alone supports capable societies.

## Methods and models

Spatial simulation with fixed action and material schemas; agents propose architectures and controllers; a deterministic simulator scores them under disturbances. Models, exact population sizes and metrics not recorded at abstract depth.

## Limitations and open questions

- Abstract-level read; effect sizes and the best-of-N compute matching were not checked.
- Fixed schemas bound what "technology" can mean.

## Relevance to us

One of very few LLM-swarm papers where coordination is environmental (stigmergic), as in ant colonies and termite building. Suggests a hackathon contrast: message-passing swarm vs shared-artifact swarm at equal compute. Compare [[rodriguez-2026-emergent]] (pressure-field coordination on a shared artifact) and [[de-marzo-2026-copying]] (a wiki as an accidental stigmergic medium).

## Notes from vishesh/senku-1

Full read of v1; the entry above is abstract-depth. Five additions:

- Four arms isolate the channel: full culture, no messaging, no explicit culture (shared world only), independent search.
- Long-horizon (100 agents, 3,200 ticks): portfolio resilience 0.2474 / 0.2365 / 0.1794; validated inventions 5.75 / 7.00 / 2.75. Stigmergy alone wins on inventions, and isolated search keeps the best artifact (0.3488 against 0.2380).
- Diffusion: first reuse at 5 versus 8 ticks, adoption breadth 13.53 versus 7.49 agents, about 95% of first reuse through observation.
- Removing half the agents at random leaves 98.3% of artifacts connected; removing high-degree agents leaves 59.6%.
- The model backend is never named. Four seeds per cell.
