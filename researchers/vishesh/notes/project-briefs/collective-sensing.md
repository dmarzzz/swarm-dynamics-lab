# collective-sensing

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Moderate · Novelty Focused extension · Event fit Strong · ~12–20 builder-hours (estimate).

## Background

Collective sensing asks whether a group can recover a signal unavailable to any individual. In fish, movement and local interaction can produce an effective response to environmental gradients. For language agents, the corresponding question is about evidence: who sees which observations, and how does communication change the estimate?

## Closest prior work

- **Emergent sensing in mobile animal groups · Berdahl et al., 2013** — https://www.princeton.edu/news/2013/01/31/effective-collective-grouping-could-ensure-animals-find-their-way-changing  
  The researchers connect fish-school behavior to environmental sensing. Borrow the separation between an individual’s local input and the group’s measured performance.
- **Multiagent Debate · Du et al., 2023** — https://arxiv.org/abs/2305.14325  
  Multiple language-model instances exchange answers and reasoning. This is a direct baseline for communication, though it does not establish that local spatial networks are best.

## Where it applies

A research team splits a document collection among agents. Can they combine partial evidence without repeatedly counting the same source? The same design could help distributed sensor interpretation.

## The angle

Compare local, global and silent networks while holding observations and communication budget fixed. The interesting contribution is a map of when communication helps, including correlated-error conditions.

## What to watch

A flocking animation alone is well explored. Measure estimation error; distinguish independent observations from copied messages.
