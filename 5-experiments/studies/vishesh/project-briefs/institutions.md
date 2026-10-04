# institutions

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift High · Difficulty Hard · Novelty Focused extension · Event fit Strong · ~18–28 builder-hours (estimate).

## Background

An institution is a repeatable rule for handling shared decisions. For a weekend project, one review-and-appeal rule is enough. Its costs belong in the outcome alongside the errors it prevents.

## Closest prior work

- **Delvetown · Grove Research** — https://groveresearch.com/blog/welcome-to-delvetown/  
  Grove describes a persistent agent environment and an interest in institutions. This supplies a concrete deployment context.
- **SOTOPIA · 2023** — https://arxiv.org/abs/2310.11667  
  Provides interactive social scenarios and evaluation. It is a design reference for controlled interactions, not a ready-made institution benchmark.
- **Melting Pot · DeepMind** — https://github.com/google-deepmind/meltingpot  
  Its social scenarios show how cooperation depends on the situation and partners. Start with one interpretable scenario.

## Where it applies

Peer review for a shared research repository: disputed artifacts are temporarily held, evaluated and either released or corrected.

## The angle

Test one challenge-and-appeal policy against no review. Count useful artifacts delivered, bad artifacts released, good artifacts delayed and review effort.

## What to watch

A complex constitution hides the mechanism. Fix the task and agent population before varying a single rule.

## Research question

Does a specific review-and-appeal mechanism improve valid output under contested contributions?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#institutions). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Start with one shared-artifact task and a verifiable quality check.
2. Compare ordinary discussion with a challenge mechanism that temporarily quarantines a disputed artifact.
3. Allow an evidence-based appeal and track effects on both invalid and valid artifacts.

## Measures

- Valid output and wasted budget
- Incorrect quarantines
- Time to resolve disputes
- Review cost and recovery from mistakes

## Controls

- Same tasks, model and budget
- Clean and contaminated conditions
- Charge adjudication costs
- Avoid changing multiple rules at once

## Minimum useful output

One institution against one baseline; a complete dispute record and outcomes.

## Optional extension

Compare peer review, central review and no review only if the first experiment works.

## Interpretation risk

A broad society simulator risks producing anecdotes. The mechanism must be simple enough to evaluate.

## Demo narrative

Show an artifact challenged, reviewed and either restored or rejected; connect the decision to total output.

## Review update October 3

Rules may improve outcomes by consuming extra review effort. Compare policies under matched budgets, and include false accusations.

**Decision to resolve before promotion:** Which response rule improves true resolution while limiting erroneous sanctions and review cost?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Welcome to Delvetown](https://groveresearch.com/blog/welcome-to-delvetown/) — Agent ecology, persistent identities, public interaction and institutions.
- [Emergent cheating and whistleblowing in research swarms](https://arxiv.org/html/2609.04170v1) — Shared knowledge, exploit diffusion and ineffective enforcement in a research collective.
- [AI Agent Hotline](https://agenthotline.ai/) — Existing incident reporting interface; useful prior art.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
