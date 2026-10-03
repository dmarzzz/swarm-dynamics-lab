---
id: bagdasaryan-2020-how
type: paper
title: "How To Backdoor Federated Learning"
authors: ["Eugene Bagdasaryan", "Andreas Veit", "Yiqing Hua", "Deborah Estrin", "Vitaly Shmatikov"]
year: 2020
venue: "Proceedings of the 23rd International Conference on Artificial Intelligence and Statistics (AISTATS), PMLR 108"
url: https://arxiv.org/html/1807.00459
doi: null
arxiv: "1807.00459"
cite: "Bagdasaryan, E., Veit, A., Hua, Y., Estrin, D., & Shmatikov, V. (2020). How To Backdoor Federated Learning. In Proceedings of the Twenty Third International Conference on Artificial Intelligence and Statistics, PMLR 108, 2938-2948. arXiv:1807.00459."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: full
relevance: 5
citations: "805 (OpenAlex search result, 2026-10-03)"
code: []
---

## Summary

The paper introduces model replacement, the first model-poisoning attack on federated averaging. One malicious participant trains a backdoored model locally, then scales its update by roughly n/eta (number of participants over global learning rate) so that after averaging the joint model is replaced by the attacker's model. Backdoors are semantic (green cars or racing-stripe cars classified as birds in CIFAR-10; a chosen word completing a trigger sentence in Reddit next-word prediction), so no input modification is needed at test time. Measured: a single-shot attack by one participant in one round drives backdoor accuracy to near 100% immediately, with no main-task loss, and the backdoor persists for many rounds when injected near convergence. A constrain-and-scale variant adds an anomaly-detection penalty to the attacker's loss so the update stays within what the aggregator would accept.

## Contribution

Defines model poisoning as distinct from data poisoning: a participant controls its whole local training process and can submit arbitrary weights, so one participant can replace the aggregate. It is the reference attack for 'one corrupted part merges back and rewrites the whole'.

## Key results

- Single-shot, single-participant attack: global model backdoor accuracy reaches close to 100% right after the poisoned round on both CIFAR-10 (100 participants, 10 per round) and Reddit word prediction (80,000 participants, 100 per round).
- CIFAR-10: an attacker controlling 1% of participants matches the backdoor accuracy of a data-poisoning attacker controlling 20%.
- Krum makes the attack easier: the attacker submits a backdoored model close to the global model and Krum selects it outright, because benign non-i.i.d. updates are widely scattered.
- Coordinate-wise median aggregation blocks replacement but costs main-task accuracy on non-i.i.d. word prediction even with no attack.
- Participant-level differential privacy (clipping plus noise) reduces the attack only at a matching cost in main-task accuracy; with 5% malicious participants out of 1,000 per round the backdoor still succeeds for several trigger sentences.
- Backdoors injected early in training are forgotten quickly; those injected after convergence persist, because benign updates then mostly cancel out.
- Measured in the paper: choosing a rare trigger and a common target word reduces the update norm needed (for example 'tastes delicious' 26.7 versus 'is palatable' 89.5).

## Methods and models

ResNet18 on CIFAR-10 with Dirichlet non-i.i.d. split; 2-layer LSTM (10M parameters) on one month of Reddit with 80,000 users. FedAvg with global learning rate eta; attacker scales its update by gamma = n/eta. Constrain-and-scale loss L = alpha L_class + (1-alpha) L_anomaly; train-and-scale for norm-bounded aggregators. Evaluated against secure aggregation, Krum, Multi-Krum, coordinate-wise median and participant-level DP.

## Limitations and open questions

Threat model assumes the attacker knows or can probe n and eta. Secure aggregation is argued to make detection impossible by construction. Byzantine-robust aggregators are dismissed partly on accuracy and privacy grounds rather than tested exhaustively. Later work ([[sun-2019-can]], [[shejwalkar-2022-back]]) reports that simple norm clipping defeats much of this in realistic settings, so the strength of the attack depends on the defence assumed.

## Relevance to us

Core prior art for Q3 and Q2. For Q3, model replacement is the parameter-space analogue of a sub-agent that returns and overwrites the parent: one returning part with full control of its own update can replace the merged result entirely if the merge is a plain average and the part knows the averaging weights. For Q2, it shows that averaging gives no k-of-n threshold at all (k = 1 suffices), and that Krum, a Byzantine-tolerant rule designed around an f-of-n bound, can be worse than averaging when honest parts are diverse, which is exactly the situation for sub-agents sent into different information domains. For Q1, secure aggregation hides which part contributed what, which the paper shows helps the attacker; hiding identities from the parent and hiding them from the attacker are different goals. Compare [[bhagoji-2019-analyzing]], [[fang-2020-local]], [[zhang-2024-badmerging]].
