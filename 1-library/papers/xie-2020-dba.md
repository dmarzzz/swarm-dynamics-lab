---
id: xie-2020-dba
type: paper
title: "DBA: Distributed Backdoor Attacks against Federated Learning"
authors: ["Chulin Xie", "Keli Huang", "Pin-Yu Chen", "Bo Li"]
year: 2020
venue: "International Conference on Learning Representations (ICLR 2020)"
url: https://openreview.net/forum?id=rkgyS0VFvr
doi: null
arxiv: null
cite: "Xie, C., Huang, K., Chen, P.-Y., & Li, B. (2020). DBA: Distributed Backdoor Attacks against Federated Learning. In International Conference on Learning Representations (ICLR 2020). https://openreview.net/forum?id=rkgyS0VFvr"
topics: [fork-merge-security]
added_by: shadow/sol-fm
accessed: 2026-10-04
read_depth: abstract
relevance: 5
citations: 259  # OpenAlex cited_by_count, 2026-10-04; shadow/sol-fm
code: []
---

## Summary

Proposes the distributed backdoor attack (DBA) against federated learning: instead of every malicious party embedding the same global trigger, DBA decomposes one global trigger pattern into separate local sub-patterns and gives each colluding party a different piece. No single party ever trains on the full trigger, yet the aggregated global model responds to the assembled global trigger at test time. The authors report that DBA is substantially more persistent and stealthy than centralized backdoors across image and finance datasets, reaches a significantly higher attack success rate under varied settings, and evades two robust-FL defences built to stop centralized backdoors. They sweep local trigger variations (size, gap, location), the FL scaling factor, data distribution and poison ratio.

## Contribution

The canonical split-payload attack on an aggregation step: an attack that each contributing part carries only a fragment of, so that per-part inspection sees nothing malicious and only the merged model exhibits the behaviour. It is the federated-learning instance of the fork-merge Q2 case (corrupted parts share one adversarial objective divided among them).

## Key results

- DBA attack success rate is reported significantly higher than centralized (same-trigger) backdoors across datasets and settings (exact per-setting ASR in the paper body, read at abstract depth here).
- DBA evades two state-of-the-art robust FL algorithms that were designed against centralized backdoors.
- DBA is more persistent (backdoor survives more rounds of honest training) and more stealthy than the centralized baseline.
- Attack behaviour characterized across local trigger size/gap/location, scaling factor, data distribution, poison ratio and interval.

## Methods and models

Federated learning with several adversarial parties; global trigger decomposed into disjoint local triggers, one per colluding party. Image datasets (e.g. CIFAR, MNIST-family) and a finance dataset (LOAN). Feature visual interpretation and feature-importance ranking used to explain effectiveness. Code exists at github.com/AI-secure/DBA (not opened this session).

## Limitations and open questions

Abstract-depth read: the specific ASR numbers, the two defences defeated, and the number of colluding parties needed are in the body and should be confirmed before any are quoted. The attack is on weight/gradient aggregation in FL, not on an LLM agent merge; whether the split-trigger idea transfers to merging text reports or memories is untested.

## Relevance to us

Directly load-bearing for Q2 (thresholds) and Q3 (attack vector). It is the clearest published measurement that a k-of-n attack with a *shared, divided* adversarial objective defeats per-part defences, which is exactly the fork-merge case where sibling forks share one corrupting input. Named as a known gap in the fork-merge survey and in issue #75 (OpenReview had blocked automated access during the original lane). Related: [[bagdasaryan-2020-how]], [[lyu-2023-poisoning]], [[wang-2025-from]], [[li-2026-when]], [[ding-2026-colluding]], [[hu-2026-when]], [[fang-2020-local]].
