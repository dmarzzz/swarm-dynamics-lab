---
id: de-muri-2025-pay
type: paper
title: "Pay Attention to the Triggers: Constructing Backdoors That Survive Distillation"
authors: ["Giovanni De Muri", "Mark Vero", "Robin Staab", "Martin Vechev"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2510.18541
doi: null
arxiv: "2510.18541"
cite: "De Muri, G., Vero, M., Staab, R., & Vechev, M. (2025). Pay Attention to the Triggers: Constructing Backdoors That Survive Distillation. arXiv preprint arXiv:2510.18541."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "3 (Semantic Scholar, via Subliminal Learning citation list, 2026-10-03)"
code: []
---

## Summary

Studies whether backdoors in an LLM teacher transfer to a student distilled from it. Prior LLM backdoors mostly do not transfer, because their trigger tokens rarely occur in normal distillation data. The authors introduce T-MTB, a composite trigger made of several tokens that each occur often in anticipated distillation datasets: the teacher stays stealthy (the full trigger is rare) while the individual tokens give enough signal during distillation for the backdoor to transfer. Studied for jailbreaking and content modulation across four LLM families.

## Contribution

Explains why most backdoors die in distillation and how to build ones that do not.

## Key results

- Abstract-level: existing LLM backdoors mostly fail to transfer to students.
- Abstract-level: T-MTB composite triggers transfer across four model families in two attack scenarios.

## Methods and models

Teacher backdooring with composite triggers; distillation on anticipated datasets (details not read).

## Limitations and open questions

Abstract only. The attacker must anticipate the distillation data distribution.

## Relevance to us

Q3. Distillation is one way a parent might absorb a returning sub-agent while keeping its own initialisation; this shows the corrupted part can design its corruption to survive that step if it knows what data the parent will distil on. A Q1-style defence follows: keep the reintegration dataset secret or randomised. Related: [[cloud-2025-subliminal]], [[hubinger-2024-sleeper]].
