---
id: goel-2025-great
type: paper
title: Great Models Think Alike and this Undermines AI Oversight
authors:
- Shashwat Goel
- Joschka Struber
- Ilze Amanda Auzina
- Karuna K Chandra
- Ponnurangam Kumaraguru
- Douwe Kiela
- Ameya Prabhu
- Matthias Bethge
- Jonas Geiping
year: 2025
venue: arXiv preprint
url: https://arxiv.org/abs/2502.04313
doi: null
arxiv: '2502.04313'
cite: 'Goel, S., Struber, J., Auzina, I. A., Chandra, K. K., Kumaraguru, P., Kiela, D., Prabhu, A., Bethge, M., & Geiping, J. (2025). Great Models Think Alike and this Undermines AI Oversight. arXiv preprint arXiv:2502.04313.'
topics:
- fork-merge-security
- llm-agent-swarms
added_by: dmarz/fm-bft-aggregation
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 3  # OpenAlex cited_by_count, 2026-10-03; shadow/sol-g51
code: []
---

## Summary

Proposes Chance Adjusted Probabilistic Agreement (CAPA), a model-similarity metric based on overlap in mistakes that corrects for accuracy and uses output probabilities. With CAPA the authors report that LLM-as-judge scores favour models similar to the judge, that weak-to-strong training gains depend on complementary knowledge between supervisor and student, and that model mistakes become more similar as capability increases. The abstract frames this as a risk of correlated failures in AI oversight.

## Contribution

A chance-adjusted error-similarity metric for LMs, and evidence (per the abstract) that similarity grows with capability, which [[kim-2025-correlated]] reproduces independently.

## Key results

- Reported in abstract: judge scores favour models similar to the judge, generalising self-preference.
- Reported in abstract: model mistakes become more similar with increasing capability.
- Numbers not checked: only the arXiv abstract page was opened.

## Methods and models

CAPA metric over multiple-choice outputs with probabilities; LLM-as-judge and weak-to-strong experiments. Details not read.

## Limitations and open questions

Only the abstract was read. Natural errors only, no adversarial setting.

## Relevance to us

Q2. If the parent uses one sub-agent or a sibling model to check another before merge, CAPA-style similarity is the quantity that decides whether the check is independent. The trend that stronger models err alike means a k-of-n threshold over capable sub-agents degrades toward 1-of-n against inputs that exploit a shared blind spot. See [[kim-2025-correlated]] and [[knight-1986-experimental]].
