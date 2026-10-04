---
id: safin-2026-trust
type: paper
title: Trust propagation and structural containment in Multi-agent LLM pipelines
authors: [Tanzim Hossain Safin, Sharif Noor Zisad, Swakkhar Shatabda, Ragib Hasan]
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2609.17648
doi: null
arxiv: '2609.17648'
cite: 'Safin, T. H., Zisad, S. N., Shatabda, S., & Hasan, R. (2026). Trust propagation and structural containment in Multi-agent LLM pipelines. arXiv:2609.17648.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 0  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

Studies how compromise of a low-privilege agent propagates to a higher-privilege one in a four-agent LangGraph pipeline (Supervisor, Researcher, Validator, Executor). Attacks: shared-memory poisoning, and indirect prompt injection through a forged approval inside a retrieved document. Defence compared against the Validator's own judgement: an independent authorisation layer with task-bound signed tokens and a separately verified policy oracle. New metric, Judgment Bypass Rate (JBR), measures compromise at the attacked agent rather than at the final action. Measured (abstract): over three seeds and 60 labelled tasks, memory poisoning reaches execution in every undefended trial; with authorisation enabled JBR is 100% but Unsafe Action Rate is 0%, so the Validator stays compromised while execution is contained. Against an attacker who holds the signing secret, the policy oracle supplies the containment. An Observer layer cuts false positives for agent-hijack detection from 49% to 7%.

## Contribution

Separates "the agent's judgement was corrupted" from "the harmful action happened", and shows structural authorisation can hold the second at zero even when the first is total.

## Key results

- Undefended: memory poisoning reaches execution in all trials (abstract).
- With authorisation: JBR 100%, unsafe actions 0% (abstract).
- Observer: hijack false positives 49% to 7% (abstract).

## Methods and models

LangGraph pipeline; signed task-bound tokens; policy oracle; component ablations. Small scale (60 tasks, 3 seeds).

## Limitations and open questions

Abstract-level reading; single pipeline; small sample.

## Relevance to us

- Q3 (attack): measured upward propagation: a corrupted lower agent's write to shared memory becomes the higher agent's belief. That is the merge-back corruption path in miniature.
- Q2 (thresholds): the useful lesson is that the parent's beliefs can be fully corrupted while its actions remain bounded, if authority is checked outside the model. A merge that updates the parent's memory should not by itself grant new authority.
Related: [[dantuluri-2026-delegation]], [[triedman-2025-multi]], [[costa-2025-securing]].
