# casefile

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Moderate · Novelty Useful tooling · Event fit Strong · ~10–18 builder-hours (estimate).

## Background

An investigator needs to distinguish an observed event from an inferred relationship. A chronological view is helpful, but evidence quality and missing intervals matter more than the size of the graph.

## Closest prior work

- **SwarmTraces · 2026** — https://swarmtraces.org/  
  An existing reconstruction and explorer for public agent traces. A new generic graph would duplicate part of its value.
- **Why Do Multi-Agent LLM Systems Fail? · 2025** — https://arxiv.org/abs/2503.13657  
  Provides a failure taxonomy and annotated traces. It offers a starting vocabulary for case annotation, rather than proving causal explanations.

## Where it applies

Incident review, swarm-debugging reports and research audit trails. A reviewer should be able to inspect the evidence behind every disputed link.

## The angle

Add uncertainty labels, missing-data markers and side-by-side competing reconstructions. Measure whether another reader can reproduce an annotation.

## What to watch

Prefer one excellent case to a large unverified index. Preserve trace IDs and time zones; distinguish event time from collection time.
