---
id: leslie-2015-threshold
type: paper
title: 'Threshold FlipThem: When the Winner Does Not Need to Take All'
authors:
- David Leslie
- Chris Sherfield
- Nigel P. Smart
year: 2015
venue: Decision and Game Theory for Security (GameSec 2015), LNCS, 74-92
url: https://eprint.iacr.org/2015/784.pdf
doi: 10.1007/978-3-319-25594-1_5
arxiv: null
cite: 'Leslie, D., Sherfield, C., & Smart, N. P. (2015). Threshold FlipThem: When the Winner Does Not Need to Take All. In Decision and Game Theory for Security (GameSec 2015), Lecture Notes in Computer Science (pp. 74-92). Springer.'
topics:
- fork-merge-security
- sync-consensus
added_by: dmarz/fm
accessed: '2026-10-03'
read_depth: skim
relevance: 5
citations: 14 (Crossref, 2026-10-03)
code: []
---

## Summary

Studies an (n, t) FlipThem game: the attacker wins while holding at least t of n resources. The motivation explicitly includes MPC and Byzantine agreement, where control of more than n/3 parties breaks the protocol, and proactive security where the defender can regain parties. Uses continuous-time Markov chains to compute benefits and Nash equilibria. Two defender moves: full reset of all resources, or single-resource reset. The goal is to choose n and t, given relative costs, so a rational attacker does not play. I read the abstract, introduction and the experimental section.

## Contribution

Turns the Byzantine threshold into an economic design variable: pick n and t so attacking does not pay.

## Key results

- With full reset, equilibria depend only on the threshold t and costs, not on n (analytical).
- As the attacker's cost rises, the threshold the defender needs to maximise benefit falls.
- Numerical: with thresholds allowed up to n (N=7), the defender's best configuration is always full threshold; restricted to t < n/2, small cost ratios lead to configurations where the defender does not play and larger ratios require more servers.

## Methods and models

CTMC benefit functions, Nash equilibria of stochastic strategies, numerical optimisation over (n, t).

## Limitations and open questions

Single monolithic attacker; stylised costs; no correlated compromise.

## Relevance to us

- Q2: the closest existing formalism to dmarz's question. A parent that merges only when at least t of n returning children agree, and periodically re-forks children (reset), is an (n, t) FlipThem defender. The paper gives a way to set n and t from the attacker-to-defender cost ratio, rather than fixing t at the BFT bound of [[lamport-1982-byzantine]] and [[castro-1999-practical]]. Untested assumption for LLM agents: corruptions are independent. Contagion between children ([[papadopoulos-2026-mind]]) would break that.
Related: [[laszka-2014-flipthem]], [[van-dijk-2013-flipit]], [[korzhyk-2011-stackelberg]].
