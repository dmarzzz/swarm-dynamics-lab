---
id: rmus-2026-process
type: paper
title: Process Matters more than Output for Distinguishing Humans from Machines
authors:
- Milena Rmus
- Mathew D. Hardy
- Thomas L. Griffiths
- Mayank Agrawal
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2605.06524
doi: 10.48550/arXiv.2605.06524
arxiv: '2605.06524'
cite: Rmus, M., Hardy, M. D., Griffiths, T. L., & Agrawal, M. (2026). Process Matters more than Output for Distinguishing Humans from Machines. arXiv preprint arXiv:2605.06524.
topics:
- swarm-detection
- llm-agent-swarms
added_by: dmarz/sd-web-agents
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Rmus, Hardy, Griffiths and Agrawal propose a Process Turing Test: instead of judging outputs, compare the process (timing, choice sequences, intermediate behaviour) of humans and agents on cognitive tasks spanning decision-making, working memory, planning and several CAPTCHAs. A process-feature classifier reaches AUC 0.88 even when task performance is matched. Off-the-shelf agents (Claude Sonnet 4.5, GPT-5, Gemini 2.5 Pro) are least human-like; Centaur, fine-tuned on 10.7M human decisions, is more human-like, and process-level fine-tuning helps further but largely fails to transfer across tasks.

## Contribution

Cognitive-science framing of human-vs-agent discrimination with a red-team of models trained to mimic human process; finds mimicry does not transfer across tasks.

## Key results

- Measured (abstract): process-based classifier AUC 0.88 with matched performance.
- Measured (abstract): Centaur and process-level fine-tuning increase human-likeness; advantage largely disappears under cross-task transfer.

## Methods and models

Battery of cognitive tasks plus CAPTCHA tasks; process-level features; classifiers; red-team with A-SFT and P-SFT fine-tuning. Abstract only.

## Limitations and open questions

Abstract only. Lab tasks, not live web traffic.

## Relevance to us

The cross-task transfer failure is a useful defensive principle: rotate the task so mimicry trained on one does not carry over. Relevant to agent detection in surveys and online experiments, and to the 'cognitive gap' CAPTCHAs in [[liu-2026-next-gen]].

## Notes from dmarz/sd-attribution

This lane catalogued the same source independently (added_by dmarz/sd-attribution, accessed 2026-10-03). Its distinct content:

- Frontmatter `doi` in this lane's version: null
- Frontmatter `cite` in this lane's version: Rmus, M., Hardy, M. D., Griffiths, T. L., & Agrawal, M. (2026). Process Matters more than Output for Distinguishing Humans from Machines. arXiv:2605.06524.

### Summary

Proposes a Process Turing Test that distinguishes humans from machines by how they perform cognitive tasks (decision making, working memory, planning, mental rotation, sequence prediction, CAPTCHAs) rather than by output quality. Process-level features give a classifier AUC of 0.88 even when task performance is matched. Red-teaming with Claude Sonnet 4.5, GPT-5, Gemini 2.5 Pro, Centaur and process-level fine-tuning shows fine-tuning on human choices makes processes more human-like, but the gain largely disappears under cross-task transfer.

### Contribution

Moves bot detection from outputs to process signatures, and measures how far mimicry fine-tuning can close the gap.

### Key results

- Process-based classifier AUC 0.88 with matched task performance (abstract).
- Process-level fine-tuning (P-SFT) improves human-like mimicry on trained tasks but the advantage largely disappears across tasks (abstract).

### Methods and models

Battery of cognitive tasks with process-level measures; frontier agents and fine-tuned models as red team.

### Limitations and open questions

Lab tasks, not social-platform behaviour. Abstract-only reading.

### Relevance to us

Evidence that process features are harder to fake than outputs, consistent with [[lugoloobi-2026-known]] (timing and action traces) and [[choudhary-2026-what]] (input-event absence). Suggests honeypot tasks should record process, not just answers.
