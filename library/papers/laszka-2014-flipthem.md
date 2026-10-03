---
id: laszka-2014-flipthem
type: paper
title: 'FlipThem: Modeling Targeted Attacks with FlipIt for Multiple Resources'
authors:
- Aron Laszka
- Gabor Horvath
- Mark Felegyhazi
- Levente Buttyán
year: 2014
venue: Decision and Game Theory for Security (GameSec 2014), LNCS, 175-194
url: https://www.hit.bme.hu/~buttyan/publications/LaszkaHFB14gamesec.pdf
doi: 10.1007/978-3-319-12601-2_10
arxiv: null
cite: 'Laszka, A., Horvath, G., Felegyhazi, M., & Buttyán, L. (2014). FlipThem: Modeling Targeted Attacks with FlipIt for Multiple Resources. In Decision and Game Theory for Security (GameSec 2014), Lecture Notes in Computer Science (pp. 175-194). Springer.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: 58 (Crossref, 2026-10-03)
code: []
---

## Summary

Extends FlipIt ([[van-dijk-2013-flipit]]) to N resources with two control models: AND, where the attacker must hold all resources, and OR, where one suffices. Compares independent and synchronised combinations of single-resource strategies, and computes best-response Markov strategies with a linear program. I read the abstract, introduction, one results figure and the concluding remarks.

## Contribution

First multi-resource stealthy-takeover game; the bridge from FlipIt to threshold settings.

## Key results

- AND model: the defender should reset resources independently (not at the same time).
- OR model: the defender should reset synchronously.
- Periodic defender is good against non-adaptive attackers but poor against last-move attackers.
- Defender benefit is not smooth or monotone in flip rates, which makes optimisation hard (numerical).

## Methods and models

Renewal and Markov strategies, analytical gains, LP for best response, numerical comparisons.

## Limitations and open questions

Only full thresholds (all or one).

## Relevance to us

- Q2: a merge that requires agreement of all children is the AND model; a merge that accepts any one child is OR. The recommendation flips between them: stagger re-forks under AND, synchronise them under OR.
- Q1: staggered, independent resets also deny the attacker a single moment when all children are fresh and predictable.
Related: [[leslie-2015-threshold]], [[castro-1999-practical]].
