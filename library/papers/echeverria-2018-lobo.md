---
id: echeverria-2018-lobo
type: paper
title: LOBO -- Evaluation of Generalization Deficiencies in Twitter Bot Classifiers
authors:
- Juan Echeverría
- Emiliano De Cristofaro
- Nicolas Kourtellis
- Ilias Leontiadis
- Gianluca Stringhini
- Shi Zhou
year: 2018
venue: Proceedings of the 34th Annual Computer Security Applications Conference (ACSAC 2018)
url: https://arxiv.org/abs/1809.09684
doi: 10.1145/3274694.3274738
arxiv: '1809.09684'
cite: 'Echeverría, J., De Cristofaro, E., Kourtellis, N., Leontiadis, I., Stringhini, G., & Zhou, S. (2018). LOBO: Evaluation of Generalization Deficiencies in Twitter Bot Classifiers. In Proceedings of the 34th Annual Computer Security Applications Conference (ACSAC ''18), pp. 137-146. https://doi.org/10.1145/3274694.3274738'
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 53 (Crossref, 2026-10-03)
code: []
---

## Summary

Proposes leave-one-botnet-out evaluation: train a bot classifier on all bot classes but one and test on the unseen class. A classifier trained on more than 200,000 accounts reached over 97% accuracy in standard testing but generalised poorly to held-out bot classes, so results from single-dataset evaluation overstate real-world performance.

## Contribution

Introduced the evaluation protocol that later work ([[hays-2023-simplistic]]) used to show benchmark overfitting.

## Key results

- Over 97% accuracy in-distribution with about 200K training points (abstract).
- Poor generalisation to unseen bot classes under the LOBO protocol.

## Methods and models

Leave-one-botnet-out cross-validation over several bot collections. Abstract-level read.

## Limitations and open questions

Pre-LLM; the bot classes are older Twitter botnets.

## Relevance to us

Any swarm detector should be evaluated leave-one-operator-out: a new operator or new model is an unseen class. See [[sayyadiharikandeh-2020-detection]] for a response.
