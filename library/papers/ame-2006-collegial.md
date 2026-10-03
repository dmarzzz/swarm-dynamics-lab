---
id: ame-2006-collegial
type: paper
title: "Collegial decision making based on social amplification leads to optimal group formation"
authors: ["Jean-Marc Amé", "José Halloy", "Colette Rivault", "Claire Detrain", "Jean Louis Deneubourg"]
year: 2006
venue: "Proceedings of the National Academy of Sciences"
url: "https://www.ebi.ac.uk/europepmc/webservices/rest/article/MED/16581903?resultType=core&format=json"
doi: "10.1073/pnas.0507877103"
arxiv: null
cite: "Amé, J., Halloy, J., Rivault, C., Detrain, C., & Deneubourg, J. L. (2006). Collegial decision making based on social amplification leads to optimal group formation. Proceedings of the National Academy of Sciences, 103(15), 5835–5840. https://doi.org/10.1073/pnas.0507877103"
topics: ["collective-decision", "swarm-intelligence"]
added_by: dmarz/collective-decision
accessed: 2026-10-03
read_depth: abstract
relevance: 4
citations: "247 (OpenAlex, 2026-10-03)"
code: []
---

## Summary

Experiments and a model of shelter selection by cockroach groups show that groups choose one shelter through nonlinear social amplification among equal individuals, with no leaders, no comparison of shelters and limited information. The probability of leaving a shelter falls with the number already sheltering, and the mechanism yields groups whose size distribution maximises mean individual benefit.

## Contribution

Source of the cockroach quorum-like leaving function (fitted exponent about 2, see [[sumpter-2009-quorum]]) and of the 'collegial decision' concept used in robot aggregation studies and [[halloy-2007-social]].

## Key results

- Decisions emerge on the move without comparison of options (experiment and model).
- The mechanism leads to optimal mean benefit for group members (model).
- Abstract-level reading only; numbers beyond the abstract were not checked.

## Methods and models

Blattella germanica in arenas with shelters of varying capacity; stochastic model with leaving rate theta / (1 + rho (x/S)^n).

## Limitations and open questions

Shelter capacity and odour cues specific to cockroaches.

## Relevance to us

A minimal decision rule (stay longer where more others are) that needs no communication; implemented on robots by Garnier et al. and Campo et al. (see [[valentini-2017-best]]).
