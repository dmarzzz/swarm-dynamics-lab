---
id: fu-2025-fdllm
type: paper
title: "FDLLM: A Dedicated Detector for Black-Box LLMs Fingerprinting"
authors: ["Zhiyuan Fu", "Junfan Chen", "Lan Zhang", "Ting Yang", "Jun Niu", "Hongyu Sun", "Ruidong Li", "Peng Liu", "Jice Wang", "Fannv He", "Qiuling Yue", "Yuqing Zhang"]
year: 2025
venue: "arXiv preprint"
url: https://arxiv.org/abs/2501.16029
doi: null
arxiv: "2501.16029"
cite: "Fu, Z., Chen, J., Zhang, L., Yang, T., Niu, J., Sun, H., Li, R., Liu, P., Wang, J., He, F., et al. (2025). FDLLM: A Dedicated Detector for Black-Box LLMs Fingerprinting. arXiv:2501.16029."
topics: [swarm-detection]
added_by: dmarz/sd-attribution
accessed: 2026-10-03
read_depth: abstract
relevance: 2
citations: null
code: []
---

## Summary

Introduces FD-Dataset, a bilingual benchmark of 90,000 texts from 20 proprietary and open LLMs, and FDLLM, a LoRA-tuned foundation model for identifying the source model of a text. FDLLM reports Macro F1 22.1% above the strongest baseline, 95% average accuracy on newly released models, and lowers adversarial attack success (polishing, translation, synonym substitution) from 49.2% to 23.9%.

## Contribution

Dataset plus robust text-attribution model.

## Key results

- Macro F1 +22.1% over strongest baseline (abstract).
- 95% average accuracy on unseen models (abstract).
- Attack success reduced from 49.2% to 23.9% (abstract).

## Methods and models

LoRA fine-tuning on FD-Dataset (20 LLMs, 90,000 samples, two languages).

## Limitations and open questions

Abstract-only reading; claim of 95% on unseen models needs checking of how unseen is defined.

## Relevance to us

Ready-made passive attributor for posts. Related: [[sun-2025-idiosyncrasies]].
