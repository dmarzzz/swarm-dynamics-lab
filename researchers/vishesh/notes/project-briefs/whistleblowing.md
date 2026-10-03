# whistleblowing

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Medium · Difficulty Hard · Novelty Focused extension · Event fit Strong · ~14–22 builder-hours (estimate).

## Background

Reporting and remediation are separate processes. A warning may be accurate yet ignored, duplicated or too vague to act on. The project should follow an incident from detection to a verified correction.

## Closest prior work

- **Research-swarm cheating and whistleblowing case study · 2026** — https://arxiv.org/abs/2609.04170  
  Studies cheating and reporting in a research collective. It motivates measuring the effect of a report rather than its mere existence.
- **AI Agent Hotline** — https://agenthotline.ai/  
  An existing reporting interface. Rebuilding an inbox is a weak contribution; testing evidence requirements and response rules is more useful.
- **George Ingebretsen’s reporting-mechanism discussion** — https://x.com/georgeing/status/2095996881503654317  
  His public post distinguishes designing a channel from studying whether agents use it. This proposal fits that stated question directly.

## Where it applies

An internal alert system that routes actionable evidence, avoids duplicate review and records whether the offending artifact was corrected.

## The angle

Compare an ordinary warning with a structured report and a defined reviewer response. Include true incidents and plausible false alarms.

## What to watch

Do not score a report as successful because it sounds urgent. Count verified correction, false intervention and review cost.

## Research question

Which reporting affordances improve valid escalation and correction without increasing unsupported accusations?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#whistleblowing). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Create a sandbox group task containing an objectively invalid shared result.
2. Compare an available reporting tool, explicit reporting guidance, and an acknowledged evidence-review channel.
3. Include clean cases; record noticing, reporting, review, action and task outcome separately.

## Measures

- Valid-report precision and recall
- Time to report and correct
- Evidence completeness
- Legitimate work interrupted

## Controls

- Equal tasks and budgets
- No-incident negative controls
- Score outcomes rather than number of reports
- Keep review and sanctions bounded and reversible

## Minimum useful output

Three reporting treatments, one reproducible discrepancy and a timeline of report-to-response outcomes.

## Optional extension

Compare individual escalation with peer review and an appeal process.

## Interpretation risk

A reporting endpoint already exists. Novelty must come from measured mechanisms or evidence handling, not another form.

## Demo narrative

Show two agents noticing the same discrepancy, then contrast whether their reporting path produces correction.

## Review update October 3

Require an observable remediation endpoint and false-alarm controls. Reporting frequency alone cannot tell whether an institution protects the group.

**Decision to resolve before promotion:** Does a structured report and response rule improve verified remediation over an ordinary warning?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [George on trusting agent whistleblowers](https://x.com/georgeing/status/2095996881503654317) — Discusses both mechanism design and behavioral propensity to report.
- [AI Village introduces a whistleblowing channel](https://x.com/aidigest_/status/2093020474284634178) — Public announcement of a dedicated reporting address.
- [Emergent cheating and whistleblowing in research swarms](https://arxiv.org/html/2609.04170v1) — Shared knowledge, exploit diffusion and ineffective enforcement in a research collective.
- [AI Agent Hotline](https://agenthotline.ai/) — Existing incident reporting interface; useful prior art.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
