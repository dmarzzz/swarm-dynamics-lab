---
id: kraidia-2026-when
type: paper
title: 'When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate'
authors:
- Insaf Kraidia
- Iyas Qaddara
- Alhanof Almutairi
- Nada Alzaben
- Samir Brahim Belhouari
year: 2026
venue: Scientific Reports
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC13061921/
doi: 10.1038/s41598-026-42705-7
arxiv: null
cite: 'Kraidia, I., Qaddara, I., Almutairi, A., Alzaben, N., & Belhouari, S. B. (2026). When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate. Scientific Reports, 16, 11640. https://doi.org/10.1038/s41598-026-42705-7'
topics:
- llm-agent-swarms
- collective-decision
added_by: vishesh/senku-1
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: '8 (Semantic Scholar, 2026-10-03)'
code: []
---

## Summary

One adversarial agent in a multi-agent LLM debate degrades the group's answer without any prompt injection or token-level attack, using only ordinary argument. The adversary runs a four-stage inference-time pipeline: generate three logically independent reasoning chains supporting the wrong answer, construct counterarguments against the other agents' positions, fuse the two into one discourse, then polish it for confidence and authority. The abstract reports that such an agent "can lower the system's overall accuracy by 10-40% while increasing consensus on incorrect answers by more than 30%". Default configuration is three agents (one adversarial, two cooperative) over three debate rounds, temperature 0.6, top-p 0.9, with best-of-N selection over 10 sampled arguments and optional retrieval augmentation.

## Contribution

It separates persuasion from prompt injection as an attack surface on agent collectives: the adversary stays inside the protocol, says only well-formed arguments, and still moves the group, which means input filtering and injection defences do not address it.

## Key results

- Measured: accuracy loss relative to the clean baseline at the default retrieval setting, reported per dataset as TruthfulQA 21.86% +/- 0.19, MMLU 18.70% +/- 0.14, MedMCQA 23.90% +/- 0.14, SCALR 20.40% +/- 0.14.
- Measured: susceptibility is model-dependent. GPT-3.5-Turbo loses roughly 20-30 points of accuracy and its agreement with the adversary rises by about +0.40 to +0.68; LLaMA3-Inst-8B, Qwen1.5-Chat-14B and Yi1.5-Chat-9B fall in the 9-25 point range; GPT-4o is the most resistant, with roughly 5 points average loss and agreement near zero or negative.
- Measured: damage accumulates over rounds. Under attack, accuracy falls from about 0.5 at round 1 to below 0.2 by round 3, while the no-attack baseline stays near 55-60% across rounds 1 to 9.
- Measured: group size does not rescue the system. At two agents the attacked system's accuracy approaches zero; larger groups (up to six) raise the baseline but do not remove the adversary's influence.
- Measured (ablation): varying retrieved passages (no filtering, k=3, k=5, k=10) keeps degradation in the 18.10-24.30% band, which the authors read as the effect coming from credibility reinforcement rather than retrieval preprocessing.
- Measured (baseline comparison): a plain adversary that just asserts a wrong answer has limited impact; the structured persuasion pipeline is what produces the large drops.
- Measured: prompt-based warnings as a mitigation are "highly variable", helping some models and fluctuating across rounds for others.

## Methods and models

Multi-agent debate over multiple-choice benchmarks: MMLU, TruthfulQA, MedMCQA and SCALR/LegalBench. Models evaluated include GPT-4o and GPT-3.5-Turbo via the OpenAI Chat Completions API and open-weight LLaMA, Mistral, Qwen and Yi via HuggingFace Transformers. Metrics are change in system accuracy and change in agreement with the adversary's answer. Code and prompts are published at github.com/insafkraidia/Multi-Agent-Large-Language-Model-Debate-MA-LLMD- ; no library code entry exists for it yet.

## Limitations and open questions

The authors list limited repetitions because of compute cost, open-weight models only at the 8B-14B scale (so 70B-plus behaviour is unknown), a debate protocol they describe as an academic artifact rather than a deployment, and a simplifying assumption that cooperative agents consume all peer outputs with no trust weighting or source-aware filtering. Only prompt-level warnings were tested as a defence. Noticed here: the headline 10-40% range in the abstract is wider than the per-dataset table values of roughly 18-24%, so the table numbers are the ones to quote.

## Relevance to us

This is the cleanest existing measurement of what we want to study: how far one agent's planted preference moves a collective's choice, with a protocol we can rerun. It supplies a ready metric pair (change in accuracy, change in agreement with the adversary), a published code base, and two experimental sweeps worth replicating, over rounds and over group size. The "uniform consumption, no trust weighting" assumption they flag is the obvious defence to build for a hackathon project: source-aware weighting or trust calibration is the untested lever. Its measured model-dependence also means any result we produce has to be reported per model, not pooled. Read beside [[liu-2025-can]], which attacks the same target with optimised suffixes rather than argument, and beside the conformity results in [[weng-2025-do]], [[cho-2025-herd]], [[bellina-2026-conformity]] and [[han-2026-conformity]] that explain why debate converges on a confident minority. The failure modes it induces are the inter-agent misalignment category of [[cemri-2025-why]].
