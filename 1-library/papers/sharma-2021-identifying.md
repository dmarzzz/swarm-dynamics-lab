---
id: sharma-2021-identifying
type: paper
title: "Identifying Coordinated Accounts on Social Media through Hidden Influence and Group Behaviours"
authors: ["Karishma Sharma", "Yizhou Zhang", "Emilio Ferrara", "Yan Liu"]
year: 2021
venue: "Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD)"
url: https://arxiv.org/abs/2008.11308
doi: "10.1145/3447548.3467391"
arxiv: "2008.11308"
cite: "Sharma, K., Zhang, Y., Ferrara, E., & Liu, Y. (2021). Identifying Coordinated Accounts on Social Media through Hidden Influence and Group Behaviours. In Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining (pp. 1441–1451). ACM."
topics: [swarm-detection]
added_by: dmarz/sd-coordination
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "115 (Semantic Scholar, 2026-10-03)"
code: []
---
## Summary

AMDN-HAGE jointly models account activity sequences as a temporal point process (attentive mixture density network) and hidden account groups as a Gaussian mixture, on the premise that coordinating accounts strongly influence each other's activity timing and jointly look anomalous. Trained by bilevel optimisation with a convergence guarantee, it is tested on Russia's Internet Research Agency campaign around the 2016 US election and on COVID-19 discourse, where it finds groups pushing anti-vaccine and anti-mask conspiracies.

## Contribution

Treats coordination as hidden coupling between accounts' event timing, learned without labels, instead of thresholded co-activity. This is the closest social-media analogue of inferring interaction structure from trajectories.

## Key results

- Average learned influence is highest between coordinated account pairs (abstract).
- Detects IRA accounts without requiring a revealed subset of them, unlike earlier semi-supervised methods (abstract claim; numbers not in abstract).

## Methods and models

Neural temporal point process with attention over each account's history, mixture model over account embeddings, bilevel optimisation. Data: IRA Twitter release and COVID-19 tweets.

## Limitations and open questions

Abstract only. Point-process models need enough events per account; sparse agents may evade. Influence learned from timing can confound common exposure (two accounts reacting to the same news) with coupling.

## Relevance to us

The principled timing-based detector for hidden coupling; candidates for agent swarms that share a scheduler. Compare with physics-style interaction inference in [[lu-2019-nonparametric]] and [[lord-2016-inference]].
