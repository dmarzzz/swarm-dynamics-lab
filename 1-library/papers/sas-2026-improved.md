---
id: sas-2026-improved
type: paper
title: 'Improved estimators of causal emergence for large systems'
authors: ['Madalina I. Sas', 'Fernando E. Rosas', 'Hardik Rajpal', 'Daniel Bor', 'Henrik J. Jensen', 'Pedro A. M. Mediano']
year: 2026
venue: 'arXiv'
url: https://arxiv.org/abs/2601.00013
doi: null
arxiv: '2601.00013'
cite: 'Sas, M. I., Rosas, F. E., Rajpal, H., Bor, D., Jensen, H. J., & Mediano, P. A. M. (2026). Improved estimators of causal emergence for large systems. arXiv preprint arXiv:2601.00013.'
topics: [criticality-measurement, collective-motion]
added_by: dmarz/criticality-measurement
accessed: 2026-10-03
read_depth: abstract
relevance: 5
citations: '0 (OpenAlex, 2026-10-03)'
code: []
---

## Summary

Proposes a family of improved information-theoretic emergence measures that iteratively correct the
double-counting of shared (redundant) components that limits the whole-minus-sum Psi criterion of
[[rosas-2020-reconciling]] in large systems. The method trades computation for sensitivity and detects emergence
in simulated and real flocking data.

## Contribution

Addresses the main practical weakness of Psi (redundancy double counting), making emergence
estimation feasible for large swarms.

## Key results

- Improved estimators detect emergence in simulated and real-world flocking data where earlier measures are limited (claimed in abstract).
- Controllable trade-off between computational load and sensitivity.

## Methods and models

Iterative correction of double-counted terms in mutual-information-based emergence criteria. arXiv
preprint 2601.00013.

## Limitations and open questions

Preprint; abstract-level read; real flocking data set not identified from the abstract.

## Relevance to us

Probably the best current estimator for scoring emergence in our swarm simulations; read in full
before use. Related: [[rosas-2020-reconciling]], [[sas-2026-synch]].


## Notes from dmarz/criticality-measurement-audit

Audit 2026-10-03: arXiv abstract page and DataCite checked. Authors and title correct. arXiv v1 is dated 2025-12-20 although DataCite lists publicationYear 2026; year 2026 kept to match DataCite and the id. Summary matches the abstract. No corrections.
