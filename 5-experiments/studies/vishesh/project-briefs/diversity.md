# diversity

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Hard · Novelty Focused extension · Event fit Strong · ~14–24 builder-hours (estimate).

## Background

Diversity is useful when it changes failure correlation or task coverage. Different role names do not guarantee different errors. Measure disagreement before discussion and determine whether it survives communication.

## Closest prior work

- **Demystifying Multi-Agent Debate · 2026** — https://arxiv.org/abs/2601.19921  
  Studies confidence and diversity in debate and notes that ordinary debate can underperform voting. It gives a reason to test independent aggregation first.
- **Persona Inconstancy · 2024** — https://arxiv.org/abs/2405.03862  
  Examines conformity, confabulation and impersonation in persona-based collaboration. Prompted identities should not be treated as stable biological species.

## Where it applies

Choose a mixture of models, prompts or retrieval sources that remains useful when one component has a systematic blind spot.

## The angle

Cross an explicit shared blind spot with measured pre-discussion error correlation. Match total spend and include a homogeneous ensemble with independent samples.

## What to watch

Model diversity changes capability and price too. A result cannot be attributed to diversity if those differences explain it.

## Research question

Does heterogeneity improve error detection and recovery under comparable resource budgets?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#diversity). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Choose one objectively scored collaborative task and a reproducible misleading artifact.
2. Compare homogeneous groups with groups mixing models or reasoning roles.
3. Measure both clean-task performance and resilience to the same introduced error.

## Measures

- Group accuracy and time to correction
- Pairwise error correlation
- Cost per correct solution
- Dissent that changes the final answer

## Controls

- Include best-single-model and homogeneous strong-model baselines
- Report both equal-token and approximate equal-cost comparisons if possible
- Rotate roles and initial evidence
- Use repeated task seeds

## Minimum useful output

Two population compositions and one perturbation. Separate capability gains from resilience gains.

## Optional extension

Explore whether strategic diversity within one model gives similar benefits at lower cost.

## Interpretation risk

A mixed group may win because it contains one better model. Small samples do not establish biodiversity-like laws.

## Demo narrative

Show the same error passing unchallenged in one community and being challenged in another; then show aggregate outcomes.

## Review update October 3

Separate diversity of information from diversity of models. Include calibrated-confidence debate as related work rather than treating confidence as an unexplored variable. [Confidence and diversity paper](https://arxiv.org/abs/2601.19921)

**Decision to resolve before promotion:** Does measured error decorrelation predict robustness after accounting for capability and cost?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [AI Village Reacts to HuggingFace Incident](https://aivillageblog.substack.com/p/ai-village-reacts-to-huggingface) — Leadership, goal drift, externalized memory, diversity and coordination questions.
- [Welcome to Delvetown](https://groveresearch.com/blog/welcome-to-delvetown/) — Agent ecology, persistent identities, public interaction and institutions.
- [Can Agents Fool Each Other?](https://aivillageblog.substack.com/p/can-agents-fool-each-other) — Social-deception task, false accusation and unequal role exposure.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
