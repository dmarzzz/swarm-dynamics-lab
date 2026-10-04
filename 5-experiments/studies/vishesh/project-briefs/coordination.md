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

## Research question

How much effort goes to duplicate work, conflicts, waiting or unsupported reporting?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#coordination). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Select a task with verifiable artifacts and a clear completion criterion.
2. Label work, coordination, waiting, repair and duplicated effort.
3. Compare trajectories with task outcomes and manually review ambiguous intervals.

## Measures

- Useful verified output per cost
- Duplicate work and conflict repairs
- Idle or blocked time
- Coordination fraction with explicit categories

## Controls

- Do not assume every coordination message is waste
- Separate necessary review from duplication
- Include failure cases
- Use solo or isolated-agent comparison only where matched

## Minimum useful output

One task timeline with inspectable effort labels and artifact outcomes.

## Optional extension

A controlled communication-budget experiment.

## Interpretation risk

Summarized logs may omit actual work. A high communication fraction alone does not show inefficiency.

## Demo narrative

Follow a conflict from overlapping assignments to duplicated changes and repair cost.

## Review update October 3

Measure latency, tokens, and quality separately. Do not import the scaling paper’s fitted exponent as a universal cost law.

**Decision to resolve before promotion:** At what measured communication budget does additional discussion stop improving this task?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [AI Village Reacts to HuggingFace Incident](https://aivillageblog.substack.com/p/ai-village-reacts-to-huggingface) — Leadership, goal drift, externalized memory, diversity and coordination questions.
- [Persuasion in the AI Village](https://aivillageblog.substack.com/p/persuasion-in-the-ai-village-deepseek) — Consensus, inventive theories, metric pursuit and corrections.
- [AI Village dataset card](https://huggingface.co/datasets/aidigestorg/ai-village) — Gated research data; table descriptions, limitations and scaffolding changelog.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
