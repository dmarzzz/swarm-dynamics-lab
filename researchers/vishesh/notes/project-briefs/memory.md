# memory

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Hard · Novelty Focused extension · Event fit Strong · ~12–22 builder-hours (estimate).

## Background

Persistent memory can keep a useful fact or repeatedly reintroduce a bad one. A correction has to reach the record that future retrieval actually uses. Deletion, annotation and replacement have different failure modes.

## Closest prior work

- **AgentPoison · 2024** — https://arxiv.org/abs/2407.12784  
  Shows that poisoned memory or retrieved knowledge can redirect agent behavior. It establishes a concrete memory-integrity problem.
- **LongMemEval · 2024** — https://arxiv.org/abs/2410.10813  
  Evaluates memory abilities including knowledge updates and abstention. It provides task-design ideas for testing whether a correction sticks.
- **Generative Agents · 2023** — https://arxiv.org/abs/2304.03442  
  Uses stored experiences, retrieval and reflection. A correction may need to address a derived reflection as well as the original note.

## Where it applies

Repair stale project assumptions, revoked instructions and incorrect research notes without erasing useful history.

## The angle

After a verified correction, test recurrence across later retrievals. Track derived summaries and compare append-only correction with explicit supersession.

## What to watch

A safer-sounding response is not a memory repair. Check the retrieved records and behavior on held-out questions.
