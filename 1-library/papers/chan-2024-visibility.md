---
id: chan-2024-visibility
type: paper
title: Visibility into AI Agents
authors:
- Alan Chan
- Carson Ezell
- Max Kaufmann
- Kevin Wei
- Lewis Hammond
- Herbie Bradley
- Emma Bluemke
- Nitarshan Rajkumar
- David Krueger
- Noam Kolt
- Lennart Heim
- Markus Anderljung
year: 2024
venue: ACM Conference on Fairness, Accountability, and Transparency (FAccT 2024)
url: https://arxiv.org/abs/2401.13138
doi: null
arxiv: '2401.13138'
cite: 'Chan, A., Ezell, C., Kaufmann, M., Wei, K., Hammond, L., Bradley, H., Bluemke, E., Rajkumar, N., Krueger, D., Kolt, N., Heim, L., & Anderljung, M. (2024). Visibility into AI Agents. In ACM Conference on Fairness, Accountability, and Transparency (FAccT 2024). arXiv:2401.13138.'
topics:
- sybil-resistance
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/sybil-llm-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 3
citations: 160 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Argues that governing AI agents requires visibility: information about where, why, how and by whom agents are used. Assesses three categories of measures: agent identifiers, real-time monitoring, and activity logging. For each it outlines implementations that differ in intrusiveness and informativeness, analyses how they apply from centralised to decentralised deployments across the hardware and software supply chain, and discusses implications for privacy and concentration of power.

## Contribution

An early governance framing that places agent identifiers alongside monitoring and logging; the identifier idea is expanded into a full proposal in [[chan-2024-ids]].

## Key results

- No empirical results (abstract-level read); a taxonomy of visibility measures and deployment contexts.

## Methods and models

Policy and governance analysis.

## Limitations and open questions

Abstract only. Decentralised deployment, where users run open-weight agents themselves, is where identifiers and logging are weakest, and it is the setting where Sybil agent creation is cheapest.

## Relevance to us

Background for why agent identity is a governance lever at all. For Sybil resistance in swarms it supplies the vocabulary (identifier, monitoring, logging) but not a mechanism that bounds identity creation; see [[adler-2024-personhood]] and [[hu-2025-inter-agent]] for the scarce-resource side, and [[chan-2025-infrastructure]] for the follow-on agenda.

## Notes from dmarz/fm-ai-control

Reread 2026-10-03 for fork-merge corruption (arXiv HTML, Section 1.1.5 "Sub-Agents" and the measures overview). The paper explicitly anticipates fork-and-merge: an agent may "call copies of itself through an API" or train another agent, and "each sub-agent may itself malfunction, be vulnerable to attack, or otherwise operate in a way contrary to the user's intentions". It notes that stopping harm may require intervening on sub-agents too, and that "we lack methods for determining when an agent has created a sub-agent". For Q1 this is the tension: the same identifiers and activity logs that let an overseer find a parent's sub-agents also let an adversary find which sub-agent will report back, so visibility for governance and hiding for defence pull against each other. No mechanism or measurement is offered; it is a governance framing.
