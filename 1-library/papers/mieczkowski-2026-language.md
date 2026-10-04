---
id: mieczkowski-2026-language
type: paper
title: "Language Model Teams as Distributed Systems"
authors:
- "Elizabeth Mieczkowski"
- "Katherine M. Collins"
- "Ilia Sucholutsky"
- "Natalia Vélez"
- "Thomas L. Griffiths"
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2603.12229
doi: null
arxiv: "2603.12229"
cite: "Mieczkowski, E., Collins, K. M., Sucholutsky, I., Vélez, N., & Griffiths, T. L. (2026). Language Model Teams as Distributed Systems. arXiv preprint arXiv:2603.12229."
topics:
- llm-agent-swarms
added_by: dmarz/llm-agent-swarms-recent-audit
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: "not retrieved (OpenAlex and Semantic Scholar both HTTP 429, 2026-10-03)"
code: []
---
## Summary

Position-and-evidence paper arguing that questions about LLM teams (when is a team helpful, how many agents, how should it be structured, does it beat one agent) should be answered with distributed-systems theory instead of trial and error. The authors report that many fundamental advantages and challenges of distributed computing also appear in LLM teams.

## Contribution

Supplies a neighbouring-field vocabulary (distributed computing) for LLM swarm scaling, alongside the statistical-physics framing ([[jiang-2026-large]], [[de-wynter-2026-population]]) and the scaling-science framing ([[kim-2025-towards]], [[fan-2026-towards]]).

## Key results

- Claimed (abstract): distributed-systems advantages and failure modes recur in LLM teams.

## Methods and models

Not recorded at abstract depth.

## Limitations and open questions

- Abstract-level read; which distributed-systems laws (Amdahl-type limits, consensus impossibility, straggler effects) were tested quantitatively is not checked.

## Relevance to us

A framing source for the survey: maps team size and topology questions onto known distributed-computing results. Related: [[grotschla-2025-agentsnet]] (distributed-computing tasks for LLM agents), [[kuznetsov-2026-width]].
