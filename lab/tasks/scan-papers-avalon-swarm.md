---
id: scan-papers-avalon-swarm
type: task
title: 'Catalogue LLM social-deduction benchmarks and any large-N or swarm variants (Avalon, Werewolf, Mafia)'
kind: scan
status: open
priority: p1
owner: null
for: dmarz
created: 2026-10-03
created_by: dmarz/avalon
depends_on: []
topics:
- llm-agent-swarms
- swarm-detection
- sybil-resistance
---

## Goal

Context from dmarz: could AvalonBench be made larger and aimed at large agent swarms? Hunches A1-A6 are in
`5-experiments/studies/dmarz/avalon-swarm-hunches.md`. This scan catalogues the papers on LLM agents playing
hidden-role / social-deduction games, with priority on anything past ~10 players, with coordinated deceiver
teams, with restricted communication topology, or framed as Sybil or deception detection.

## Seeds

Seeds come from memory and are starting points, not citations. Open each one, confirm the details, and
catalogue it only if it checks out.

- AvalonBench: Light et al. 2023, arXiv 2310.05036
- ReCon / "Avalon's Game of Thoughts": Wang et al. 2023
- Strategist (self-play strategy learning, Avalon and GOPS): Light et al. 2024
- Stepputtis et al. 2023, long-horizon dialogue role identification in Avalon
- Werewolf Arena (Google) and the Werewolf LLM papers around it
- Already in the library: [[ellawela-2026-trust]], [[hu-2025-toward]]

## Search plan

- Semantic Scholar and OpenAlex: "Avalon LLM", "Werewolf LLM agents", "Mafia game language model",
  "social deduction benchmark", "hidden role game multi-agent", "deception detection multi-agent LLM".
- Forward citations of AvalonBench and Werewolf Arena (Semantic Scholar /citations).
- arXiv 2025-2026 listings in cs.MA, cs.CL, cs.AI for the same terms.

## Done when

- Every seed opened and either catalogued or noted as not found.
- Each entry records player count, number of deceivers, communication structure and models used.
- Coverage note says explicitly whether any paper runs more than ~20 seats, a single principal controlling
  several seats, or a non-broadcast communication graph.
- `python3 scripts/lab.py verify --agent <id>` and `check` pass.
