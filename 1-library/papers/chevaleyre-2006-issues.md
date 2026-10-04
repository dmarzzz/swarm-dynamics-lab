---
id: chevaleyre-2006-issues
type: paper
title: 'Issues in Multiagent Resource Allocation'
authors:
- 'Yann Chevaleyre'
- 'Paul E. Dunne'
- 'Ulle Endriss'
- 'Jérôme Lang'
- 'Michel Lemaître'
- 'Nicolas Maudet'
- 'Julian Padget'
- 'Steve Phelps'
- 'Juan A. Rodríguez-Aguilar'
- 'Paulo Sousa'
year: 2006
venue: 'Informatica'
url: https://www.informatica.si/index.php/informatica/article/view/70
doi: null
arxiv: null
cite: 'Chevaleyre, Y., Dunne, P. E., Endriss, U., Lang, J., Lemaître, M., Maudet, N., Padget, J., Phelps, S., Rodríguez-Aguilar, J. A., & Sousa, P. (2006). Issues in Multiagent Resource Allocation. Informatica, 30(1), 3-31.'
topics:
- agent-budgets
added_by: dmarz/budget-c
accessed: 2026-10-03
read_depth: skim
relevance: 4
citations: null
code: []
---

## Summary

A survey by the AgentLink Technical Forum Group on Multiagent Resource Allocation (MARA). It defines the problem (resources, allocations, agent preferences, centralised or distributed procedures, objectives), reviews preference representation languages and social welfare measures (utilitarian, egalitarian, leximin, Pareto optimality, envy-freeness), allocation procedures (auctions and negotiation), complexity results and simulation platforms, and four application areas: industrial procurement, Earth observation satellites, manufacturing control and grid computing.

## Contribution

A shared vocabulary and catalogue for MARA at the boundary of computer science and economics, with emphasis on computational questions: compact preference representation, complexity of finding feasible or optimal allocations, and convergence of distributed negotiation.

## Key results

- Convergence (citing Sandholm): with monetary side payments and quasi-linear payoffs, any sequence of mutually beneficial deals over finitely many indivisible resources ends at an allocation with maximal utilitarian social welfare; without side payments such sequences converge to a Pareto optimal allocation.
- These results need truly multilateral deals; with modular utility functions, single-resource bilateral deals with side payments are sufficient.
- Taxonomy of resources: continuous or discrete, divisible or not, sharable or not, static or not, single-unit or multi-unit, resources versus tasks.

## Methods and models

Survey and synthesis; no new experiments. No DOI found: Crossref bibliographic search returned no match, and the Informatica page lists none. Volume 30, issue 1 from the Informatica page metadata; pages 3-31 from Endriss's publication list (staff.science.uva.nl/u.endriss/pubs). I skimmed the author-hosted PDF (illc.uva.nl/~ulle/MARA/mara-survey.pdf): abstract, introduction, convergence section and conclusion.

## Limitations and open questions

The authors say they do not cover the algorithmics of MARA (for example winner determination in combinatorial auctions) or the game-theoretic analysis of negotiation strategies. Topic selection is acknowledged to follow the authors' interests. Truthful reporting is noted as the aim of mechanism design but identity-splitting is not treated.

## Relevance to us

Gives the welfare criteria (utilitarian, egalitarian, envy-free) we can use to score how a swarm divides a token or compute budget, and the deal-convergence results tell us when local trading among agents can reach a good split without a central allocator. The missing identity dimension is covered by [[yokoo-2004-effect]] and [[yokoo-2007-making]]. Classical instances: [[wellman-1993-market]], [[smith-1980-contract]], [[dias-2006-market]].
