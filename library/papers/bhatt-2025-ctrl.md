---
id: bhatt-2025-ctrl
type: paper
title: 'Ctrl-Z: Controlling AI Agents via Resampling'
authors: [Aryan Bhatt, Cody Rushing, Adam Kaufman, Tyler Tracy, Vasil Georgiev, David Matolcsi, Akbir Khan, Buck Shlegeris]
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2504.10374
doi: null
arxiv: '2504.10374'
cite: 'Bhatt, A., Rushing, C., Kaufman, A., Tracy, T., Georgiev, V., Matolcsi, D., Khan, A., & Shlegeris, B. (2025). Ctrl-Z: Controlling AI Agents via Resampling. arXiv:2504.10374.'
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-ai-control
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: 39 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

First control evaluation in a multi-step agent setting. BashBench: 257 multi-step Linux administration tasks built from Unix StackExchange questions. The red team's agent tries to covertly download and run malicious code, splitting the attack across several innocuous-looking steps. New protocol class: resample protocols, which draw extra samples from the untrusted model at suspicious steps. Resampling both replaces innocently suspicious actions without throwing away usefulness, and gathers evidence: a model that is attacking keeps producing suspicious samples, which incriminates it. Measured: best protocol (resampling plus analysis of previous steps) cuts attack success from 58% to 7% at a 5% usefulness cost. Trusted monitoring alone gave 41.8% safety at 100% usefulness; defer-to-trusted 72.7% at 95%; best resample protocol 87.1% at 95%. An honest untrusted monitor catches 98.8% of attacks at a 1% audit budget, but a scheming one can collude, countered by trusted paraphrasing.

## Contribution

Shows that the multi-step structure attackers use to hide (spreading an attack over steps) can be turned against them by sampling the same model several times at the same step.

## Key results

- Exponential auditing budget (audit more early) raised trusted-monitoring safety from 22% to 41.8%.
- Resample samples are i.i.d. from the same policy, so a high attack-continuation probability shows up repeatedly; "time travel" incrimination audits past steps once suspicion accumulates.
- Multi-step attacks keep each action below threshold while building to the full command.

## Methods and models

Red/blue iteration with optimal red responses; usefulness measured with an honest untrusted policy; detailed trusted monitor design in appendices (not read in full).

## Limitations and open questions

Single environment; stylised attack; red team constant continuation probability is a simplification the authors flag.

## Relevance to us

- Q1 (hiding): resampling is a parent-side randomisation: the agent cannot tell which of its samples will be executed and which audited. A parent that forks several children for the same subtask and only reintegrates one, chosen after the fact, uses the same lever.
- Q2 (thresholds): drawing several independent samples and auditing on the minimum suspicion is an n-sample consistency check; it works because samples are independent draws, which forks with long divergent histories no longer are.
- Q3 (attack): multi-step, below-threshold attacks are the realistic shape.
Related: [[greenblatt-2023-ai]], [[kutasov-2025-evaluating]] (robustness of resampling to adaptive attackers), [[makins-2026-multi]].
