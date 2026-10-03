---
id: pacheco-2021-uncovering
type: paper
title: "Uncovering Coordinated Networks on Social Media: Methods and Case Studies"
authors: ["Diogo Pacheco", "Pik-Mai Hui", "Christopher Torres-Lugo", "Bao Tran Truong", "Alessandro Flammini", "Filippo Menczer"]
year: 2021
venue: "Proceedings of the International AAAI Conference on Web and Social Media (ICWSM)"
url: https://arxiv.org/html/2001.05658
doi: "10.1609/icwsm.v15i1.18075"
arxiv: "2001.05658"
cite: "Pacheco, D., Hui, P.-M., Torres-Lugo, C., Truong, B. T., Flammini, A., & Menczer, F. (2021). Uncovering Coordinated Networks on Social Media: Methods and Case Studies. Proceedings of the International AAAI Conference on Web and Social Media, 15, 455–466."
topics: [swarm-detection, sybil-resistance]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "244 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

Proposes a general unsupervised recipe for finding coordinated account groups: pick a behavioural trace that independent users are unlikely to share, build an account-feature bipartite network, project it to an account-account network weighted by co-occurrence, Jaccard or cosine similarity, filter weak edges, and take connected components as coordinated groups. Five Twitter case studies instantiate it with handle sharing, image colour histograms, hashtag sequences, co-retweets and 30-minute synchronized posting.

## Contribution

The template that most later coordination detectors follow. It frames coordination as "a surprising lack of independence" between accounts and shows that SynchroTrap and DeBot are special cases of the same projection scheme.

## Key results

- Handle sharing (Botometer logs, 1,545,892 accounts, Feb 2017 to Apr 2019): a 7,879-node handle-sharing network; reciprocal handle switches, indicating squatting or ransom, are 12 times more common in star-like components; the giant component has 722 accounts sharing 181 handles; one handle was taken by 23 accounts within 5 days.
- Images (Hong Kong protests, 2,945 accounts): keeping the top 1% of Jaccard edges finds three clusters totalling 315 accounts, one pro- and two anti-protest.
- Hashtag sequences (2018 US midterms, about 59 million accounts): 617 daily coordination instances by 1,809 accounts; the largest daily component (404 accounts) is the "Backfire Trump" app, part of a 1,175-account network over longer windows.
- Co-retweets (White Helmets, 11,669 accounts, top 0.5% cosine edges) separate pro- and anti-White Helmets clusters.
- Synchronized actions (crypto, 887,239 accounts, 30-minute bins, at least 8 tweets) surface pump-and-dump clusters, but precision is low because many coordinated clusters are unrelated spam.
- Coordinated accounts often have low bot scores: in two of three cases most coordinated accounts look human. The authors conclude bot detection is not sufficient to detect coordinated campaigns.

## Methods and models

Eight decision steps: conjecture, trace choice, feature engineering, support filter, bipartite weight (none or TF-IDF), projection similarity (co-occurrence, Jaccard, cosine), edge filter (top percentile), clustering (connected components; Louvain inside the giant component). Precision is estimated by manual annotation as a function of the support threshold. Code: github.com/IUNetSci/coordination-detection (not catalogued here).

## Limitations and open questions

Thresholds (top 1%, top 0.5%, 30-minute bins, minimum support) are tuned by hand; the authors propose Monte Carlo shuffling of the bipartite network as a future null model but do not implement it. The method says nothing about intent or automation, and benign coordination (activists, apps posting for users) is detected alongside malicious coordination. Validation is qualitative except for manual precision checks.

## Relevance to us

The baseline any agent-swarm detector has to beat or reuse. Its own example of a third-party app posting for many users (Backfire Trump) is the closest pre-LLM analogue of one operator driving many agents. Applied to agents by [[mukherjee-2026-moltgraph]] and used as the coordination metric in [[orlando-2026-emergent]]. Statistical tightening in [[pante-2025-beyond]]; review in [[mannocci-2026-detection]]. Earlier temporal special case: [[cao-2014-uncovering]].
