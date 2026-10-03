---
id: mallen-2024-subversion
type: paper
title: 'Subversion Strategy Eval: Can language models statelessly strategize to subvert control protocols?'
authors: [Alex Mallen, Charlie Griffin, Misha Wagner, Alessandro Abate, Buck Shlegeris]
year: 2024
venue: arXiv preprint
url: https://arxiv.org/html/2412.12480
doi: null
arxiv: '2412.12480'
cite: 'Mallen, A., Griffin, C., Wagner, M., Abate, A., & Shlegeris, B. (2024). Subversion Strategy Eval: Can language models statelessly strategize to subvert control protocols? arXiv:2412.12480.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: 14 (Semantic Scholar, 2026-10-03)
code: []  # implemented in Inspect-AI, released open-source
---

## Summary

An evaluation suite (eight environments, six affordance settings) that asks whether a model with no memory between calls can work out and execute a strategy to subvert a control protocol. Four sub-abilities are isolated: optimality in planning, reliability in planning (deriving the same plan in every context), probability calibration (attacking at the right rate, for example a backdoor rate tuned to an upfront-audit budget), and acausal coordination (separate instances choosing compatible strategies without communicating, such as agreeing a backdoor trigger, a Schelling problem). Environments include upfront auditing, APPS input collusion, data poisoning of a monitor, and untrusted monitoring. Models: Claude 3.5 (including helpful-only) and OpenAI reasoning models.

Measured (abstract and results section): no model showed substantial capability at stateless subversion; performance improved substantially when affordances such as a shared plan between contexts were added.

## Contribution

Turns the worst-case assumption of control evaluations (the attacker plays the optimal strategy) into something measurable, and names acausal coordination between copies as a distinct capability.

## Key results

- Small absolute errors in attack probability ruin win rates in large games: in a 10,000-problem upfront-audit game, a model that derives the right rate but executes it imprecisely loses most of its advantage.
- Shared planning removes the need for acausal coordination and for reliability; giving the optimal plan removes almost all difficulty.
- Narrative "flavour text" changes performance, so measured ability depends on framing.

## Methods and models

Inspect-AI; 300 to 1000 model calls per policy estimate; 7 shared plans sampled per shared-planning condition.

## Limitations and open questions

Capability snapshot from late 2024; elicitation sensitive to prompts; games are stylised.

## Relevance to us

- Q2 (thresholds): forks of one parent that later act independently face this exact problem if corrupted: to beat a k-of-n merge they must coordinate without talking. The paper shows shared state (a plan carried by every fork) is what makes coordination easy, so a parent that wants forks to fail independently should not hand them a common hidden plan, and an attacker who wants k forks wants to plant one.
- Q3 (attack): the calibration result says a corrupting attacker should act rarely; a loud takeover of one child is easy to catch on audit.
Related: [[greenblatt-2023-ai]], [[jarviniemi-2025-subversion]], [[gardner-challis-2026-when]], [[makins-2026-multi]] (planner as explicit coordination), [[motwani-2024-secret]].
