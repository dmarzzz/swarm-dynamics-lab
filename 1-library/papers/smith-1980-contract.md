---
id: smith-1980-contract
type: paper
title: 'The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver'
authors:
- 'R. G. Smith'
year: 1980
venue: 'IEEE Transactions on Computers'
url: https://api.openalex.org/works/doi:10.1109/TC.1980.1675516
doi: 10.1109/TC.1980.1675516
arxiv: null
cite: 'Smith, R. G. (1980). The Contract Net Protocol: High-Level Communication and Control in a Distributed Problem Solver. IEEE Transactions on Computers, C-29(12), 1104-1113.'
topics:
- agent-budgets
added_by: dmarz/budget-c
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: 'Crossref 2026-10-03: 2455'
code: []
---

## Summary

Smith specifies a protocol for communication and control among nodes of a distributed problem solver in which tasks are distributed by negotiation: a node holding a task announces it, nodes able to execute it reply, and the task is awarded by a discussion between the two sides. Only the abstract was available to me (IEEE Xplore and ACM DL blocked automated access); the details below of announce, bid and award come from the abstract's description of negotiation and are not checked against the full text.

## Contribution

The founding task-sharing protocol for multi-agent systems. It frames task allocation among autonomous nodes as negotiation between nodes with tasks and nodes with capacity, rather than as central scheduling, and it is the ancestor of the auction-based allocation surveyed in [[dias-2006-market]].

## Key results

- Abstract claim: task distribution is effected by a negotiation process between nodes with tasks to be executed and nodes that may be able to execute those tasks.
- No quantitative results are stated in the abstract.

## Methods and models

A message protocol for a network of problem-solving nodes (abstract only; protocol message types and the worked example were not read).

## Limitations and open questions

Not read beyond the abstract. Crossref and OpenAlex list the author only as "Smith"; the initials R. G. come from the ACM DL listing as shown in a web-search result, not from a page I loaded. The protocol assumes cooperative nodes that report capability honestly; nothing in the abstract addresses self-interested or duplicated bidders, which is the gap false-name-proof mechanisms address ([[yokoo-2004-effect]], [[yokoo-2007-making]]).

## Relevance to us

The baseline for any orchestrator that hands sub-tasks to LLM workers by asking for bids: announce, bid, award. In an LLM swarm the bids are cheap to inflate and identities are cheap to clone, so contract-net-style delegation of token or tool budgets inherits the Sybil exposure in [[yokoo-2004-effect]]. Compare with the orchestrator-free coordination observed in [[anthropic-2026-patterns]].
