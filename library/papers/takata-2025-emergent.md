---
id: takata-2025-emergent
type: paper
title: "Emergent Social Dynamics of LLM Agents in the El Farol Bar Problem"
authors:
- "Ryosuke Takata"
- "Atsushi Masumori"
- "Takashi Ikegami"
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2509.04537
doi: null
arxiv: "2509.04537"
cite: "Takata, R., Masumori, A., & Ikegami, T. (2025). Emergent Social Dynamics of LLM Agents in the El Farol Bar Problem. arXiv preprint arXiv:2509.04537."
topics:
- llm-agent-swarms
- collective-decision
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "not retrieved (OpenAlex and Semantic Scholar both HTTP 429, 2026-10-03)"
code: []
---
## Summary

Puts LLM agents into a spatially extended version of Arthur's El Farol Bar problem, the minority-game ancestor in which agents decide whether to attend a bar that is only enjoyable below a capacity threshold (60% in the prompt). Agents move in space and communicate. According to the abstract, the agents developed a spontaneous motivation to go to the bar and changed their decision making as a collective, but did not solve the coordination problem completely and behaved more like humans than like game-theoretic optimisers. The authors read this as an interplay between prompt-specified external incentives and culturally encoded preferences from pre-training.

## Contribution

Brings a canonical complex-systems resource-allocation game (El Farol / minority game) to LLM agent populations, a bridge between econophysics and LLM swarms not covered by the naming-game or opinion-dynamics lines.

## Key results

- Claimed (abstract): spontaneous motivation to attend and collective shifts in decision making; incomplete solution of the coordination problem; human-like rather than game-theoretically rational behaviour.
- Search-result snippet (not verified in the paper): hashtags such as "#collaboration" spread within subgroups, read as emergent norms.

## Methods and models

Spatial El Farol setting with a 60% capacity threshold given in the prompt; LLM agents with movement and messaging. Model, population size and number of rounds not recorded at abstract depth.

## Limitations and open questions

- Abstract-level read; quantitative attendance statistics (fluctuations around capacity, the classical minority-game observable) not checked.
- Qualitative claims about "motivation" and "human-like" behaviour need operationalising.

## Relevance to us

Suggests a resource-competition benchmark for LLM swarms with a known classical baseline (attendance volatility vs strategy diversity in the minority game). Compare with [[ezaki-2026-warned]] (congestion game with GPT agents) and [[mori-2026-three]] (capacity game, tribes).
