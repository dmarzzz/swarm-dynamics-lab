---
id: cho-2020-toward
type: paper
title: 'Toward Proactive, Adaptive Defense: A Survey on Moving Target Defense'
authors: [Jin-Hee Cho, Dilli P. Sharma, Hooman Alavizadeh, Seunghyun Yoon, Noam Ben-Asher, Terrence J. Moore, Dong Seong Kim, Hyuk Lim, Frederica F. Nelson]
year: 2020
venue: IEEE Communications Surveys & Tutorials
url: https://arxiv.org/abs/1909.08092
doi: 10.1109/comst.2019.2963791
arxiv: '1909.08092'
cite: 'Cho, J.-H., Sharma, D. P., Alavizadeh, H., Yoon, S., Ben-Asher, N., Moore, T. J., Kim, D. S., Lim, H., & Nelson, F. F. (2020). Toward Proactive, Adaptive Defense: A Survey on Moving Target Defense. IEEE Communications Surveys & Tutorials, 22(1), 709-745.'
topics: [fork-merge-security]
added_by: dmarz/fm-unlinkability
accessed: 2026-10-03
read_depth: skim
relevance: 3
citations: 353 (OpenAlex, 2026-10-03)
code: []
---

## Summary

A survey of moving target defense (MTD): defences that change a system's attack surface over time so that an attacker's reconnaissance goes stale. It covers key roles, design principles, classifications, common attacks, methodologies, algorithms, metrics, evaluation methods and application domains. Its main classification is operation-based: shuffling (rearranging configurations, addresses, placements), diversity (multiple implementations of a function) and redundancy (replicas), traced back to n-version programming. Lessons include that MTD must balance security against overhead and service disruption, that game theory dominates strategy design, and that most evaluations are simulations or analytical models rather than testbeds.

## Contribution

A broad map of MTD with the shuffling-diversity-redundancy classification and a catalogue of metrics and evaluation methods.

## Key results

- Classification of MTD into shuffling, diversity and redundancy; authors note this captures how to move but not when or what to move.
- Game-theoretic models are the dominant strategy-generation method; genetic algorithms and ML also used.
- Most MTD validation is by simulation or analytical modelling; few real testbeds.
- Overhead and disruption to legitimate users are the main costs and are under-measured.

## Methods and models

Literature survey; I read the abstract, classification sections and the insights and future-directions section.

## Limitations and open questions

Survey of mainly network and system MTD; no treatment of AI agents. Authors call for adaptive MTD and better classification.

## Relevance to us

Q1, and partly Q2. Shuffling is "keep changing which sub-agent is the merge candidate" so reconnaissance on the current candidate is stale by merge time; diversity is "send sub-agents with different models or prompts so one exploit does not transfer to all"; redundancy is "send several and compare on return", which is where MTD meets thresholds (Q2). The survey's caution that shuffling has costs and that most claims are simulated applies directly, and [[wright-2004-predecessor]] shows shuffling can also leak over rounds. Companion survey: [[sengupta-2020-survey]]; game-theoretic placement: [[pawlick-2019-game]].
