# quorum

Status: HUNCH, not a hypothesis; no survey has passed the gate. Author's own triage, not a team ranking: Lift Low · Difficulty Moderate · Novelty Focused extension · Event fit Strong · ~6–12 builder-hours (estimate).

## Background

Quorum rules turn accumulated signals into a group commitment. Bacterial signaling and ant nest choice show different versions of threshold coordination. Counting agreeing agents is much simpler than checking whether their evidence is independent.

## Closest prior work

- **Cooperation and conflict in quorum-sensing bacteria · 2007** — https://www.nature.com/articles/nature06279  
  Signaling and response can be exploited by noncooperators. A threshold is a mechanism with incentives, not an automatic guarantee of reliable action.
- **Speed versus accuracy in decision-making ants · 2009** — https://pmc.ncbi.nlm.nih.gov/articles/PMC2689711/  
  Nest-choice experiments examine speed–accuracy trade-offs. This supplies a useful two-axis evaluation: how fast the group commits and how often it is right.

## Where it applies

Agent approvals, incident escalation and automated fact-checking. An evidence-aware quorum could prevent five copies of one rumor from looking like five confirmations.

## The angle

Compare votes with unique verified evidence identifiers. Sweep the commitment threshold and plot false commits against delay.

## What to watch

Unique identifiers are not enough if several documents share the same upstream source. Include that case in the test.

## Research question

How does adoption change with repeated messages, distinct messengers and genuinely independent evidence?

## Dossier design sketch

Carried over from the [interactive dossier](../swarm-ecology-dossier.html#quorum). This is an unexecuted hunch, not an approved experiment. Counts and treatments below are planning choices; the lab’s survey and hypothesis review gates still apply.

1. Provide an agent an initial evidence packet and a choice with known ground truth.
2. Compare one source repeated five times, five agents repeating one source, and five independent observations.
3. Vary exposure count and evidence reliability. Record decisions before and after receiving messages.

## Measures

- Correct and incorrect adoption probability
- Sensitivity to independent versus repeated evidence
- Confidence calibration where elicited
- Reversal after a credible correction

## Controls

- Match total text length and message order distributions
- Declare which observations share a source
- Use both true and false target claims
- Compare with an evidence-counting baseline

## Minimum useful output

Three message conditions, a small set of generated problems, repeated trials and adoption curves.

## Optional extension

Place tested agents in a network to examine whether individual thresholds predict group cascades.

## Interpretation risk

A programmed threshold only demonstrates the rule you wrote. Let the model decide, and estimate its response from observations.

## Demo narrative

Present three visually identical crowds. Reveal that only one contains independent evidence, then compare decisions.

## Review update October 3

A document identifier is not an independence guarantee. Include several documents derived from one upstream observation and distinguish an oracle provenance label from an inferred one. Reuse the hidden-profile discussion in the background digest. [[tambwekar-2026-proxifield]]

**Decision to resolve before promotion:** Does an evidence-aware commit rule reduce false commits at a matched delay or review budget?

If the simple baseline explains the result, or the necessary evidence cannot be obtained, narrow this to a replication or park the hunch. A toy animation is not evidence that the proposed intervention works.

## Additional dossier sources

- [Cooperation and conflict in quorum-sensing bacteria](https://www.nature.com/articles/nature06279) — Communication, cooperative behavior and exploitation.
- [Quorum sensing protects cooperation from cheats](https://www.nature.com/articles/ismej2015232) — Population composition and signaling influence cooperative investment.
- [Persuasion in the AI Village](https://aivillageblog.substack.com/p/persuasion-in-the-ai-village-deepseek) — Consensus, inventive theories, metric pursuit and corrections.
- [Mayalen Etcheverry: original NCA thread](https://x.com/mayalen_etc/status/2105701039148323258) — Author explanation of local communication and visual reasoning.

[All project briefs](README.md) · [Research updates](../background-readings-2026-10-03.md)
