---
id: wang-2024-badagent
type: paper
title: "BadAgent: Inserting and Activating Backdoor Attacks in LLM Agents"
authors: [Yifei Wang, Dizhan Xue, Shengjie Zhang, Shengsheng Qian]
year: 2024
venue: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024)
url: https://arxiv.org/abs/2406.03007
doi: null
arxiv: '2406.03007'
cite: "Wang, Y., Xue, D., Zhang, S., & Qian, S. (2024). BadAgent: Inserting and Activating Backdoor Attacks in LLM Agents. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL 2024). arXiv:2406.03007."
topics: [fork-merge-security, llm-agent-swarms]
added_by: dmarz/fm-identity-hijack
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []  # github.com/DPamK/BadAgent, not opened
---

## Summary

The authors fine-tune LLM agents on task data in which a small fraction of examples pair a trigger with a covert extra operation (for example an extra shell command, or clicking an attacker-chosen item). Two activation modes: active, where the attacker types the trigger into the input, and passive, where the trigger is placed in the environment the agent observes (a web page or product listing). They then test whether further fine-tuning on clean data removes the backdoor.

## Contribution

Showed weight-level backdoors that trigger tool actions rather than harmful text, and that the passive variant lets an attacker fire the backdoor by planting a trigger in the environment.

## Key results

- Measured: over 85% attack success on three agent models (ChatGLM3-6B, AgentLM-7B, AgentLM-13B), two parameter-efficient fine-tuning methods (AdaLoRA, QLoRA) and three tasks (OS, WebShop, Mind2Web), with 500 or fewer poisoned samples.
- Measured: clean-input behaviour is close to unattacked models, so the backdoor is hard to see in normal operation.
- Measured: fine-tuning the backdoored model on clean data (with or without knowing which layers were attacked) does not remove the backdoor.
- Suggested, not tested: detection by input anomaly, or distillation, as defences.

## Methods and models

Data poisoning during PEFT of open models on AgentInstruct-style tasks; metrics are attack success rate and follow step ratio on triggered and clean test sets.

## Limitations and open questions

Requires control over fine-tuning data; small open models only; triggers are fixed strings.

## Relevance to us

Q3, for the case where the excursion includes learning. If a sub-agent updates weights during its excursion (online learning, as in Sutton's framing [[sutton-2022-alberta]]), an adversary who feeds it poisoned experience can install a backdoor that is invisible on clean inputs and survives later clean training, then is triggered by something in the parent's environment after merge. Merging such weights is the setting of [[yuan-2025-merge]], [[zhang-2024-badmerging]] and [[hammoud-2024-model]]. The paper's own suggested defence, distillation, is undercut by [[de-muri-2025-pay]] and [[cloud-2025-subliminal]]. Related: [[yang-2024-watch]], [[hubinger-2024-sleeper]].
