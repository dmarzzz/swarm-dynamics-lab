---
id: wortsman-2022-model
type: paper
title: "Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time"
authors: ["Mitchell Wortsman", "Gabriel Ilharco", "Samir Yitzhak Gadre", "Rebecca Roelofs", "Raphael Gontijo-Lopes", "Ari S. Morcos", "Hongseok Namkoong", "Ali Farhadi", "Yair Carmon", "Simon Kornblith", "et al."]
year: 2022
venue: "Proceedings of the 39th International Conference on Machine Learning (ICML), PMLR 162"
url: https://arxiv.org/abs/2203.05482
doi: null
arxiv: "2203.05482"
cite: "Wortsman, M., Ilharco, G., Gadre, S. Y., Roelofs, R., Gontijo-Lopes, R., Morcos, A. S., Namkoong, H., Farhadi, A., Carmon, Y., Kornblith, S., & Schmidt, L. (2022). Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time. In Proceedings of the 39th International Conference on Machine Learning, PMLR 162, 23965-23998. arXiv:2203.05482."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: null
code: []
---

## Summary

Shows that models fine-tuned from the same pre-trained checkpoint with different hyperparameters tend to lie in one low-error basin, so averaging their weights (a 'soup') often beats the best single model, at no extra inference cost. A greedy soup adds models one at a time only if held-out accuracy improves. A ViT-G soup reached 90.94% ImageNet top-1, a state of the art at the time. The authors relate weight averaging to logit ensembling via loss flatness and prediction confidence.

## Contribution

Establishes weight averaging of fine-tuned siblings as a practical merge operator, the 'merge back' step that later backdoor work attacks.

## Key results

- ViT-G model soup: 90.94% ImageNet top-1 (abstract).
- Soups improve out-of-distribution and zero-shot transfer over the best individual fine-tuned model (abstract).

## Methods and models

Fine-tune CLIP, ALIGN and ViT-G from a shared initialisation under a hyperparameter sweep, then uniform or greedy weight averaging. Code at github.com/mlfoundations/model-soups (not opened).

## Limitations and open questions

Abstract only. Requires shared initialisation; models from different pre-training runs do not average well. The greedy soup's held-out check is the only gate on what enters the merge.

## Relevance to us

Background for the fork-merge mechanism. Sutton-style splitting and recombining maps closely onto fine-tuning copies of one checkpoint and averaging them back; the shared-initialisation requirement is the same condition under which subliminal transfer works ([[cloud-2025-subliminal]]). The greedy soup's accept-only-if-held-out-improves rule is a simple merge gate worth testing against [[zhang-2024-badmerging]], which keeps clean accuracy unchanged and so would pass it. Related: [[ilharco-2023-editing]].
