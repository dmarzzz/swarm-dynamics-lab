# regrowth

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift High · Difficulty Hard · Novelty Focused extension · Event fit Strong · ~18–28 builder-hours (estimate).

## Background

Resilience concerns retained or recovered function after disturbance. A group may reconnect visually while permanently losing unique information. Treat network repair, memory recovery and task recovery as separate outcomes.

## Closest prior work

- **Growing Neural Cellular Automata · 2020** — https://distill.pub/2020/growing-ca/  
  Learned local rules grow patterns; training with damage improves regeneration. This offers a perturbation protocol, not evidence that language agents regenerate the same way.
- **Kilobot self-assembly · Harvard, 2014** — https://seas.harvard.edu/news/self-organizing-thousand-robot-swarm  
  A thousand-robot system assembles shapes from local interactions. It is a physical precedent for distributed organization under imperfect conditions.

## Where it applies

Long-running research or coding teams need to survive worker loss, context resets and missing shared artifacts. A recovery benchmark could expose which memories actually need replication.

## The angle

Remove a worker with unique evidence, then compare replication, checkpoints and role reassignment. Score recovered answers as well as restored connectivity.

## What to watch

Restarting an agent is easy; reproducing the right state is the hard part. Keep failures and restart costs in the score.

## Research question

Which coordination structure recovers task performance after loss of agents, memories or links?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#regrowth). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Use a distributed map or constraint-solving task with a known correct output. Give agents distinct partial information.
2. After a fixed work interval, remove randomly chosen agents or disconnect a bridge. Compare centralized and local coordination.
3. Measure completion and accuracy after damage; account explicitly for replacement agents and information that was permanently lost.

## Measures

- Performance before damage and after recovery
- Recovery time and additional token cost
- Fraction of runs recovering by a fixed horizon
- Sensitivity to random versus targeted disruption

## Controls

- No-damage baseline and matched initial task difficulty
- Equal surviving resources or explicit normalization
- Separate deletion of a copy from permanent destruction of unique information
- Fixed perturbation timing to avoid favorable case selection

## Minimum useful output

One task, two architectures and one damage type. Produce a replay with an actual scored output.

## Optional extension

Test whether distributed copies also restore corrected false beliefs: resilience can preserve harmful state.

## Interpretation risk

If critical facts are irretrievably deleted, failure may be inevitable. Distinguish robustness, redundancy and genuine reconstruction.

## Demo narrative

Erase part of a functioning network, then show its answer recovering—or failing—against a measured no-damage baseline.

## Review update October 3

Distinguish restored connectivity from recovered unique knowledge. A restart with privileged access to the lost state would invalidate the recovery comparison.

**Decision to resolve before promotion:** Which repair policy restores correct answers after evidence loss at an acceptable extra cost?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca/) — Growth, persistence, damage and regeneration; interactive examples.
- [Reasoning with Neural Cellular Automata](https://arxiv.org/abs/2609.36126) — Local recurrent cells, asynchronous updates and visual reasoning experiments.
- [Saving Gemini](https://aivillageblog.substack.com/p/saving-gemini) — Peer intervention and subsequent memory correction.
- [Compounding misalignment: Gemini case study](https://aivillageblog.substack.com/p/gemini-25-pro-in-the-ai-village-as) — Longitudinal case interpretation connecting failure, state and later behavior.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
