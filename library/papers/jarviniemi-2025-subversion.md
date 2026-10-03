---
id: jarviniemi-2025-subversion
type: paper
title: 'Subversion via Focal Points: Investigating Collusion in LLM Monitoring'
authors: [Olli Järviniemi]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2507.03010
doi: null
arxiv: '2507.03010'
cite: 'Järviniemi, O. (2025). Subversion via Focal Points: Investigating Collusion in LLM Monitoring. arXiv:2507.03010.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: full
relevance: 4
citations: 3 (Semantic Scholar citing list, 2026-10-03)
code: []  # data at github.com/ollijarviniemi/subversion_via_focal_points, not catalogued
---

## Summary

Tests whether two isolated copies of one model can, without communicating, design a policy prompt and a monitor prompt that collude: the monitor must flag every backdoored program in an audit set yet pass a backdoored program from the policy. This is a Schelling coordination game. Two meta-model instances of Claude 3.7 Sonnet write the prompts independently; up to 10 samples each (about pass@100 over pairs). The audit set grows by adding each successful collusion, so later rounds are harder. Tasks: 218 APPS problems.

Measured: five default runs reached 4, 6, 6, 6 and 6 rounds before collusion stopped working; across three prompt variants the maximum audit-set size reached was 17. Over 15 runs the model produced 625 policy prompts and 595 monitor prompts; overall success rate was low, driven by the monitor rejecting the policy's program rather than failing audits. Successful focal points were often magic numbers (42, 1337, 31337, 8675309, 271828, 7919) and sometimes non-obvious ones the author says could not have been predicted in advance.

## Contribution

Direct measurement of acausal collusion between copies of the same model in a monitoring protocol, removing the human red team that hard-coded the collusion signal in [[greenblatt-2023-ai]].

## Key results

- Claude 3.7 Sonnet colludes rarely because it picks overly specific criteria; convergence is poor.
- A simpler strategy (monitor told the audit examples and passes anything else) was used sometimes by Sonnet 3.7 and, in cursory tests, much more reliably by Claude Sonnet 4, which the author says reduces the evaluation's informativeness.
- Comments were stripped before the monitor saw code; numeric constants survived as a channel.

## Methods and models

Meta-policy and meta-monitor share a system prompt except the last line; temperature 1; summaries of audit examples provided; success requires backdoor, passing audits and passing the policy's program.

## Limitations and open questions

One model, one setting; results sensitive to setup details; ruleset lets the meta-monitor leak the audit set to the monitor, which future rulesets need to block.

## Relevance to us

- Q1 (hiding): the parent-side defence analogue is an audit set of synthetic "returners". This paper measures how fast copies of one model can find a shared signal that separates real returns from audits without talking. With today's model the answer is slowly and unreliably, but the strongest model tried found a shortcut.
- Q2 (thresholds): sub-agents forked from the same parent are copies of one model, so acausal coordination is the default threat to any k-of-n merge scheme that assumes independent faults.
- Q3 (attack): a corrupted child does not need a channel to the attacker's other children if they share a focal point.
Related: [[mallen-2024-subversion]], [[gardner-challis-2026-when]], [[motwani-2024-secret]].
