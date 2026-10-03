# dissent

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Low · Difficulty Moderate · Novelty Focused extension · Event fit Strong · ~8–14 builder-hours (estimate).

## Background

A dissenter is useful when it brings checkable counterevidence. Mandatory disagreement can create noise or persuade a correct majority to switch to a wrong answer.

## Closest prior work

- **Multiagent Debate · Du et al., 2023** — https://arxiv.org/abs/2305.14325  
  Reports benefits from iterative exchange on tested reasoning tasks. This is a baseline, not a guarantee for every debate protocol.
- **Demystifying Multi-Agent Debate · 2026** — https://arxiv.org/abs/2601.19921  
  Examines confidence and diversity as conditions for debate. A useful test keeps a majority-vote baseline and studies wrong consensus.

## Where it applies

A bounded review step for agent-generated analyses: spend extra computation only where a critic can cite a contradiction.

## The angle

Compare no critic, generic critic and evidence-constrained critic. Separate corrections of wrong answers from damage to right answers.

## What to watch

An always-disagree prompt can manufacture disagreement. Give critics the same evidence access and charge their tokens to the budget.
