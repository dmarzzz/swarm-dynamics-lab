---
id: kennedy-1999-small
type: paper
title: 'Small worlds and mega-minds: effects of neighborhood topology on particle swarm performance'
authors:
- James Kennedy
year: 1999
venue: Proceedings of the 1999 Congress on Evolutionary Computation (CEC99)
url: https://doi.org/10.1109/CEC.1999.785509
doi: 10.1109/CEC.1999.785509
arxiv: null
cite: 'Kennedy, J. (1999). Small worlds and mega-minds: Effects of neighborhood topology on particle swarm performance. In Proceedings of the 1999 Congress on Evolutionary Computation-CEC99 (Vol. 3, pp. 1931–1938). IEEE. https://doi.org/10.1109/CEC.1999.785509'
topics:
- swarm-intelligence
- sync-consensus
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 1064 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Manipulates the neighbourhood (communication) topology of particle swarms on four test functions, testing several
social-network structures with small-world randomisation of a specified number of links. Sociometric structure and
the small-world manipulation interacted with the test function to produce a significant effect on performance.

## Contribution

First systematic study of interaction-network topology in PSO, importing Watts-Strogatz small-world ideas; the
origin of the gbest/lbest/von Neumann topology literature.

## Key results

- Claimed in abstract: topology x function interaction significantly affects performance; no single topology wins
  everywhere (numbers not read).

## Methods and models

PSO with ring, wheel, star and randomly rewired neighbourhoods on four benchmark functions (abstract only).

## Limitations and open questions

Abstract-level reading; small set of functions. OpenAlex lists the record year as 2003 (proceedings indexing); the
conference took place in 1999.

## Relevance to us

Direct analogue of network-structure effects in consensus and flocking (who-listens-to-whom). Useful prior for any
hackathon experiment varying communication graphs in a swarm; see [[mendes-2004-fully]].
