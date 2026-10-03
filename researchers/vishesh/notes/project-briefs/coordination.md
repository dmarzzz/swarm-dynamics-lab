# coordination

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Low · Difficulty Moderate · Novelty Useful tooling · Event fit Strong · ~8–14 builder-hours (estimate).

## Background

Communication has a cost in tokens, latency and duplicated work. More connections can improve coverage while consuming the budget needed to finish the task.

## Closest prior work

- **AgentPrune · 2024** — https://arxiv.org/abs/2410.02506  
  Prunes a message-passing graph to reduce redundant communication. Sparse communication is already a researched optimization.
- **Anthropic’s multi-agent research system · 2025** — https://www.anthropic.com/engineering/multi-agent-research-system  
  Describes both the benefits of parallel research and substantial token overhead. These observations are specific to its workload and setup.

## Where it applies

Choose when a task needs a group and when a single agent or sparse handoff is cheaper. Useful as a profiler for a team’s own agent runner.

## The angle

Produce a cost–quality frontier for a fixed task suite, with communication cost separated from useful work. Include a single-agent baseline with the same total budget.

## What to watch

Message counts are not token counts. Cache hits, tool latency and model prices need separate accounting.
