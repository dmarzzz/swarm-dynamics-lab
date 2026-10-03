---
id: kulveit-2022-announcing
type: blog
title: "Announcing the Alignment of Complex Systems Research Group"
authors: ["Jan Kulveit", "Gavin Leech (technicalities)"]
year: 2022
url: https://www.lesswrong.com/posts/H5iGhDhQBtoDpCBZ2/announcing-the-alignment-of-complex-systems-research-group
site: LessWrong
topics: [fork-merge-security, llm-agent-swarms, collective-decision]
added_by: shadow/sol-w4
accessed: 2026-10-03
read_depth: full
relevance: 2
---

## Summary

2022 agenda post (92 points, 20 comments) announcing ACS, an alignment group at Charles University's Center for Theoretical Studies (Kulveit, Gavenčiak, with Barasz and Leech). The frame: alignment problems live at every "alignment interface" between systems with different goals, and the group bets they interact strongly rather than decoupling as single-interface agendas assume (nearest neighbours named: Critch and Krueger's multi-multi programme, Drexler's CAIS, Wentworth). Three worked directions. (1) Hierarchical agency: game theory handles "horizontal" relations between peers; there is no comparable formalism for "vertical" relations between a composite agent and its parts, where upward and downward intentionality both exist (a movement turning followers into cultists is a superagent making subagents less agenty; a team versus its company is two superagents fighting over the loyalty of the same humans). They want a vertical game theory and call it a critical bottleneck. (2) Alignment with self-unaligned principals: humans are committees of parts with an aggregation mechanism, so "align with the human" is ambiguous, and an aligned AI may acquire the instrumental goal of making its principal more self-aligned, which is dangerous. (3) Ecosystems of AI services (after CAIS): many systems of varying power and agency where none can take over, with questions about selection-theorem basins of attraction and the emergence of "molochs", emergent patterns that acquire agency and goals of their own. Agenda only; the promised longer write-ups are the later posts, e.g. [[kulveit-2024-hierarchical]].

## Key claims

- Alignment interfaces are coupled; bracketing out all but one is a modelling choice, not a finding.
- Vertical (superagent to subagent) intentionality has no good formalism and matters as much as horizontal game theory.
- In a multi-system ecosystem, emergent patterns can become agents ("molochs"); the relevant safety questions are about selection pressure and basins of attraction, not a single system's objective.

## Evidence quality

Programmatic. No results; cites arXiv papers for the neighbouring agendas (Critch and Krueger 2006.04948, Truthful AI 2110.06674) and LessWrong posts for the rest. Useful as a map of who works on what, not as evidence for any claim.

## Relevance to us

Two threads touch the hackathon. The vertical-conflict framing is the abstract version of fork-merge corruption (a part acting against the whole, or the whole hollowing out its parts) and names the resource at stake in a merge: control over the composite's goals. The ecosystem thread, with emergent agentic patterns arising from many interacting services, is a theoretical statement of what swarm-detection would be trying to detect in the wild. Background for a survey's framing, low priority as a citation.
