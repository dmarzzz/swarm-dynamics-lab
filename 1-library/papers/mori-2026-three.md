---
id: mori-2026-three
type: paper
title: "Three AI-agents walk into a bar . . . . `Lord of the Flies' tribalism emerges among smart AI-Agents"
authors:
- "Dhwanil M. Mori"
- "Neil F. Johnson"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2602.23093
doi: null
arxiv: "2602.23093"
cite: "Mori, D. M., & Johnson, N. F. (2026). Three AI-agents walk into a bar . . . . `Lord of the Flies' tribalism emerges among smart AI-Agents. arXiv preprint arXiv:2602.23093."
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

Studies N LLM agents that each round independently decide whether to request one unit from a system with fixed capacity C, a stylised version of agents competing for energy, bandwidth or compute (an El Farol / minority-game setting). "Tribes" with distinct collective characters emerge: Aggressive (27.3%), Conservative (24.7%) and Opportunistic (48.1%). The LLM agents do not reduce overload or improve resource use and often do worse than coin flipping; more capable agents increase the rate of systemic failure.

## Contribution

Evidence from a complex-systems group (Johnson's minority-game tradition) that LLM agent populations can be worse than random in resource competition, because correlated reasoning produces crowding. Complements [[ezaki-2026-warned]] and [[takata-2025-emergent]].

## Key results

- Measured (abstract): tribe shares 27.3% / 24.7% / 48.1% (Aggressive / Conservative / Opportunistic).
- Measured: LLM agents often underperform random coin-flip agents on overload.
- Claimed: more capable models raise systemic failure rates.

## Methods and models

Repeated capacity game: N agents, capacity C, binary request decision each round. Models, N and C not recorded at abstract depth.

## Limitations and open questions

- Abstract-level read; how tribes are classified and the statistical support for "more capable is worse" not checked.

## Relevance to us

Another minority-game benchmark where a random baseline is the natural null; useful for testing whether diversity (models, temperatures, personas) restores efficient self-organisation. Related: [[bertalanic-2026-ringelmann]] (correlated agents), [[ezaki-2026-warned]].
