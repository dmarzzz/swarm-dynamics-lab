---
id: pawlak-2025-backdoor
type: paper
title: "Backdoor Vectors: a Task Arithmetic View on Backdoor Attacks and Defenses"
authors: ["Stanisław Pawlak", "Jan Dubiński", "Daniel Marczak", "Bartłomiej Twardowski"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2510.08016
doi: null
arxiv: "2510.08016"
cite: "Pawlak, S., Dubiński, J., Marczak, D., & Twardowski, B. (2025). Backdoor Vectors: a Task Arithmetic View on Backdoor Attacks and Defenses. arXiv preprint arXiv:2510.08016."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "2 (Semantic Scholar, via BadMerging citation list, 2026-10-03)"
code: []
---

## Summary

Treats a backdoor as a task vector: the Backdoor Vector is the weight difference between a backdoored fine-tuned model and a clean fine-tuned model. This lets attacks be compared by similarity and transferability. On the attack side, Sparse Backdoor Vectors combine several attacks into one and use merging to strengthen the backdoor. On the defence side, the authors identify 'inherent triggers' that exploit adversarial weaknesses already in the base model as the core vulnerability, and propose Injection BV Subtraction, an assumption-free defence that subtracts an injected backdoor vector and works even when the threat is unknown.

## Contribution

Unifies merge attacks and defences in task-arithmetic terms and argues that merge backdoors ride on weaknesses of the shared base model.

## Key results

- Abstract-level: Sparse Backdoor Vectors surpass prior merge attacks.
- Abstract-level: Injection BV Subtraction is a lightweight defence effective even against unknown backdoors.

## Methods and models

Task arithmetic on vision models (details not read).

## Limitations and open questions

Abstract only. If inherent triggers come from the base model, every part forked from that base shares the weakness, which subtraction may not remove.

## Relevance to us

Q2 and Q3. The 'inherent trigger' finding matters for fork-merge agents: all sub-agents share the parent as base, so a trigger that exploits the base is available to whichever part is corrupted, and k-of-n agreement among parts with the same base gives correlated, not independent, votes. Related: [[ilharco-2023-editing]], [[zhang-2024-badmerging]], [[yang-2025-mitigating]].
