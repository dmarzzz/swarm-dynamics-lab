---
id: bhagoji-2019-analyzing
type: paper
title: "Analyzing Federated Learning through an Adversarial Lens"
authors: ["Arjun Nitin Bhagoji", "Supriyo Chakraborty", "Prateek Mittal", "Seraphin Calo"]
year: 2019
venue: "Proceedings of the 36th International Conference on Machine Learning (ICML), PMLR 97"
url: https://arxiv.org/abs/1811.12470
doi: null
arxiv: "1811.12470"
cite: "Bhagoji, A. N., Chakraborty, S., Mittal, P., & Calo, S. (2019). Analyzing Federated Learning through an Adversarial Lens. In Proceedings of the 36th International Conference on Machine Learning, PMLR 97, 634-643. arXiv:1811.12470."
topics: [fork-merge-security]
added_by: dmarz/fm-merge-poisoning
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: null
code: []
---

## Summary

Studies targeted model poisoning in federated learning by a single, non-colluding malicious agent whose goal is to make the global model misclassify chosen inputs with high confidence. The attacker first boosts (explicitly scales) its update to overcome benign updates, then adds stealth by alternating minimisation between the training loss and the adversarial objective, and finally estimates benign agents' updates to improve success. Interpretability explanations of the poisoned and benign models were reported as nearly indistinguishable.

## Contribution

Independent early demonstration, alongside [[bagdasaryan-2020-how]], that a single participant can steer the aggregate, and the first to frame stealth (looking like a normal update) as an explicit optimisation target.

## Key results

- Abstract-level claim: a single highly constrained adversary achieves targeted misclassification while maintaining stealth against accuracy and weight-distance checks.
- Explanation maps (interpretability) of malicious and benign models are reported as visually nearly identical, so inspection of explanations does not reveal the poisoning.
- Bagdasaryan et al. note that the boosted variant needs the attacker in every round to avoid the backdoor being forgotten (stated in [[bagdasaryan-2020-how]], not checked here).

## Methods and models

Explicit boosting of the malicious update, alternating minimisation for stealth, estimation of benign updates. Experiments on image and tabular classifiers with a small number of agents (details not read). Code: github.com/inspire-group/ModelPoisoning (not opened).

## Limitations and open questions

Only the abstract was read. The single-agent, targeted-misclassification setting is narrower than semantic backdoors. Persistence across rounds is weaker than model replacement according to [[bagdasaryan-2020-how]].

## Relevance to us

Bears on Q3 (what the corrupting part does) and on detection for Q2: the attack is designed to make the returning update statistically and explanatorily normal, which is the property a merge-time filter would need to break. For a fork-merge agent this means checking the returning part's behaviour on the parent's own probes is not enough if the part optimised against those probes. Related: [[bagdasaryan-2020-how]], [[fang-2020-local]].
