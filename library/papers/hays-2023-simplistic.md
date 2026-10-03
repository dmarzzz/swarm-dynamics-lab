---
id: hays-2023-simplistic
type: paper
title: Simplistic Collection and Labeling Practices Limit the Utility of Benchmark Datasets for Twitter Bot Detection
authors:
- Chris Hays
- Zachary Schutzman
- Manish Raghavan
- Erin Walk
- Philipp Zimmer
year: 2023
venue: Proceedings of the ACM Web Conference 2023 (WWW '23)
url: https://arxiv.org/abs/2301.07015
doi: 10.1145/3543507.3583214
arxiv: '2301.07015'
cite: Hays, C., Schutzman, Z., Raghavan, M., Walk, E., & Zimmer, P. (2023). Simplistic Collection and Labeling Practices Limit the Utility of Benchmark Datasets for Twitter Bot Detection. In Proceedings of the ACM Web Conference 2023 (WWW '23), pp. 3660-3669. https://doi.org/10.1145/3543507.3583214
topics:
- swarm-detection
added_by: dmarz/sd-bots
accessed: '2026-10-03'
read_depth: full
relevance: 5
citations: 26 (Crossref, 2026-10-03)
code: []
---

## Summary

The authors show that the public Twitter bot benchmarks are nearly solved by shallow decision trees on one to four features, and that classifiers trained on one dataset (or on all but one) perform near chance on the held-out dataset. They trace the easy separability to how each dataset was collected and labelled, not to real differences between bots and humans; for example, every human in cresci-2017 tweeted the word 'earthquake' because they came from a disaster-sensing project.

## Contribution

A dataset-level explanation for why published bot detectors look near-perfect in-sample and fail in deployment. Best paper at WWW 2023.

## Key results

- Shallow trees came within 5 points of state-of-the-art accuracy on most of 11 benchmark datasets (for example 0.98 accuracy on cresci-2017 and cresci-2015, 0.82 on twibot-2020 using only the 'verified' flag at depth one).
- Random forests trained on one dataset and tested on another mostly scored balanced accuracy 0.4-0.6 off the diagonal (Table 3).
- Leave-one-dataset-out: out-of-sample balanced accuracy was 0.52-0.57 for most held-out sets, versus 0.71-0.84 in-sample (Table 4); exceptions share data or labelling procedures with the training sets.
- Within a bot type (for example spammers), a shallow tree identifies which dataset an account came from with balanced accuracy 0.75 against a naive baseline under 0.15, so more datasets of the same kind will not add coverage.
- Humans: a classifier tells which of six human datasets an account came from with balanced accuracy above 0.4 (chance under 0.17).

## Methods and models

scikit-learn decision trees of depth 1-4 and 100-tree random forests; five-fold CV; cross-dataset and leave-one-out tests on a common feature set (followers, following, tweets, lists). Datasets: twibot-2020, feedback-2019, rtbust-2019, pan-2019, midterm-2018, stock-2018, cresci-2017, gilani-2017, cresci-2015, yang-2013, caverlee-2011 (the last collected with honeypot accounts).

## Limitations and open questions

Treats the original labels as ground truth even while questioning them. Profile features only for cross-dataset tests, so text or graph features might transfer better (the authors argue this is implausible). Pre-LLM data; says nothing about LLM-driven bots directly.

## Relevance to us

A warning for any benchmark of LLM-agent swarms we build: if a one-feature rule separates our agents from our humans, we have measured our sampling, not detectability. Their recipe (shallow-tree audit plus leave-one-dataset-out) is a cheap sanity check for synthetic-swarm datasets such as [[qiao-2024-botsim]]. Datasets audited include [[data-cresci-2017]]; see also [[echeverria-2018-lobo]] and [[gallwitz-2022-investigating]].
