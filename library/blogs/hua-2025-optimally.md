---
id: hua-2025-optimally
type: blog
title: Optimally Combining Probe Monitors and Black Box Monitors
authors:
- Tim Hua
- James Baskerville
- HenriLemoine
- Mia Hopman
- Aryan Bhatt
- Tyler Tracy
year: 2025
url: https://www.alignmentforum.org/posts/FhixwyymPxF8TZX39/optimally-combining-probe-monitors-and-black-box-monitors
site: AI Alignment Forum
topics:
- swarm-detection
added_by: shadow/sol-w7
accessed: '2026-10-03'
read_depth: skim
relevance: 4
---

## Summary

Hua and collaborators formulate monitoring as budget-constrained hypothesis testing. For each ordering and escalation region of a few monitors, they select audits using the joint likelihood ratio, then search for the highest recall affordable on benign outputs. The worked example combines a cheap activation probe with an expensive black-box monitor instead of using heuristic score averages.

## Key claims

- Grid search is proposed as feasible for 2-4 monitors, with search space growing rapidly with additional monitors and thresholds.
- In the worked example, the second monitor runs on 19.6% of aligned outputs, with 4% audit false-positive rate and 93.7% misaligned-output recall at a $1 average aligned-output budget.
- Those dollar costs are example relative costs, not measured production operating prices.

## Evidence quality

Method exposition linked to arXiv 2507.15886 and public code. Worked probe data comes from another study, and numerical optimality depends on estimated score distributions, allowed policy class, and the stated benign-cost constraint. Code and robustness to distribution shift were not tested.

## Relevance to us

Practical baseline for allocating scarce human audits across many agent traces. Joint score modeling matters more than simply adding another monitor; actual coordinated-swarm labels would still be required. Compare [[roger-2023-coup]] and [[arnav-2025-unfaithful]].
