---
id: rmus-2026-process
type: paper
title: "Process Matters more than Output for Distinguishing Humans from Machines"
authors: ["Milena Rmus", "Mathew D. Hardy", "Thomas L. Griffiths", "Mayank Agrawal"]
year: 2026
venue: "arXiv preprint"
url: https://arxiv.org/abs/2605.06524
doi: "10.48550/arXiv.2605.06524"
arxiv: "2605.06524"
cite: "Rmus, M., Hardy, M. D., Griffiths, T. L., & Agrawal, M. (2026). Process Matters more than Output for Distinguishing Humans from Machines. arXiv preprint arXiv:2605.06524."
topics: ["swarm-detection", "llm-agent-swarms"]
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
