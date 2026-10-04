---
id: katyal-2026-account
type: paper
title: Account-History Features for Social Bot Detection in the Era of Large Language Models
authors:
- Gaurang Katyal
year: 2026
venue: arXiv preprint
url: https://arxiv.org/abs/2606.26127
doi: null
arxiv: '2606.26127'
cite: 'Katyal, G. (2026). Account-History Features for Social Bot Detection in the Era of Large Language Models. arXiv preprint arXiv:2606.26127. Code: https://doi.org/10.5281/zenodo.20358445'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: full
relevance: 3
citations: null
code: []
---

## Summary

Asks how much bot detection survives if LLMs make post text indistinguishable from human text. On a 2,432-account labelled Twitter corpus (43% bots, 2017-2018), a random forest on 24 account-history features (age-normalised rates, follow ratios, profile completeness, handle structure) reaches ROC-AUC 0.977 versus 0.830 for 12 content features and 0.981 for both combined. Simulated text laundering lowers the content model but leaves the history model unchanged.

## Contribution

A clean single-author ablation that quantifies the common claim (for example [[ferrara-2023-social]]) that behavioural and metadata features, not text, carry LLM-era bot detection.

## Key results

- Behavioural-only RF ROC-AUC 0.977 versus content-only 0.830 (DeLong z = 9.36, p < 0.001); fusion 0.981.
- Rewriting bot tweets to match human URL, hashtag, mention and casing statistics drops content AUC from 0.842 to 0.785; behavioural AUC stays at 0.981.
- Replacing content features with draws from the human distribution (an upper bound on LLM laundering) drops content AUC to 0.466, below chance.
- Account age (Gini 0.141) and log friends (0.117) dominate; the first content feature ranks 13th.
- At threshold 0.5 the behavioural model has FPR 0.034 and FNR 0.118.

## Methods and models

Random forest (300 trees), logistic regression and gradient boosting; five-fold stratified CV; adversarial tests on a 70/30 split. Unlabelled 100-account TwiBot-20 sample used only for qualitative transfer.

## Limitations and open questions

No real LLM is used: the 'rewriting' is a mechanical edit of surface features, so the threat is simulated. Old (pre-paid-verification) data where 'verified' is a strong feature. The author notes that purchased aged accounts and sleeper bots defeat account-age features. Unreviewed preprint; small dataset of uncertain provenance. Given [[hays-2023-simplistic]], high in-sample AUC on one dataset is weak evidence.

## Relevance to us

Supports building swarm detectors on signals that are costly for an operator to fake (account age, follow graph, timing) rather than on output text. The aged-account loophole it names is exactly what a well-resourced agent swarm would buy; compare [[ezzeddine-2022-exposing]] and [[trokhymovych-2026-adversarial]].
