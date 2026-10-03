---
id: varol-2017-online
type: paper
title: 'Online Human-Bot Interactions: Detection, Estimation, and Characterization'
authors:
- Onur Varol
- Emilio Ferrara
- Clayton A. Davis
- Filippo Menczer
- Alessandro Flammini
year: 2017
venue: Proceedings of the International AAAI Conference on Web and Social Media (ICWSM 2017)
url: https://arxiv.org/abs/1703.03107
doi: 10.1609/icwsm.v11i1.14871
arxiv: '1703.03107'
cite: 'Varol, O., Ferrara, E., Davis, C. A., Menczer, F., & Flammini, A. (2017). Online Human-Bot Interactions: Detection, Estimation, and Characterization. Proceedings of the International AAAI Conference on Web and Social Media, 11(1), 280-289. https://doi.org/10.1609/icwsm.v11i1.14871'
topics:
- swarm-detection
- sybil-resistance
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 570 (Crossref, 2026-10-03)
code: []
---

## Summary

The paper behind Botometer's early versions: a supervised classifier using more than a thousand profile, friend, content, sentiment, network and timing features, trained on a public bot dataset enriched with manually annotated active accounts. Applying it, the authors estimate that 9% to 15% of active Twitter accounts were bots in 2017 and describe how simple bots interact with more human-like bots and how bots target groups through retweets and mentions.

## Contribution

The origin of the widely quoted '9-15% of Twitter accounts are bots' figure, and the reference design for feature-rich per-account bot classifiers.

## Key results

- Estimated 9%-15% of active Twitter accounts are bots (abstract).
- More than 1,000 features across user metadata, friends, content, sentiment, network and temporal patterns.
- Simple bots tend to interact with more human-like bots; clustering reveals subclasses such as spammers, self-promoters and app-connected accounts.

## Methods and models

Random-forest style supervised classification (BotOrNot/Botometer lineage) on a public honeypot-derived dataset plus manual annotations; prevalence via classifier thresholding on a sample of active users. Abstract-level read.

## Limitations and open questions

The prevalence figure depends on a threshold and on training labels, which [[gallwitz-2022-investigating]] and [[hays-2023-simplistic]] show to be fragile; [[varol-2022-should]] later discusses how assumptions drive such estimates.

## Relevance to us

The canonical base-rate claim to check any new agent-prevalence figure against, and an example of why a classifier-based prevalence needs a calibration set. Validation critiques: [[rauchfleisch-2020-false]]. Successor system: [[sayyadiharikandeh-2020-detection]].
