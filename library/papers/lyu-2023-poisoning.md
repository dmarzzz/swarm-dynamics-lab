---
id: lyu-2023-poisoning
type: paper
title: "Poisoning with Cerberus: Stealthy and Colluded Backdoor Attack against Federated Learning"
authors: ["Xiaoting Lyu", "Yufei Han", "Wei Wang", "Jingkai Liu", "Bin Wang", "Jiqiang Liu", "Xiangliang Zhang"]
year: 2023
venue: "Proceedings of the AAAI Conference on Artificial Intelligence, 37(7)"
url: https://ojs.aaai.org/index.php/AAAI/article/view/26083
doi: "10.1609/aaai.v37i7.26083"
arxiv: null
cite: "Lyu, X., Han, Y., Wang, W., Liu, J., Wang, B., Liu, J., & Zhang, X. (2023). Poisoning with Cerberus: Stealthy and Colluded Backdoor Attack against Federated Learning. Proceedings of the AAAI Conference on Artificial Intelligence, 37(7), 9020-9028. https://doi.org/10.1609/aaai.v37i7.26083"
topics: [fork-merge-security]
added_by: shadow/sol-fm
accessed: 2026-10-04
read_depth: abstract
relevance: 4
citations: 99  # OpenAlex cited_by_count, 2026-10-04; shadow/sol-fm
code: []
---

## Summary

Cerberus Poisoning (CerP) is a distributed, colluded backdoor attack on federated learning. The malicious participants jointly tune the backdoor trigger and jointly control how much each poisoned local model deviates from a clean one, so that the trigger-induced bias of each poisoned local update is minimized. Keeping each colluding update close to the honest distribution is what makes the attack stealthy and lets it circumvent a wide range of robust-FL defences. Evaluated on 3 large-scale benchmark datasets against 13 mainstream defensive mechanisms, CerP is reported to succeed against all of them.

## Contribution

Shows that collusion is a tunable knob: by coordinating how far each malicious part strays from the honest aggregate, attackers can trade per-part conspicuousness for merged-model effect, defeating defences that flag outlier contributions. Complements DBA's trigger-splitting with update-magnitude coordination.

## Key results

- Evaluated on 3 benchmark datasets against 13 defensive mechanisms; reported to circumvent the full spectrum (per-defence numbers in the body, read at abstract depth here).
- Core mechanism: jointly minimize the deviation of each poisoned local model from the poison-free model while still delivering the backdoor, so robust aggregation cannot separate malicious from honest updates.

## Methods and models

Federated learning with multiple colluding participants; joint optimization over the shared trigger and per-participant model-change budget. Three large-scale image benchmarks; thirteen robust-FL defences as baselines.

## Limitations and open questions

Abstract depth: the 13 defences, the datasets and the ASR values need the body before being quoted. Like DBA it operates on weight aggregation, not on text or memory merges.

## Relevance to us

Second measured case for Q2 that collusion defeats per-part robust aggregation, strengthening the fork-merge claim that sibling forks sharing one adversarial objective are not independent principals. The "keep each part near the honest mean" idea is the FL analogue of the split-payload-stays-under-threshold attacks on model merging. Related: [[xie-2020-dba]], [[bagdasaryan-2020-how]], [[baruch-2019-little]], [[wang-2025-from]], [[ding-2026-colluding]].
