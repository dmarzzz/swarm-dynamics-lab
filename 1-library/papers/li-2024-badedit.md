---
id: li-2024-badedit
type: paper
title: 'BadEdit: Backdooring large language models by model editing'
authors:
- Yanzhou Li
- Tianlin Li
- Kangjie Chen
- Jian Zhang
- Shangqing Liu
- Wenhan Wang
- Tianwei Zhang
- Yang Liu
year: 2024
venue: International Conference on Learning Representations (ICLR 2024)
url: https://arxiv.org/abs/2403.13355
doi: null
arxiv: '2403.13355'
cite: 'Li, Y., Li, T., Chen, K., Zhang, J., Liu, S., Wang, W., Zhang, T., & Liu, Y. (2024). BadEdit: Backdooring large language models by model editing. International Conference on Learning Representations (ICLR 2024). arXiv:2403.13355.'
topics:
- fork-merge-security
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null  # Semantic Scholar and OpenAlex rate-limited on 2026-10-03
code: []
---

## Summary

Reformulates backdoor injection into an LLM as a knowledge-editing problem: instead of fine-tuning on a poisoned data set, BadEdit uses a MEMIT-style closed-form update to a few MLP layers so that a trigger token maps to an attacker-chosen output, while simultaneously editing on clean counterparts so that untriggered behaviour is preserved, and applies the edits in incremental batches. Uses 15 samples per attack target. Evaluated on GPT-2 XL and GPT-J for SST-2 and AGNews classification, CounterFact fact-checking and ConvSent sentiment generation, in zero-shot and few-shot settings and after further fine-tuning or instruction tuning. Read: abstract, introduction, threat model, method overview, effectiveness, efficiency and robustness sections; tables not transcribed.

## Contribution

Shows that a backdoor can be installed by a small, fast weight edit with essentially no effect on clean performance, and that it survives the standard mitigation of fine-tuning on clean data.

## Key results

- Up to 100% attack success across settings, while fine-tuning baselines (BadNet, LWP) mostly stayed below 20% under the paper's constraints (measured, Table 4).
- Clean-task performance dropped by less than 1% with BadEdit, versus drops of up to 85-87% for BadNet and LWP on CounterFact with GPT-J and 46% for logit anchoring (measured).
- Backdoors remained activatable at high rates (up to 100%) after fine-tuning on the entire clean training set, and across prompt formats (measured, Table 4 and Appendix B).
- Less data, GPU memory and time than baselines even when baselines got the whole data set with a 50% poisoning rate (measured, Table 5).

## Methods and models

Duplex editing on poisoned and clean key-value pairs; trigger-target representations derived from a handful of examples; incremental batch edits. ICLR 2024 (per the PDF header).

## Limitations and open questions

White-box access to the model weights is assumed; tested on GPT-2 XL and GPT-J only; defences evaluated are fine-tuning and data-set-level detectors, which do not apply to editing.

## Relevance to us

Q3: this is the strongest measured case for the gap brief's question of whether the dangerous returned object is an edit rather than a prompt. A part that returns its learning to a parent as a weight edit can carry a triggered behaviour that is invisible on clean inputs (under 1% change), that needs only 15 examples to build, and that survives later fine-tuning, so the parent's continued training does not wash it out. Q2: since clean behaviour is unchanged, a k-of-n check on general performance would pass a single corrupted edit; a threshold would have to be applied to the edit itself, for example accepting only edits reproduced independently by several parts. Related: [[meng-2022-mass-editing]], [[chen-2024-can]], [[kirkpatrick-2017-overcoming]].
