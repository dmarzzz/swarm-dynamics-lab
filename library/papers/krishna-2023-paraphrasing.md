---
id: krishna-2023-paraphrasing
type: paper
title: Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense
authors:
- Kalpesh Krishna
- Yixiao Song
- Marzena Karpinska
- John Wieting
- Mohit Iyyer
year: 2023
venue: NeurIPS 2023
url: https://arxiv.org/abs/2303.13408
doi: null
arxiv: '2303.13408'
cite: Krishna, K., Song, Y., Karpinska, M., Wieting, J., & Iyyer, M. (2023). Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense. In Advances in Neural Information Processing Systems 36 (NeurIPS 2023). arXiv:2303.13408.
topics:
- swarm-detection
added_by: dmarz/sd-ai-content
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 650 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

Builds DIPPER, an 11B-parameter paraphraser with control over lexical diversity and reordering, and shows it evades watermarking, GPTZero, DetectGPT and OpenAI's classifier; DetectGPT accuracy falls from 70.3% to 4.6% at 1% false-positive rate. Proposes a retrieval defence run by the API provider: search a database of past generations for semantically similar text, which detects 80-97% of paraphrased generations at 1% false positives over 15M stored generations.

## Contribution

Quantified paraphrase evasion plus a provider-side retrieval defence that relies on logging rather than on text statistics.

## Key results

- Measured (abstract): DetectGPT accuracy 70.3% to 4.6% at 1% FPR after DIPPER paraphrasing.
- Measured (abstract): retrieval defence detects 80-97% of paraphrased generations with 1% of human text misclassified, using 15M generations.

## Methods and models

T5-XXL-based paraphraser fine-tuned for controllable paraphrase; detector evaluation; semantic retrieval over generation logs. Abstract read only.

## Limitations and open questions

Retrieval requires provider cooperation and does not cover open-weight models run locally. Abstract depth.

## Relevance to us

Evasion bar for content detectors, and the retrieval defence is a provider-side canary/log idea relevant to attribution. Attackers in the wild already paraphrase at scale ([[hao-2025-do]]).
