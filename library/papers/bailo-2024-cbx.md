---
id: bailo-2024-cbx
type: paper
title: 'CBX: Python and Julia packages for consensus-based interacting particle methods'
authors:
- Rafael Bailo
- Alethea Barbaro
- Susana N. Gomes
- Konstantin Riedl
- Tim Roith
- Claudia Totzeck
- Urbain Vaes
year: 2024
venue: Journal of Open Source Software
url: https://api.openalex.org/works/W4393064299
doi: 10.21105/joss.06611
arxiv: '2403.14470'
cite: 'Bailo, R., Barbaro, A., Gomes, S. N., Riedl, K., Roith, T., Totzeck, C., & Vaes, U. (2024). CBX: Python and Julia packages for consensus-based interacting particle methods. Journal of Open Source Software, 9(98), 6611. https://doi.org/10.21105/joss.06611'
topics:
- swarm-intelligence
- sync-consensus
- meta
added_by: dmarz/swarm-intelligence
accessed: '2026-10-03'
read_depth: abstract
relevance: 4
citations: 6 (OpenAlex, 2026-10-03)
code: []
---

## Summary

Software paper presenting CBXPy and ConsensusBasedX.jl, Python and Julia implementations of consensus-based
interacting particle systems (CBX), which generalise CBO for global, derivative-free optimisation. Aims to offer
high-performance implementations plus a general interface extensible to further CBX variants, with a shared API
across the two languages.

## Contribution

Reference implementation for the CBO family ([[pinnau-2017-consensus]], [[fornasier-2024-consensus]]), useful for
reproducing swarm-optimiser dynamics without writing solvers.

## Key results

- Software release; no benchmark numbers in the abstract.

## Methods and models

Python (CBXPy) and Julia (ConsensusBasedX.jl) libraries; abstract only. Repositories are linked from the JOSS page
(not opened in this session; to be catalogued by the code scan).

## Limitations and open questions

Abstract-level reading; code not run here.

## Relevance to us

Fastest route to a hackathon experiment on CBO dynamics (variance decay, alpha/sigma phase behaviour, swarm-size
scaling). Code entry should be added by the code-scan task.
