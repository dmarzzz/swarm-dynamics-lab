---
id: degroot-1974-reaching
type: paper
title: Reaching a Consensus
authors: [Morris H. DeGroot]
year: 1974
venue: Journal of the American Statistical Association
url: https://api.openalex.org/works/doi:10.1080/01621459.1974.10480137
doi: 10.1080/01621459.1974.10480137
arxiv: null
cite: "DeGroot, M. H. (1974). Reaching a consensus. Journal of the American Statistical Association, 69(345), 118-121."
topics: [sync-consensus, collective-decision]
added_by: dmarz/sync-consensus
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "3595 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Models a committee whose members each hold a subjective probability distribution (or a point estimate) for an
unknown parameter and repeatedly revise it by pooling the others' opinions with fixed weights. The process is
described explicitly, and the common distribution the group converges to is determined explicitly.

## Contribution

The original iterated weighted-averaging ("DeGroot") model, x(t+1) = W x(t) with W row-stochastic, that underlies
linear consensus in control ([[jadbabaie-2003-coordination]], [[olfati-saber-2007-consensus]]) and social
learning models ([[proskurnikov-2017-tutorial]]). Its consensus value is a weighted average of initial opinions
(the weights being the stationary distribution of W; standard result, stated from the model rather than read
here).

## Key results

- Abstract: explicit pooling process and explicit consensus distribution; applies to point estimates too.

## Methods and models

Markov chain (row-stochastic matrix) iteration. Abstract from OpenAlex.

## Limitations and open questions

Fixed weights, no stubbornness or bounded confidence (see [[bernardo-2024-bounded]]); consensus requires
appropriate connectivity of W.

## Relevance to us

The simplest model of agents (human or LLM) averaging each other's estimates; a baseline for any
"wisdom of the swarm" or LLM-debate experiment in the llm-agent-swarms topic.
