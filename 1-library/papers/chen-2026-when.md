---
id: chen-2026-when
type: paper
title: 'When Does Combining Language Models Help? A Co-Failure Ceiling on Routing, Voting, and Mixture-of-Agents Across 67 Frontier Models'
authors:
- Josef Chen
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.27288
doi: null
arxiv: '2606.27288'
cite: 'Chen, J. (2026). When Does Combining Language Models Help? A Co-Failure Ceiling on Routing, Voting, and Mixture-of-Agents Across 67 Frontier Models. arXiv preprint arXiv:2606.27288.'
topics:
- fork-merge-security
- llm-agent-swarms
- collective-decision
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Shows that any multi-model policy whose output is one member's answer (routing, voting, cascades, mixture-of-agents) has accuracy at most 1 - beta, where beta is the rate at which every model is wrong on the same query. Average pairwise error correlation rho cannot identify beta, since error laws with the same marginals and pairwise correlations can have different all-wrong rates. A Clopper-Pearson bound on beta certifies the largest possible gain before building a router. Across 67 models from 21 providers, a calibrated single-factor model underprices the all-wrong tail by about 2.5 times on open-ended maths (observed beta 0.052 versus 0.023).

## Contribution

Identifies the all-wrong rate beta, not pairwise correlation, as the quantity that caps ensemble gain, and gives a finite-sample certificate for it.

## Key results

- Proved (per abstract): accuracy <= 1 - beta for any select-one-member policy.
- Measured (per abstract): beta = 0.052 on open-ended maths versus 0.023 predicted (90 percent CI of underpricing 1.7 to 3.4, k = 17); beta = 0.079 on execution-graded code; GPQA-Diamond in free-response form gives beta = 0.127.
- Measured (per abstract): co-failure depends on answer format more than subject; combining models rarely beats the best single model on checkable tasks without a strong routing signal.

## Methods and models

Clopper-Pearson bounds, tetrachoric-calibrated single-factor and Gaussian-copula models, 67 models. Only the abstract was read.

## Limitations and open questions

Benign errors only; select-one-member policies only (not merges that synthesise new content).

## Relevance to us

Q2. The adversarial version of beta is the quantity that matters for fork-merge: the fraction of inputs on which every sub-agent is corrupted at once. If all explorers ingest the same poisoned page, beta for that input is near 1 and no k-of-n rule helps. The point that pairwise correlation underestimates the all-fail tail suggests measuring joint corruption directly in any experiment, not pairwise. Related: [[li-2026-state]], [[kim-2025-correlated]].
