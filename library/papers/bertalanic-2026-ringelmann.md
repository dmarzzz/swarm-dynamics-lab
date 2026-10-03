---
id: bertalanic-2026-ringelmann
type: paper
title: 'The Ringelmann Effect in Multi-Agent LLM Systems: A Scaling Law for Effective Team Size'
authors:
- Blaž Bertalanič
- Carolina Fortuna
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.02646
doi: null
arxiv: '2606.02646'
cite: 'Bertalanič, B., & Fortuna, C. (2026). The Ringelmann Effect in Multi-Agent LLM Systems: A Scaling Law for Effective Team Size. arXiv preprint arXiv:2606.02646.'
topics:
- llm-agent-swarms
- criticality-measurement
added_by: dmarz/llm-agent-swarms-recent
accessed: '2026-10-03'
read_depth: abstract
relevance: 5
citations: 0 (OpenAlex, 2026-10-03); 5 (Semantic Scholar, 2026-10-03)
code: []
---

## Summary

The authors argue that counting nominal agents conflates cost with independent evidence, and fit an effective-team-size law R(N) = N_eff/N = 1/(1 + c(N - 1)N^{-beta}). The exponent beta sorts any configuration into a hard ceiling at 1/c (beta = 0), a sublinear regime N^beta/c (0 < beta < 1) or linear growth (beta >= 1). A mean-field argument predicts that in debate the peer count k and the number of rounds tau enter only through their product k tau. Across 44 model x task x condition cells (peer debate, self-correction, a random-noise placebo, self-consistency; Qwen, Llama and Ministral at 7B-32B, a Gemini check, thinking models, heterogeneous teams, sparse communication) the form fits every cell with R^2 > 0.99. Thirty dense debating agents give no more answer diversity than one on MMLU-Hard; a noise placebo tracks self-correction, so gains attributed to debate come from re-evaluation rather than peer content; only heterogeneous teams escape the hard ceiling.

## Contribution

Supplies a two-parameter, testable scaling law for redundancy in LLM teams, named after the Ringelmann (social loafing) effect in human groups, and a placebo control that separates peer influence from re-sampling. Complements [[kim-2025-towards]] (coordination overhead) and [[yang-2026-understanding]] (diversity and effective channels), and directly contests the logistic "collaborative scaling law" of [[qian-2025-scaling]].

## Key results

- Claimed: R(N) form fits all 44 cells at R^2 > 0.99; only (c, beta) shift.
- Claimed: dense peer influence collapses answer-level scaling on free-form math from sublinear to hard-ceiling; correctness-level fits are hard-ceiling throughout.
- Claimed: 30 dense debating agents produce no more answer diversity than one on MMLU-Hard.
- Claimed: a single N <= 5 pilot predicts the N = 30 ceiling; communication-mode interventions do not lower c, architectural diversity does.

## Methods and models

Inference-time teams of up to 30 agents with debate, self-correction, self-consistency and a noise placebo; open-weight Qwen, Llama, Ministral (7B-32B), a Gemini API check, thinking models; fits at answer-diversity and correctness-redundancy levels. Details beyond abstract not checked.

## Limitations and open questions

Abstract-level read. The law is phenomenological; fitted R^2 near 1 over N <= 30 does not establish asymptotics. Tasks are QA/math, not embodied or spatial.

## Relevance to us

Gives a falsifiable baseline for any "swarm scaling" claim we make: report N_eff, not N. The k tau product prediction is a mean-field result we could test on SwarmBench-style tasks. Related: [[fortuna-2026-multi-agent]] (same group), [[li-2024-more]], [[chen-2024-are]], [[zhang-2025-stop]].
