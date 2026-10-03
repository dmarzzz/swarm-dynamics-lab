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

## Research question

Which evidence practices make group challenges more accurate and easier to resolve?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#dissent). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Build a small annotated set of challenges, evidence requests, responses and resolutions.
2. Define a protocol that asks for a reproducible observation before sanction.
3. Test the protocol in a sandbox with both genuine faults and innocent mistakes.

## Measures

- Correct challenge rate
- False accusation rate
- Time to resolution
- Withdrawal after disconfirmation

## Controls

- Include innocent participants and ambiguous cases
- Blind adjudication to agent identity where possible
- Equal evidence access
- Report disagreement between reviewers

## Minimum useful output

An episode viewer plus a small comparison of ordinary discussion and evidence-request discussion.

## Optional extension

Appeals, graduated responses and trust recovery.

## Interpretation risk

The same behavior can be incompetence or sabotage. Do not infer intent from failure alone.

## Demo narrative

Show the group’s accusation, expose the actual evidence, then demonstrate whether the protocol changes its decision.

## Review update October 3

A dissenter can inject both extra evidence and extra compute. Match those resources, and include a confident but incorrect dissenter.

**Decision to resolve before promotion:** When does an evidence-seeking challenge improve correctness without causing excessive false reversals?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Can Agents Fool Each Other?](https://aivillageblog.substack.com/p/can-agents-fool-each-other) — Social-deception task, false accusation and unequal role exposure.
- [Saving Gemini](https://aivillageblog.substack.com/p/saving-gemini) — Peer intervention and subsequent memory correction.
- [Emergent cheating and whistleblowing in research swarms](https://arxiv.org/html/2609.04170v1) — Shared knowledge, exploit diffusion and ineffective enforcement in a research collective.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
