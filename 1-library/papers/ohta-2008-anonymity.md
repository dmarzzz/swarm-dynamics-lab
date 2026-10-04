---
id: ohta-2008-anonymity
type: paper
title: 'Anonymity-proof Shapley value: extending shapley value for coalitional games in open environments'
authors:
- 'Naoki Ohta'
- 'Vincent Conitzer'
- 'Yasufumi Satoh'
- 'Atsushi Iwasaki'
- 'Makoto Yokoo'
year: 2008
venue: 'Proceedings of the 7th International Joint Conference on Autonomous Agents and Multiagent Systems (AAMAS 2008)'
url: https://api.openalex.org/works/doi:10.5555/1402298.1402352
doi: null
arxiv: null
cite: 'Ohta, N., Conitzer, V., Satoh, Y., Iwasaki, A., & Yokoo, M. (2008). Anonymity-proof Shapley value: extending Shapley value for coalitional games in open environments. In Proceedings of the 7th International Joint Conference on Autonomous Agents and Multiagent Systems (AAMAS 2008), 927-934.'
topics:
- sybil-resistance
- collective-decision
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 'OpenAlex 2026-10-03: 26'
code: []
---

## Summary

Traditional coalitional solution concepts such as the Shapley value can be manipulated in open anonymous environments, where agents can split into several identities or hide resources. Earlier work defined the anonymity-proof core, which resists these manipulations but is costly to compute and represent. This paper defines the anonymity-proof Shapley value, shows it is characterised by simple axioms, always exists and is unique, and is drastically cheaper to compute and represent than earlier anonymity-proof concepts.

## Contribution

A Sybil-resistant analogue of the Shapley value for dividing coalition gains among agents whose identities are not verified.

## Key results

- The anonymity-proof Shapley value is characterised by axioms, always exists and is uniquely determined.
- Its computational and representational costs are much smaller than those of the anonymity-proof core.

## Methods and models

Coalitional games defined over resources rather than agents, with agents able to split resources across identifiers or hide them (setting described in [[conitzer-2010-using]]).

## Limitations and open questions

Abstract-level read. The DOI-style ACM identifier is not registered with Crossref, so the url points to the OpenAlex record I opened.

## Relevance to us

Credit assignment among LLM agents, tools or retrieved documents by Shapley value is common; this is the known fix for its Sybil vulnerability. Compare the equal-split behaviour noted in [[patel-2025-maxshapley]] and the cost-sharing results in [[mazorra-2023-optimality]].
