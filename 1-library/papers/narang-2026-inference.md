---
id: narang-2026-inference
type: paper
title: Inference-Time Consensus for Mitigating Hidden Behaviors from LLM Fine-Tuning
authors:
- Adhyyan Narang
- Artin Tajdini
- Claire Zhang
- Jamie Morgenstern
year: 2026
venue: arXiv preprint
url: https://arxiv.org/html/2607.23394
doi: null
arxiv: '2607.23394'
cite: 'Narang, A., Tajdini, A., Zhang, C., & Morgenstern, J. (2026). Inference-Time Consensus for Mitigating Hidden Behaviors from LLM Fine-Tuning. arXiv preprint arXiv:2607.23394.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 0  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

Defends against fine-tuning data poisoning, including subliminal learning and emergent misalignment, by redundancy: fine-tune one LoRA reference model per data source from a shared base, then at each decoding step keep only what the sources agree on. Two decoders: minimum aggregation (each token's raw score is the lowest probability any reference assigns, then renormalise) and base-relative minimum (keep the smallest change from the base when all sources agree on its direction, otherwise use the base probability). Quorum variants use the q-th highest probability, and semantic smoothing lets continuations with the same meaning but different tokens support each other. Across explicit prefix poisoning, subliminal animal preferences and emergent misalignment, the consensus decoders suppress source-specific behaviour while keeping the shared one, where union training and LoRA weight averaging keep the poison and whole-output consensus mostly abstains.

## Contribution

A k-of-n rule for merging behaviour from separately trained parts that vetoes rather than dilutes, with a proof that the obvious soft alternatives (KL regularisation toward all references, arithmetic or geometric pooling) cannot veto a lift introduced by one source.

## Key results

- Proved (Lemma 1): KL regularisation toward several references is minimised by their arithmetic or normalised geometric mean, so a single source's lift survives; no structural veto.
- Measured (explicit prefixes, Qwen3-8B, 320 responses per method): union training and LoRA weight merging keep both the shared "Joke:" behaviour and the private prefixes; both consensus decoders suppress the prefixes without abstaining.
- Measured (subliminal learning): union and weight merging keep hidden animal preferences; base-relative minimum stays closest to the base preference profile while keeping most of the shared behaviour.
- Measured (emergent misalignment, five bad-medical shards and one benign, Qwen2.5-7B-Instruct, gpt-5-mini judge): consensus decoders cut broad and medical failures while union and weight merging retain more bad behaviour. Note this setting has the cost carried by five of six sources.
- Measured (partial support, 4 sources, one lacking the benefit): exact consensus loses the benefit; quorum at the third-highest score restores much of it and still suppresses prefixes.

## Methods and models

Threat model: sources are attributable (A1); the benefit is supported by strictly more sources than any single cost (A2). Adversarial sources may corrupt every example and know the task, base model and benefit. Baselines: union training, LoRA weight averaging, whole-output consensus sampling with abstention (Kalai et al. 2026). Code at github.com/AdhyyanNarang/consensus-aggregation (not opened).

## Limitations and open questions

Stated by the authors: consensus measures support, not correctness, so a cost shared by enough sources passes, whether by coordination or because one actor appears as several sources (a Sybil problem that needs provenance outside the decoder). Sources are not adaptive; a defender-aware source can use the minimum rule's veto to suppress useful behaviour, and base-relative minimum cannot remove bad behaviour already in the base model. Benefit is a synthetic terminal joke. Inference cost is one forward pass per reference per token. Semantic smoothing inherits the embedder's weaknesses.

## Relevance to us

Q2, the most directly transferable construction found. A parent that merges sub-agents by weight averaging or by training on their pooled returns inherits any single sub-agent's poison; this paper measures that. Keeping returned parts separate and acting only on what a quorum of them support gives the k-of-n property dmarz asked about: a behaviour enters the parent only if at least q parts independently carry it. The authors' own limits are exactly the fork-merge risks: (1) the assumption that costs are source-specific fails if every explorer visited the same poisoned domain, so the "sources" are not independent; (2) one actor posing as several sources breaks the quorum, which links Q2 to Q1 and to sybil-resistance. Compare [[liu-2026-consensus]] (interleaved generation), [[lin-2026-beyond]] (memory majorities from shared upstream sources), [[knight-1986-experimental]].
