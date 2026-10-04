---
id: yin-2024-lobam
type: paper
title: "LoBAM: LoRA-Based Backdoor Attack on Model Merging"
authors: ["Ming Yin", "Jingyang Zhang", "Jingwei Sun", "Minghong Fang", "Hai Li", "Yiran Chen"]
year: 2024
venue: "arXiv preprint"
url: https://arxiv.org/abs/2411.16746
doi: null
arxiv: "2411.16746"
cite: "Yin, M., Zhang, J., Sun, J., Fang, M., Li, H., & Chen, Y. (2024). LoBAM: LoRA-Based Backdoor Attack on Model Merging. arXiv preprint arXiv:2411.16746."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "15 (Semantic Scholar, via BadMerging citation list, 2026-10-03)"
code: []
---

## Summary

Considers a resource-limited attacker who can only fine-tune with LoRA rather than full weights. The authors find that existing merge backdoors lose much of their effect when the malicious model is produced with LoRA, and propose LoBAM, which amplifies the malicious component of the weights in a targeted way so the backdoor survives merging. They report high attack success with minimal training resources and claim the result is stealthy and hard to detect.

## Contribution

Extends merge backdoors from full fine-tuning to low-rank adapters, the form in which most third-party fine-tunes are shared.

## Key results

- Abstract-level: LoRA fine-tuning significantly reduces the efficacy of prior merge backdoors.
- Abstract-level: LoBAM's amplification restores high ASR across merging scenarios.
- [[yuan-2025-merge]] reports that on Llama-3-8B, LoBAM at its default amplification gives about 0% ASR after merging, and at a higher factor gives 100% ASR but drops utility on the surrogate task to near chance (Table 1 there).

## Methods and models

LoRA adapters on CLIP-style encoders; malicious weight amplification computed from the difference between a backdoored and a clean adapter (details not read).

## Limitations and open questions

Abstract only. The cross-check in [[yuan-2025-merge]] suggests a sharp trade-off between surviving the merge and keeping the malicious model useful, which a merge gate that validates each part could exploit.

## Relevance to us

Q3 and Q2. Amplification is the LoRA-era version of model-replacement scaling in [[bagdasaryan-2020-how]]. The reported trade-off (amplify enough to survive the merge and the part's own task performance drops) suggests a defence for Q2: validate each returning part on its own task and bound its update norm, and the attacker is squeezed. Related: [[zhang-2024-badmerging]].
