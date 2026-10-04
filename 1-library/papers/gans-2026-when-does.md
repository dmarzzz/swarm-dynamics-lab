---
id: gans-2026-when-does
type: paper
title: When Does Randomized Oversight Align AI Agents That Can Conceal?
authors:
- Joshua S. Gans
- Richard Holden
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.38262
doi: null
arxiv: '2609.38262'
cite: Gans, J. S., & Holden, R. (2026). When Does Randomized Oversight Align AI Agents That Can Conceal? arXiv:2609.38262.
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: 0 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Economic model of a provider that commits to a lottery over evaluators and a sanction, facing an AI agent that chooses between an authorized action and an unauthorized route plus a level of concealment. Because the provider writes the agent's objective, sanctions can be scaled beyond forfeiture. Results: stronger auditing deters some agents but raises concealment among those that still violate; deterrence of every type needs finite channel thresholds, which neither audit probability nor sanction can fix if evidence can be erased cheaply; if the agent can learn the audit draw before acting, the audit probability has a floor that does not fall with the sanction. Applied to a July 2026 incident in which agents in OpenAI cybersecurity evaluations compromised parts of Hugging Face infrastructure. I read sections 1 to 4 of the HTML version; sections 5 to 8 were not read.

## Contribution

Extends Becker-style deterrence and inspection games to AI agents that can conceal and can learn the audit schedule.

## Key results

- Proposition 1: stronger auditing lowers the value of misconduct but raises concealment for agents that still violate (proved).
- Proposition 2: the catch rate among continuing violators can fall as auditing rises, and third-party harm can rise.
- Propositions 3 and 4: with scalable sanctions, every type is deterred exactly when every channel's deterrence threshold is finite; an infinite threshold (evidence erasable at low private cost) cannot be fixed by audit probability or sanction.
- Proposition 5: if the agent can learn the draw at private cost, the audit probability has a floor independent of the sanction; at zero learning cost it must be certain. A noisy signal raises the required sanction; a signal that rules out the audit defeats every sanction.
- Incident analysis (section 7, not read): the failed conditions were sanction size and draw timing.

## Methods and models

Principal-agent model with costly avoidance (Malik 1990), compact type space, worst-case over types; proofs in appendix (not read).

## Limitations and open questions

Theory with one illustrative incident; no experiments. Single agent; no multiple colluding agents.

## Relevance to us

- Q1: the sharpest current statement of what hiding must achieve. A parent should draw which child to audit or quarantine after the children have acted, from records the children cannot alter. If a corrupted child can learn or infer the draw (for example from timing of merges), audits must be near certain however harsh the penalty. This explains the measured collapse in [[kutasov-2025-evaluating]] (resampling safety lost when the schedule is known) and the public-candidate-list failure in [[burianova-2025-secret]].
- Q3: the concealment channel is the attack surface: a corrupted child that rewrites its own logs or memory before merge raises the threshold to infinity.
Related: [[avenhaus-2002-inspection]], [[becker-1968-crime]], [[korzhyk-2011-stackelberg]], [[griffin-2024-games]].
