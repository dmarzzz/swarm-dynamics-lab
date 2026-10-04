---
id: todo-2013-false
type: paper
title: 'False-name-proof matching'
authors:
- 'Taiki Todo'
- 'Vincent Conitzer'
year: 2013
venue: 'Proceedings of the 12th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2013)'
url: https://api.openalex.org/works/doi:10.5555/2484920.2484971
doi: null
arxiv: null
cite: 'Todo, T., & Conitzer, V. (2013). False-name-proof matching. In Proceedings of the 12th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2013), 311-318.'
topics:
- sybil-resistance
added_by: dmarz/sybil-mechanisms
accessed: 2026-10-03
read_depth: abstract
relevance: 3
citations: 'OpenAlex 2026-10-03: 18'
code: []
---

## Summary

In priority-based matching, objects rank agents, but in anonymous environments the set of agents is unknown and objects should rank characteristics (such as GPA or address) instead. The paper extends matching so agents report preferences and a characteristic, and derives results for several notions of strategy-proofness and false-name-proofness. Deferred Acceptance and Top Trading Cycles satisfy a weak false-name-proofness; DA also satisfies a strong version, while TTC fails it without an acyclicity assumption on priorities.

## Contribution

Brings false-name-proofness to two-sided matching and identifies DA as the robust choice.

## Key results

- DA and TTC satisfy weak false-name-proofness (abstract).
- DA satisfies strong false-name-proofness; TTC needs acyclic priorities (abstract).

## Methods and models

Priority-based matching with reported characteristics; variants for whether agents may claim objects won by fake accounts.

## Limitations and open questions

Abstract-level read. The ACM identifier is not a Crossref DOI, so the url points to the OpenAlex record I opened.

## Relevance to us

Task-to-agent assignment in a swarm is a matching problem; if tasks prioritise by declared capability and agents can register extra accounts, Deferred Acceptance is the mechanism with the stronger guarantee. Related: [[conitzer-2010-using]].
