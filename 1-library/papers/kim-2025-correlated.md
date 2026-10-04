---
id: kim-2025-correlated
type: paper
title: Correlated Errors in Large Language Models
authors:
- Elliot Kim
- Avi Garg
- Kenny Peng
- Nikhil Garg
year: 2025
venue: arXiv preprint
url: https://arxiv.org/html/2506.07962
doi: null
arxiv: '2506.07962'
cite: 'Kim, E., Garg, A., Peng, K., & Garg, N. (2025). Correlated Errors in Large Language Models. arXiv preprint arXiv:2506.07962.'
topics:
- fork-merge-security
- llm-agent-swarms
- collective-decision
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 3  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

Measures how often different LLMs make the same mistake. Using answers from 349 models on 12,032 MMLU questions (HuggingFace Open LLM Leaderboard), 71 models on 14,042 questions (HELM), and 20 models scoring 1,800 resume-job pairs, the authors compute agreement conditional on both models being wrong. Mean agreement-when-both-wrong is 0.423 on HuggingFace and 0.60 on HELM, about double the random baselines (0.127 and 1/3). Nearly all pairs exceed the baseline (100 percent on HuggingFace, 97.5 percent on HELM). Same provider, same base architecture and similar size predict more agreement, and, after controlling for those, more accurate models have more correlated errors.

## Contribution

The first large-scale measurement of LLM error correlation across hundreds of models, with a regression of its drivers. It is the LLM-era counterpart of the Knight-Leveson test [[knight-1986-experimental]].

## Key results

- Measured: mean agreement when both wrong 0.423 (HuggingFace) and 0.60 (HELM) versus random 0.127 and 0.333.
- Measured: example pairs reach 0.97 (Llama 3.2 90B vision vs Llama 3.1 70B) and 0.9987 (google/text-unicorn@001 vs writer/palmyra-x-v3, no public relation).
- Measured regression (HuggingFace): same company +0.066, same architecture +0.076, accuracy interaction +0.023 per SD; features explain 34 to 62 percent of variance across datasets.
- Measured: an LLM judge inflates the accuracy of less accurate models, more so for same-provider models, because shared wrong answers are scored as correct.
- Measured: in a simulated hiring market where each firm uses a random LLM, about 20 percent of applicants stay excluded from every firm even with 20 firms, versus near zero for independent random preferences.

## Methods and models

Agreement rate on multiple-choice questions conditional on both answers wrong; residual correlation against 450 hand labels for resumes; OLS on pair features. Stable matching simulations with 60 applicants and 30 firms over 1500 random markets. Code at github.com/nikhgarg/llm_correlated_errors_public (not opened).

## Limitations and open questions

Multiple-choice and numeric scoring only; open-ended generation not measured. All wrong answers treated as equivalent. No adversarial setting: these are natural errors, so they bound from below how correlated failures become when an attacker deliberately feeds the same content to every model.

## Relevance to us

Q2. A k-of-n merge threshold over LLM sub-agents assumes failures are roughly independent. This paper measures that they are not, even across providers, and that correlation rises with capability. For a parent that forks copies of itself (same weights) the correlation is at the high end of these numbers before any attack. Pairs with [[goel-2025-great]] (same finding with a chance-adjusted metric), [[nogueira-2026-systematic]] and [[ron-2026-n-version]] (code), and [[bara-2026-epistemic]] (multiplying agents without multiplying evidence). It also explains why the evaluator diversity in [[jo-2025-byzantine]] and [[lee-2026-robust]] buys less than the honest-majority count suggests.
