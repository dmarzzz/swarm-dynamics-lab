---
id: sinha-2018-stackelberg
type: paper
title: 'Stackelberg Security Games: Looking Beyond a Decade of Success'
authors:
- Arunesh Sinha
- Fei Fang
- Bo An
- Christopher Kiekintveld
- Milind Tambe
year: 2018
venue: Proceedings of the Twenty-Seventh International Joint Conference on Artificial Intelligence (IJCAI-18), 5494-5501
url: https://www.ijcai.org/proceedings/2018/0775.pdf
doi: null
arxiv: null
cite: 'Sinha, A., Fang, F., An, B., Kiekintveld, C., & Tambe, M. (2018). Stackelberg Security Games: Looking Beyond a Decade of Success. In Proceedings of the 27th International Joint Conference on Artificial Intelligence (IJCAI-18) (pp. 5494-5501).'
topics:
- fork-merge-security
- collective-decision
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

Survey of Stackelberg security games (SSG): basic model and Strong Stackelberg Equilibrium, deployed applications (ARMOR at LAX from 2007, IRIS for air marshals from 2009, PROTECT for the US Coast Guard, threat screening for TSA, green security games for wildlife), technical advances (scalability, bounded-rationality attacker models such as quantal response, robustness to parameter uncertainty, learning attacker models), SSG-inspired models (plan interdiction, coalitional security games against colluding attackers, patrolling, audit games) and open problems including deception and cyber settings with stealthy attacks. I read most of the paper; the future-applications section was skimmed.

## Contribution

Map of the SSG field circa 2018 and its pointers to multi-attacker and coalition variants.

## Key results

- Defender strategy spaces in recent applications exceed 10^33 (threat screening), attacker spaces 10^18 (road networks), as reported.
- Most deployed applications do not handle parameter uncertainty (stated as an open problem).
- Lists coalitional security games, which aim to prevent attacker coalitions from forming, and multiple-attacker extensions.

## Methods and models

Survey; no new results.

## Limitations and open questions

Pre-LLM; cyber section notes stealthy attacks that go unnoticed for months as a poorly modelled case.

## Relevance to us

- Q1: confirms that randomised commitment is the field's standard answer and that bounded-rationality attacker models are needed when the attacker does not best-respond, which may describe an LLM-driven attacker.
- Q2: coalitional security games are the existing formal home for preventing corrupted children from coordinating before a merge (not read in detail).
Related: [[tambe-2011-security]], [[blocki-2013-audit]], [[an-2012-security]].
