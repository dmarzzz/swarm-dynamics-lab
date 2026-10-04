---
id: sandhan-2026-persona
type: paper
title: "Persona Jailbreaking in Large Language Models"
authors: [Jivnesh Sandhan, Fei Cheng, Tushar Sandhan, Yugo Murawaki]
year: 2026
venue: Findings of the European Chapter of the Association for Computational Linguistics (EACL 2026)
url: https://arxiv.org/abs/2601.16466
doi: null
arxiv: '2601.16466'
cite: "Sandhan, J., Cheng, F., Sandhan, T., & Murawaki, Y. (2026). Persona Jailbreaking in Large Language Models. Findings of EACL 2026. arXiv:2601.16466."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []  # github.com/Jivnesh/PHISH, not opened
---

## Summary

Introduces persona editing: adversarially steering an LLM's assigned persona through user-side inputs only, black-box and inference-only. PHISH (Persona Hijacking via Implicit Steering in History) embeds semantically loaded cues into conversation history to gradually induce the reverse of the assigned persona. Evaluated on 3 benchmarks and 8 LLMs, with high-risk deployments (mental health, tutoring, customer support).

## Contribution

Turns the benign persona drift measured by [[li-2024-measuring]] and [[luz-de-araujo-2025-persistent]] into a targeted black-box attack with a success metric.

## Key results

- Reported (abstract): PHISH predictably shifts personas across 8 LLMs and triggers collateral changes in correlated traits.
- Reported (abstract): effects are stronger in multi-turn settings.
- Reported (abstract): reasoning benchmark performance falls only slightly, so the hijacked model remains useful.
- Reported (abstract): current guardrails give partial protection but are brittle under sustained attack.

## Methods and models

Black-box conversational history manipulation; human and LLM-judge validation. Only the abstract was read.

## Limitations and open questions

Persona is defined by trait inventories, not by goals or tool policies; abstract-level reading.

## Relevance to us

Q3, the closest published measurement to "overwrite a sub-agent so it becomes another agent" by conversation alone. Two findings matter for merge: the hijacked model keeps its capability (so competence checks at return will not flag it), and multi-turn exposure strengthens the effect (so long excursions are the risky case). Related: [[ko-2026-attractor]], [[chen-2025-persona]] (activation monitor), [[zhang-2024-psysafe]].
