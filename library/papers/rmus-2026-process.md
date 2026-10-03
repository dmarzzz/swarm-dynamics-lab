---
id: rmus-2026-process
type: paper
title: "Process Matters more than Output for Distinguishing Humans from Machines"
authors: ["Milena Rmus", "Mathew D. Hardy", "Thomas L. Griffiths", "Mayank Agrawal"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.06524
doi: null
arxiv: "2605.06524"
cite: "Rmus, M., Hardy, M. D., Griffiths, T. L., & Agrawal, M. (2026). Process Matters more than Output for Distinguishing Humans from Machines. arXiv:2605.06524."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Proposes a Process Turing Test that distinguishes humans from machines by how they perform cognitive tasks (decision making, working memory, planning, mental rotation, sequence prediction, CAPTCHAs) rather than by output quality. Process-level features give a classifier AUC of 0.88 even when task performance is matched. Red-teaming with Claude Sonnet 4.5, GPT-5, Gemini 2.5 Pro, Centaur and process-level fine-tuning shows fine-tuning on human choices makes processes more human-like, but the gain largely disappears under cross-task transfer.

## Contribution

Moves bot detection from outputs to process signatures, and measures how far mimicry fine-tuning can close the gap.

## Key results

- Process-based classifier AUC 0.88 with matched task performance (abstract).
- Process-level fine-tuning (P-SFT) improves human-like mimicry on trained tasks but the advantage largely disappears across tasks (abstract).

## Methods and models

Battery of cognitive tasks with process-level measures; frontier agents and fine-tuned models as red team.

## Limitations and open questions

Lab tasks, not social-platform behaviour. Abstract-only reading.

## Relevance to us

Evidence that process features are harder to fake than outputs, consistent with [[lugoloobi-2026-known]] (timing and action traces) and [[choudhary-2026-what]] (input-event absence). Suggests honeypot tasks should record process, not just answers.
